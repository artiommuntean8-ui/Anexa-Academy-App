import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Asigurare cale către backend în sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.services.docker_sandbox import (
    DockerSandboxRunner,
    SecureLocalSandbox,
    ExecutionResult,
    TestCaseItem,
    TestSuiteResult,
)
from app.main import app
from app.api.v1.endpoints.sandbox import (
    run_code as api_run_code,
    test_code as api_test_code,
    get_sandbox_status,
    CodeRunRequest,
    CodeTestRequest,
    SingleTestCase,
)


class TestDockerSandboxRunner(unittest.TestCase):
    def setUp(self):
        self.runner = DockerSandboxRunner()

    def test_01_default_configuration_and_limits(self):
        """1. Verificare cerințe securitate și resurse Docker SDK."""
        self.assertEqual(self.runner.image, "python:3.12-slim")
        self.assertEqual(self.runner.mem_limit, "128m")
        self.assertEqual(self.runner.nano_cpus, 500000000)
        self.assertTrue(self.runner.network_disabled)
        self.assertEqual(self.runner.user, "nobody")
        self.assertTrue(self.runner.read_only)
        self.assertIn("/tmp", self.runner.tmpfs)
        self.assertTrue(self.runner.auto_remove)
        self.assertTrue(3.0 <= self.runner.default_timeout <= 5.0)

    def test_02_docker_container_creation_args_mocked(self):
        """2. Verificare că la apelul Docker se transmit toți parametrii de securitate și kill la timeout."""
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_client.containers.create.return_value = mock_container

        # Simulăm un timeout în container
        mock_container.status = "running"
        mock_container.reload.side_effect = None

        with patch.object(self.runner, "get_docker_client", return_value=mock_client), \
             patch.object(self.runner, "is_docker_available", return_value=True):
            
            result = self.runner.run_code(
                code="while True: pass",
                input_data="test_input",
                timeout=1.0,
            )

            # Verificare că containerul a fost creat cu argumentele cerute
            mock_client.containers.create.assert_called_once()
            _, kwargs = mock_client.containers.create.call_args
            
            self.assertEqual(kwargs["image"], "python:3.12-slim")
            self.assertEqual(kwargs["mem_limit"], "128m")
            self.assertEqual(kwargs["nano_cpus"], 500000000)
            self.assertTrue(kwargs["network_disabled"])
            self.assertEqual(kwargs["user"], "nobody")
            self.assertTrue(kwargs["read_only"])
            self.assertTrue(kwargs["auto_remove"])
            self.assertIn("/tmp", kwargs["tmpfs"])

            # Verificare că kill() a fost apelat pentru forțarea opririi la timeout
            mock_container.kill.assert_called_once()
            self.assertEqual(result.status, "timeout")
            self.assertIn("TimeoutError: Timpul de execuție a fost depășit", result.stderr)

    def test_03_standard_code_execution_fallback(self):
        """3. Execuție standard cod Python (print output)."""
        code = "print('Hello from Anexa Sandbox!')"
        res = self.runner.run_code(code, force_fallback=True)
        
        self.assertEqual(res.exit_code, 0)
        self.assertEqual(res.stdout.strip(), "Hello from Anexa Sandbox!")
        self.assertEqual(res.stderr, "")
        self.assertEqual(res.status, "success")
        self.assertGreater(res.execution_time_ms, 0)

    def test_04_stdin_input_handling(self):
        """4. Verificare transmitere input_data către sys.stdin."""
        code = (
            "nume = input()\n"
            "varsta = input()\n"
            "print(f'Elev: {nume}, Varsta: {varsta}')\n"
        )
        res = self.runner.run_code(code, input_data="Alex\n14\n", force_fallback=True)
        
        self.assertEqual(res.exit_code, 0)
        self.assertEqual(res.stdout.strip(), "Elev: Alex, Varsta: 14")
        self.assertEqual(res.status, "success")

    def test_05_infinite_loop_timeout_kill(self):
        """5. Verificare oprire forțată la buclă infinită și returnare TimeoutError."""
        code = "while True:\n    pass\n"
        res = self.runner.run_code(code, timeout=1.2, force_fallback=True)

        self.assertEqual(res.status, "timeout")
        self.assertEqual(res.exit_code, -1)
        self.assertIn("TimeoutError: Timpul de execuție a fost depășit", res.stderr)
        self.assertIn("TimeoutError: Timpul de execuție a fost depășit", res.error)

    def test_06_syntax_and_runtime_errors(self):
        """6. Verificare captură erori de execuție (stderr și exit_code non-zero)."""
        code = "x = 10 / 0"
        res = self.runner.run_code(code, force_fallback=True)

        self.assertNotEqual(res.exit_code, 0)
        self.assertEqual(res.status, "error")
        self.assertIn("ZeroDivisionError: division by zero", res.stderr)

    def test_07_run_test_cases_suite(self):
        """7. Verificare evaluare suită de cazuri de test cu input_data diferit."""
        code = (
            "num = int(input())\n"
            "print('PAR' if num % 2 == 0 else 'IMPAR')\n"
        )
        test_cases = [
            TestCaseItem(id=1, input_data="4", expected_output="PAR"),
            TestCaseItem(id=2, input_data="7", expected_output="IMPAR"),
            TestCaseItem(id=3, input_data="10", expected_output="IMPAR"), # Va pica intenționat
        ]

        suite_res = self.runner.run_test_cases(code, test_cases)
        
        self.assertFalse(suite_res.all_passed)
        self.assertEqual(suite_res.passed_count, 2)
        self.assertEqual(suite_res.total_count, 3)
        self.assertAlmostEqual(suite_res.score, 66.67, places=1)
        self.assertEqual(suite_res.results[0].status, "PASSED")
        self.assertEqual(suite_res.results[1].status, "PASSED")
        self.assertEqual(suite_res.results[2].status, "FAILED")

    def test_08_fastapi_endpoints_run_and_test(self):
        """8. Verificare apelare directă a endpoint-urilor FastAPI /api/sandbox/run și /api/sandbox/test."""
        # Test endpoint run
        run_req = CodeRunRequest(
            code="print('Test FastAPI Run Direct')",
            input_data="",
            timeout=3.0,
        )
        res = api_run_code(run_req)
        self.assertEqual(res.stdout.strip(), "Test FastAPI Run Direct")
        self.assertEqual(res.exit_code, 0)
        self.assertGreater(res.execution_time_ms, 0)

        # Test endpoint test cu cazuri manuale
        test_req = CodeTestRequest(
            code="print(input().upper())",
            test_cases=[
                SingleTestCase(input_data="salut", expected_output="SALUT"),
                SingleTestCase(input_data="anexa", expected_output="ANEXA"),
            ],
            timeout=3.0,
        )
        mock_db = MagicMock()
        res_test = api_test_code(test_req, db=mock_db)
        self.assertTrue(res_test.all_passed)
        self.assertEqual(res_test.passed_count, 2)
        self.assertEqual(res_test.score, 100.0)

        # Test status endpoint
        status_data = get_sandbox_status()
        self.assertEqual(status_data["status"], "ready")
        self.assertIn("limits", status_data)
        self.assertEqual(status_data["limits"]["memory"], "128m")
        self.assertEqual(status_data["limits"]["nano_cpus"], 500000000)
        self.assertTrue(status_data["limits"]["network_disabled"])
        self.assertEqual(status_data["limits"]["user"], "nobody")
        self.assertTrue(status_data["limits"]["read_only"])
        self.assertTrue(status_data["limits"]["auto_remove"])



if __name__ == "__main__":
    unittest.main()
