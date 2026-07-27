import pytest
from app.negocio.reports.reports_service import ReportsService


@pytest.fixture
def reports_service():
    return ReportsService()


class TestReportsService:

    def test_compile_report_data_passed(self, reports_service):
        evaluation_results = {
            "coverage": {"value": 90.0, "threshold": 80.0, "passed": True},
            "mutation_score": {"value": 85.0, "threshold": 70.0, "passed": True},
            "failure_detection": {"value": 90.0, "threshold": 60.0, "passed": True},
            "all_passed": True,
        }
        report = reports_service.compile_report_data(evaluation_results, "def test(): pass")
        assert report["summary"] == "passed"
        assert "generated_at" in report
        assert report["evaluation"]["all_passed"] is True

    def test_compile_report_data_failed(self, reports_service):
        evaluation_results = {
            "coverage": {"value": 50.0, "threshold": 80.0, "passed": False},
            "mutation_score": {"value": 85.0, "threshold": 70.0, "passed": True},
            "failure_detection": {"value": 90.0, "threshold": 60.0, "passed": True},
            "all_passed": False,
        }
        report = reports_service.compile_report_data(evaluation_results, "def test(): pass")
        assert report["summary"] == "failed"

    def test_compile_report_with_improvement_cycles(self, reports_service):
        evaluation_results = {"all_passed": True}
        report = reports_service.compile_report_data(evaluation_results, "", improvement_cycles=2)
        assert report["improvement_cycles"] == 2
