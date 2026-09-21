import base64
import logging
import sys
import subprocess
import time
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

logger = logging.getLogger("app.sandbox")

try:
    import docker
    from docker.errors import DockerException, APIError, NotFound
    HAS_DOCKER_LIB = True
except ImportError:
    docker = None
    DockerException = Exception
    APIError = Exception
    NotFound = Exception
    HAS_DOCKER_LIB = False


# =====================================================================
# Pydantic Result & Request Models
# =====================================================================

class ExecutionResult(BaseModel):
    """Model pentru rezultatul execuției unui script de cod în sandbox."""
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    execution_time_ms: float = 0.0
    status: str = "success"  # "success", "timeout", "error"
    error: Optional[str] = None
    runner: str = "docker"   # "docker" sau "fallback"
    warning: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class TestCaseItem(BaseModel):
    """Model pentru un caz de test."""
    id: Optional[int] = None
    input_data: Optional[str] = ""
    expected_output: str
    is_hidden: bool = False


class TestRunResult(BaseModel):
    """Rezultat pentru un singur caz de test."""
    test_id: Optional[int] = None
    status: str  # "PASSED" sau "FAILED"
    is_hidden: bool = False
    expected: str
    got: str
    execution_time_ms: float = 0.0
    error: Optional[str] = None


class TestSuiteResult(BaseModel):
    """Rezultat agregat pentru o suită de teste."""
    all_passed: bool
    passed_count: int
    total_count: int
    score: float
    results: List[TestRunResult]
    runner: str = "docker"
    warning: Optional[str] = None


# =====================================================================
# Fallback Local Sandbox (Când Docker Daemon este oprit/indisponibil)
# =====================================================================

class SecureLocalSandbox:
    """
    Fallback securizat local bazat pe procese izolate (subprocess) cu timeout strict.
    Se activează automat atunci când Docker Daemon nu rulează pe server.
    """

    @staticmethod
    def _build_runner_script(code: str, input_data: str = "") -> str:
        b64_code = base64.b64encode(code.encode("utf-8")).decode("ascii")
        b64_input = base64.b64encode((input_data or "").encode("utf-8")).decode("ascii")
        
        return (
            "import sys, io, base64\n"
            f"code = base64.b64decode('{b64_code}').decode('utf-8')\n"
            f"raw_input = base64.b64decode('{b64_input}').decode('utf-8')\n"
            "if raw_input:\n"
            "    sys.stdin = io.StringIO(raw_input)\n"
            "sys.argv = ['student_code.py']\n"
            "g = {'__name__': '__main__', '__file__': 'student_code.py'}\n"
            "compiled = compile(code, 'student_code.py', 'exec')\n"
            "exec(compiled, g)\n"
        )

    def run_code(self, code: str, input_data: str = "", timeout: float = 3.5) -> ExecutionResult:
        start_time = time.perf_counter()
        runner_script = self._build_runner_script(code, input_data)

        proc = None
        try:
            proc = subprocess.Popen(
                [sys.executable, "-u", "-c", runner_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout_data, stderr_data = proc.communicate(timeout=timeout)
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            exit_code = proc.returncode

            status = "success" if exit_code == 0 else "error"
            err_msg = stderr_data.strip() if exit_code != 0 else None

            return ExecutionResult(
                stdout=stdout_data,
                stderr=stderr_data,
                exit_code=exit_code,
                execution_time_ms=elapsed_ms,
                status=status,
                error=err_msg,
                runner="fallback",
                warning="Executat via Local Sandbox Fallback (Docker Daemon indisponibil).",
            )

        except subprocess.TimeoutExpired:
            if proc:
                try:
                    proc.kill()
                    proc.communicate()
                except Exception:
                    pass
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            timeout_msg = "TimeoutError: Timpul de execuție a fost depășit"
            return ExecutionResult(
                stdout="",
                stderr=timeout_msg,
                exit_code=-1,
                execution_time_ms=elapsed_ms,
                status="timeout",
                error=timeout_msg,
                runner="fallback",
                warning="Executat via Local Sandbox Fallback (Docker Daemon indisponibil).",
            )
        except Exception as e:
            logger.error(f"Error in local sandbox execution: {e}")
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return ExecutionResult(
                stdout="",
                stderr=str(e),
                exit_code=-1,
                execution_time_ms=elapsed_ms,
                status="error",
                error=f"Eroare execuție locală: {str(e)}",
                runner="fallback",
                warning="Executat via Local Sandbox Fallback (Docker Daemon indisponibil).",
            )


# =====================================================================
# Docker Sandbox Runner Principal
# =====================================================================

class DockerSandboxRunner:
    """
    Execuție securizată de cod în containere ephemere Docker conform cerințelor:
    - Docker SDK Integration (python:3.12-slim)
    - Resurse & Securitate:
      * auto_remove=True
      * mem_limit='128m'
      * nano_cpus=500000000 (0.5 cores)
      * network_disabled=True
      * user='nobody'
      * read_only=True
      * tmpfs={'/tmp': 'rw,size=16m,mode=1777'}
    - Gestiune input_data și timeout strict (3-5s) cu container.kill() forțat
    - Returnare structurată ExecutionResult
    - Fallback grațios dacă Docker Daemon nu este pornit
    """

    def __init__(
        self,
        image: str = "python:3.12-slim",
        mem_limit: str = "128m",
        nano_cpus: int = 500000000,
        network_disabled: bool = True,
        user: str = "nobody",
        read_only: bool = True,
        tmpfs: Optional[Dict[str, str]] = None,
        auto_remove: bool = True,
        default_timeout: float = 3.5,
    ):
        self.image = image
        self.mem_limit = mem_limit
        self.nano_cpus = nano_cpus
        self.network_disabled = network_disabled
        self.user = user
        self.read_only = read_only
        self.tmpfs = tmpfs or {"/tmp": "rw,size=16m,mode=1777"}
        self.auto_remove = auto_remove
        self.default_timeout = default_timeout
        self.fallback = SecureLocalSandbox()
        self._client = None

    def get_docker_client(self):
        """Obține clientul Docker SDK sau returnează None dacă daemonul nu este activ."""
        if not HAS_DOCKER_LIB:
            return None
        try:
            if self._client is None:
                self._client = docker.from_env()
            self._client.ping()
            return self._client
        except Exception as e:
            logger.debug(f"Docker ping eșuat: {e}")
            self._client = None
            return None

    def is_docker_available(self) -> bool:
        """Verifică dacă Docker daemon este funcțional."""
        return self.get_docker_client() is not None

    def _build_runner_script(self, code: str, input_data: str = "") -> str:
        b64_code = base64.b64encode(code.encode("utf-8")).decode("ascii")
        b64_input = base64.b64encode((input_data or "").encode("utf-8")).decode("ascii")
        
        return (
            "import sys, io, base64\n"
            f"code = base64.b64decode('{b64_code}').decode('utf-8')\n"
            f"raw_input = base64.b64decode('{b64_input}').decode('utf-8')\n"
            "if raw_input:\n"
            "    sys.stdin = io.StringIO(raw_input)\n"
            "sys.argv = ['student_code.py']\n"
            "g = {'__name__': '__main__', '__file__': 'student_code.py'}\n"
            "compiled = compile(code, 'student_code.py', 'exec')\n"
            "exec(compiled, g)\n"
        )

    def run_code(
        self,
        code: str,
        input_data: str = "",
        timeout: Optional[float] = None,
        force_fallback: bool = False,
    ) -> ExecutionResult:
        """
        Execută codul transmis într-un container temporar Docker.
        Dacă Docker Daemon nu este pornit, apelează automat fallback-ul securizat.
        """
        actual_timeout = timeout if timeout is not None else self.default_timeout
        # Limitare timeout strict între 1.0 și 10.0 secunde
        actual_timeout = max(1.0, min(10.0, actual_timeout))

        if force_fallback or not self.is_docker_available():
            logger.info("Docker Daemon indisponibil. Se folosește fallback-ul securizat local.")
            return self.fallback.run_code(code, input_data=input_data, timeout=actual_timeout)

        client = self.get_docker_client()
        if not client:
            logger.warning("Docker client unavailable, switching to fallback")
            return self.fallback.run_code(code, input_data=input_data, timeout=actual_timeout)

        runner_script = self._build_runner_script(code, input_data)
        command = ["python", "-u", "-c", runner_script]

        start_time = time.perf_counter()
        container = None

        try:
            # Creare container cu toți parametrii de securitate și izolare
            container = client.containers.create(
                image=self.image,
                command=command,
                mem_limit=self.mem_limit,
                nano_cpus=self.nano_cpus,
                network_disabled=self.network_disabled,
                user=self.user,
                read_only=self.read_only,
                tmpfs=self.tmpfs,
                auto_remove=self.auto_remove,
                detach=True,
            )

            # Pornire container
            container.start()

            # Așteptare execuție cu timeout strict (3-5 secunde)
            deadline = time.perf_counter() + actual_timeout
            is_finished = False
            exit_code = 0

            while time.perf_counter() < deadline:
                try:
                    container.reload()
                    status = container.status
                    if status in ["exited", "dead"]:
                        is_finished = True
                        attrs = container.attrs
                        state = attrs.get("State", {})
                        exit_code = state.get("ExitCode", 0)
                        break
                except (NotFound, APIError) as e:
                    # Dacă auto_remove=True a șters deja containerul la terminare
                    logger.debug(f"Container not found during reload: {e}")
                    is_finished = True
                    break
                time.sleep(0.05)

            # Tratare timeout: dacă după timeout containerul încă rulează
            if not is_finished:
                logger.warning(f"Timeout depășit ({actual_timeout}s). Forțare oprire container Docker.")
                try:
                    container.kill()
                except Exception as kill_err:
                    logger.debug(f"Eroare kill container: {kill_err}")

                elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
                timeout_msg = "TimeoutError: Timpul de execuție a fost depășit"
                return ExecutionResult(
                    stdout="",
                    stderr=timeout_msg,
                    exit_code=-1,
                    execution_time_ms=elapsed_ms,
                    status="timeout",
                    error=timeout_msg,
                    runner="docker",
                )

            # Extragere stdout și stderr
            stdout_str = ""
            stderr_str = ""
            try:
                raw_stdout = container.logs(stdout=True, stderr=False)
                raw_stderr = container.logs(stdout=False, stderr=True)
                stdout_str = raw_stdout.decode("utf-8", errors="replace") if isinstance(raw_stdout, bytes) else str(raw_stdout or "")
                stderr_str = raw_stderr.decode("utf-8", errors="replace") if isinstance(raw_stderr, bytes) else str(raw_stderr or "")
            except Exception as e:
                # În caz că auto_remove a șters containerul înainte de logs
                logger.debug(f"Error extracting container logs: {e}")

            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            run_status = "success" if exit_code == 0 else "error"
            err_msg = stderr_str.strip() if exit_code != 0 else None

            return ExecutionResult(
                stdout=stdout_str,
                stderr=stderr_str,
                exit_code=exit_code,
                execution_time_ms=elapsed_ms,
                status=run_status,
                error=err_msg,
                runner="docker",
            )

        except DockerException as de:
            logger.error(f"Eroare Docker API: {de}. Se comută la fallback.")
            return self.fallback.run_code(code, input_data=input_data, timeout=actual_timeout)
        except Exception as e:
            logger.error(f"Eroare neașteptată în Docker Sandbox: {e}. Se comută la fallback.")
            return self.fallback.run_code(code, input_data=input_data, timeout=actual_timeout)
        finally:
            # Curățare garantată dacă auto_remove nu a intervenit încă
            if container is not None:
                try:
                    container.remove(force=True)
                except Exception as e:
                    logger.debug(f"Error removing container: {e}")

    def run_test_cases(
        self,
        code: str,
        test_cases: List[TestCaseItem],
        timeout: Optional[float] = None,
    ) -> TestSuiteResult:
        """
        Execută codul împotriva unei liste de cazuri de test și returnează rezultatul structurat.
        """
        results: List[TestRunResult] = []
        passed_count = 0
        total_count = len(test_cases)
        runner_used = "docker" if self.is_docker_available() else "fallback"
        warning_msg = None if self.is_docker_available() else "Executat via Local Sandbox Fallback."

        for tc in test_cases:
            run_res = self.run_code(code, input_data=tc.input_data or "", timeout=timeout)
            if run_res.runner == "fallback":
                runner_used = "fallback"
                warning_msg = run_res.warning

            got_output = run_res.stdout.strip()
            expected_output = tc.expected_output.strip()

            passed = (run_res.exit_code == 0) and (got_output == expected_output)
            if passed:
                passed_count += 1

            results.append(
                TestRunResult(
                    test_id=tc.id,
                    status="PASSED" if passed else "FAILED",
                    is_hidden=tc.is_hidden,
                    expected=expected_output if not tc.is_hidden else "HIDDEN",
                    got=got_output if not tc.is_hidden else "HIDDEN",
                    execution_time_ms=run_res.execution_time_ms,
                    error=run_res.error,
                )
            )

        all_passed = (passed_count == total_count) if total_count > 0 else False
        score = round((passed_count / total_count) * 100.0, 2) if total_count > 0 else 0.0

        return TestSuiteResult(
            all_passed=all_passed,
            passed_count=passed_count,
            total_count=total_count,
            score=score,
            results=results,
            runner=runner_used,
            warning=warning_msg,
        )


# Instanță singleton gata de utilizat în endpoints
sandbox_service = DockerSandboxRunner()
