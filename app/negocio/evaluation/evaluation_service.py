import subprocess
import tempfile
from pathlib import Path
from typing import Any


class EvaluationService:
    COVERAGE_THRESHOLD = 80.0
    MUTATION_THRESHOLD = 70.0
    FAILURE_DETECTION_THRESHOLD = 60.0

    def run_coverage(self, source_path: Path, test_code: str) -> float:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_code = source_path.read_text(encoding="utf-8")
            source_copy = Path(tmpdir) / "source.py"
            source_copy.write_text(source_code, encoding="utf-8")
            test_file = Path(tmpdir) / "test_generated.py"
            test_file.write_text(f"from source import *\n\n{test_code}", encoding="utf-8")

            result = subprocess.run(
                [
                    "coverage", "run",
                    "--source", str(tmpdir),
                    "-m", "pytest", str(test_file),
                    "-q", "--no-header",
                ],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=tmpdir,
            )
            report = subprocess.run(
                ["coverage", "report", "--format=total"],
                capture_output=True,
                text=True,
                cwd=tmpdir,
            )
            try:
                return float(report.stdout.strip().rstrip("%"))
            except (ValueError, AttributeError):
                return 0.0

    def run_mutation_score(self, source_path: Path, test_code: str) -> float:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_copy = Path(tmpdir) / "source.py"
            source_copy.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
            test_file = Path(tmpdir) / "test_source.py"
            test_file.write_text(f"from source import *\n\n{test_code}", encoding="utf-8")

            result = subprocess.run(
                ["mutmut", "run", "--paths-to-mutate", str(source_copy)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=tmpdir,
            )
            result = subprocess.run(
                ["mutmut", "results"],
                capture_output=True,
                text=True,
                cwd=tmpdir,
            )
            try:
                lines = result.stdout.strip().splitlines()
                for line in lines:
                    if "killed" in line.lower() and "/" in line:
                        parts = line.split()
                        killed = int(parts[0])
                        total = int(parts[2])
                        return (killed / total * 100) if total > 0 else 100.0
                return 0.0
            except (ValueError, IndexError):
                return 0.0

    def run_failure_detection(self, source_path: Path, test_code: str) -> float:
        import ast
        source_code = source_path.read_text(encoding="utf-8")
        original_tree = ast.parse(source_code)
        function_defs = [n for n in ast.walk(original_tree) if isinstance(n, ast.FunctionDef)]
        if not function_defs:
            return 100.0

        detected = 0
        total = len(function_defs)

        for func in function_defs:
            mutated_source = self._mutate_function(source_code, func.name)
            if mutated_source == source_code:
                continue
            with tempfile.TemporaryDirectory() as tmpdir:
                mutated_file = Path(tmpdir) / "source.py"
                mutated_file.write_text(mutated_source, encoding="utf-8")
                test_file = Path(tmpdir) / "test_source.py"
                test_file.write_text(f"from source import *\n\n{test_code}", encoding="utf-8")

                result = subprocess.run(
                    ["pytest", str(test_file), "-q", "--no-header"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=tmpdir,
                )
                if result.returncode != 0:
                    detected += 1

        return (detected / total * 100) if total > 0 else 100.0

    def _mutate_function(self, source: str, func_name: str) -> str:
        import ast
        class FunctionMutator(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                if node.name == func_name:
                    for stmt in node.body:
                        if isinstance(stmt, ast.Return):
                            if isinstance(stmt.value, ast.Constant):
                                if isinstance(stmt.value.value, bool):
                                    stmt.value.value = not stmt.value.value
                                elif isinstance(stmt.value.value, (int, float)):
                                    stmt.value.value = stmt.value.value + 1
                            elif isinstance(stmt.value, ast.Name):
                                if stmt.value.id == "True":
                                    stmt.value.id = "False"
                                elif stmt.value.id == "False":
                                    stmt.value.id = "True"
                return node

        tree = ast.parse(source)
        tree = FunctionMutator().visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def check_thresholds(self, coverage: float, mutation: float, failure_detection: float) -> dict[str, Any]:
        results = {
            "coverage": {"value": coverage, "threshold": self.COVERAGE_THRESHOLD, "passed": coverage >= self.COVERAGE_THRESHOLD},
            "mutation_score": {"value": mutation, "threshold": self.MUTATION_THRESHOLD, "passed": mutation >= self.MUTATION_THRESHOLD},
            "failure_detection": {"value": failure_detection, "threshold": self.FAILURE_DETECTION_THRESHOLD, "passed": failure_detection >= self.FAILURE_DETECTION_THRESHOLD},
        }
        results["all_passed"] = all(r["passed"] for r in results.values())
        return results
