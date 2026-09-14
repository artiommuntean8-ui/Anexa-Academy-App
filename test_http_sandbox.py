import sys
import os
import json
import time
import subprocess
import urllib.request
import urllib.error

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    print("=== STARTING LIVE HTTP ENDPOINTS TEST ===")
    
    # Pornim serverul backend uvicorn pe un port dedicat de test (port 8009)
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.getcwd(), "backend")
    
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8009"],
        cwd=os.path.join(os.getcwd(), "backend"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
    )

    try:
        # Așteptăm câteva secunde pentru pornirea serverului
        time.sleep(3)
        
        base_url = "http://127.0.0.1:8009"

        # 1. Test GET /api/sandbox/status
        print("\n1. Testing GET /api/sandbox/status...")
        req = urllib.request.Request(f"{base_url}/api/sandbox/status")
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            body = json.loads(response.read().decode("utf-8"))
            print(f"Status code: {status_code}")
            print(f"Response: {body}")
            assert status_code == 200
            assert body["status"] == "ready"
            assert "limits" in body
            print(">>> GET /api/sandbox/status: PASSED")

        # 2. Test POST /api/sandbox/run
        print("\n2. Testing POST /api/sandbox/run...")
        run_data = json.dumps({
            "code": "name = input()\nprint(f'Bun venit la Docker Sandbox, {name}!')",
            "input_data": "Alexandru",
            "timeout": 3.0
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{base_url}/api/sandbox/run",
            data=run_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            body = json.loads(response.read().decode("utf-8"))
            print(f"Status code: {status_code}")
            print(f"Response: {body}")
            assert status_code == 200
            assert "Bun venit la Docker Sandbox, Alexandru!" in body["stdout"]
            assert body["exit_code"] == 0
            assert body["execution_time_ms"] > 0
            print(">>> POST /api/sandbox/run: PASSED")

        # 3. Test POST /api/v1/sandbox/run (alias)
        print("\n3. Testing POST /api/v1/sandbox/run (alias)...")
        req = urllib.request.Request(
            f"{base_url}/api/v1/sandbox/run",
            data=run_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            body = json.loads(response.read().decode("utf-8"))
            assert status_code == 200
            assert body["exit_code"] == 0
            print(">>> POST /api/v1/sandbox/run (alias): PASSED")

        # 4. Test POST /api/sandbox/test
        print("\n4. Testing POST /api/sandbox/test...")
        test_data = json.dumps({
            "code": "n = int(input())\nprint(n * 2)",
            "test_cases": [
                {"input_data": "5", "expected_output": "10"},
                {"input_data": "21", "expected_output": "42"}
            ],
            "timeout": 3.0
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{base_url}/api/sandbox/test",
            data=test_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            body = json.loads(response.read().decode("utf-8"))
            print(f"Status code: {status_code}")
            print(f"Response: {body}")
            assert status_code == 200
            assert body["all_passed"] is True
            assert body["score"] == 100.0
            assert body["passed_count"] == 2
            print(">>> POST /api/sandbox/test: PASSED")

        # 5. Test POST /api/sandbox/run cu Infinite Loop (Timeout)
        print("\n5. Testing Timeout Handling on POST /api/sandbox/run...")
        timeout_data = json.dumps({
            "code": "while True: pass",
            "input_data": "",
            "timeout": 1.5
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{base_url}/api/sandbox/run",
            data=timeout_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            status_code = response.getcode()
            body = json.loads(response.read().decode("utf-8"))
            print(f"Status code: {status_code}")
            print(f"Response: {body}")
            assert status_code == 200
            assert body["status"] == "timeout"
            assert "TimeoutError: Timpul de execuție a fost depășit" in body["stderr"]
            assert body["exit_code"] == -1
            print(">>> Timeout Handling on POST /api/sandbox/run: PASSED")

        print("\n=== ALL LIVE HTTP TESTS PASSED SUCCESSFULLY! ===")

    finally:
        server_process.terminate()
        server_process.wait(timeout=5)

if __name__ == "__main__":
    main()
