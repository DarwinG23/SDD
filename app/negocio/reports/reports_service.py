from datetime import datetime
from typing import Any


class ReportsService:
    def compile_report_data(
        self,
        evaluation_results: dict[str, Any],
        test_code: str,
        test_result: dict[str, Any] | None = None,
        improvement_cycles: int = 0,
    ) -> dict[str, Any]:
        details = evaluation_results.get("details", evaluation_results)
        return {
            "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "evaluation": details,
            "test_code": test_code,
            "test_result": test_result or {},
            "improvement_cycles": improvement_cycles,
            "summary": "passed" if evaluation_results.get("all_passed") else "failed",
        }
