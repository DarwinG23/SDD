import asyncio
import tempfile
from pathlib import Path


class TestRunner:
    TIMEOUT_SECONDS = 60

    async def execute_tests(self, source_code: str, test_code: str) -> dict:
        with tempfile.TemporaryDirectory() as tmpdir:
            if source_code:
                source_file = Path(tmpdir) / "source.py"
                source_file.write_text(source_code, encoding="utf-8")
                full_test = f"from source import *\n\n{test_code}"
            else:
                full_test = test_code
            test_file = Path(tmpdir) / "test_generated.py"
            test_file.write_text(full_test, encoding="utf-8")

            try:
                process = await asyncio.create_subprocess_exec(
                    "pytest", str(test_file), "-v", "--no-header",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=tmpdir,
                )
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=self.TIMEOUT_SECONDS
                )
                return {
                    "success": process.returncode == 0,
                    "stdout": stdout.decode("utf-8", errors="replace"),
                    "stderr": stderr.decode("utf-8", errors="replace"),
                    "exit_code": process.returncode,
                }
            except asyncio.TimeoutError:
                if process and process.returncode is None:
                    process.kill()
                    await process.wait()
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": "Timeout: test execution exceeded 60 seconds.",
                    "exit_code": -1,
                }

    async def execute_tests_from_path(self, source_path: Path, test_code: str) -> dict:
        source_code = source_path.read_text(encoding="utf-8")
        return await self.execute_tests(source_code, test_code)

    def parse_test_result(self, raw_result: dict) -> dict:
        stdout = raw_result.get("stdout", "")
        stderr = raw_result.get("stderr", "")
        passed = "passed" in stdout or "passed" in stderr
        failed = "failed" in stdout or "FAILED" in stdout
        error_count = 0
        passed_count = 0
        for line in stdout.splitlines():
            if "PASSED" in line or "passed" in line:
                passed_count += 1
            if "FAILED" in line:
                error_count += 1
        return {
            "success": raw_result.get("success", False),
            "passed": passed_count,
            "failed": error_count,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": raw_result.get("exit_code", -1),
        }
