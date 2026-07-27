import pytest
from app.negocio.evaluation.evaluation_service import EvaluationService


@pytest.fixture
def evaluator():
    return EvaluationService()


class TestEvaluationService:

    def test_check_thresholds_all_pass(self, evaluator):
        result = evaluator.check_thresholds(85.0, 75.0, 65.0)
        assert result["all_passed"] is True
        assert result["coverage"]["passed"] is True
        assert result["mutation_score"]["passed"] is True
        assert result["failure_detection"]["passed"] is True

    def test_check_thresholds_coverage_fails(self, evaluator):
        result = evaluator.check_thresholds(70.0, 75.0, 65.0)
        assert result["all_passed"] is False
        assert result["coverage"]["passed"] is False
        assert result["coverage"]["value"] == 70.0

    def test_check_thresholds_mutation_fails(self, evaluator):
        result = evaluator.check_thresholds(85.0, 60.0, 65.0)
        assert result["all_passed"] is False
        assert result["mutation_score"]["passed"] is False

    def test_check_thresholds_failure_detection_fails(self, evaluator):
        result = evaluator.check_thresholds(85.0, 75.0, 50.0)
        assert result["all_passed"] is False
        assert result["failure_detection"]["passed"] is False

    def test_check_thresholds_all_fail(self, evaluator):
        result = evaluator.check_thresholds(50.0, 50.0, 50.0)
        assert result["all_passed"] is False
        for metric in ["coverage", "mutation_score", "failure_detection"]:
            assert result[metric]["passed"] is False

    def test_threshold_boundaries(self, evaluator):
        at_threshold = evaluator.check_thresholds(80.0, 70.0, 60.0)
        assert at_threshold["all_passed"] is True
        just_below = evaluator.check_thresholds(79.99, 69.99, 59.99)
        assert just_below["all_passed"] is False

    def test_mutate_function_changes_return(self, evaluator):
        source = "def foo():\n    return True\n"
        mutated = evaluator._mutate_function(source, "foo")
        assert "False" in mutated
        assert "True" not in mutated

    def test_mutate_function_unchanged_if_no_return(self, evaluator):
        source = "def foo():\n    pass\n"
        mutated = evaluator._mutate_function(source, "foo")
        assert mutated.strip() == source.strip()
