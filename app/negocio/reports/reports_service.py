from datetime import datetime
from typing import Any


class ReportsService:
    def compile_report_data(
        self,
        evaluation_results: dict[str, Any],
        test_code: str,
        improvement_cycles: int = 0,
    ) -> dict[str, Any]:
        return {
            "generated_at": datetime.now().isoformat(),
            "evaluation": evaluation_results,
            "test_code": test_code,
            "improvement_cycles": improvement_cycles,
            "summary": "passed" if evaluation_results.get("all_passed") else "failed",
        }
