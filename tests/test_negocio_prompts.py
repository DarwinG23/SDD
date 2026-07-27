import pytest
from app.negocio.prompts.prompts_service import PromptsService


@pytest.fixture
def prompts_service():
    return PromptsService()


class TestPromptsService:

    def test_generate_improvement_prompt_with_failures(self, prompts_service):
        evaluation_results = {
            "coverage": {"value": 50.0, "threshold": 80.0, "passed": False},
            "mutation_score": {"value": 75.0, "threshold": 70.0, "passed": True},
            "failure_detection": {"value": 60.0, "threshold": 60.0, "passed": True},
            "all_passed": False,
        }
        prompt = prompts_service.generate_improvement_prompt("original", "def test(): pass", evaluation_results)
        assert "coverage" in prompt.lower() or "50.0" in prompt
        assert "mutation" not in prompt.lower()

    def test_generate_improvement_prompt_all_pass(self, prompts_service):
        evaluation_results = {
            "coverage": {"value": 90.0, "threshold": 80.0, "passed": True},
            "mutation_score": {"value": 85.0, "threshold": 70.0, "passed": True},
            "failure_detection": {"value": 90.0, "threshold": 60.0, "passed": True},
            "all_passed": True,
        }
        prompt = prompts_service.generate_improvement_prompt("original", "def test(): pass", evaluation_results)
        assert prompt == ""

    def test_generate_improvement_prompt_includes_test_code(self, prompts_service):
        evaluation_results = {
            "coverage": {"value": 50.0, "threshold": 80.0, "passed": False},
            "mutation_score": {"value": 75.0, "threshold": 70.0, "passed": True},
            "failure_detection": {"value": 65.0, "threshold": 60.0, "passed": True},
            "all_passed": False,
        }
        prompt = prompts_service.generate_improvement_prompt("original", "def test_foo(): pass", evaluation_results)
        assert "test_foo" in prompt
