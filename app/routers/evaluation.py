from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.negocio.evaluation.evaluation_service import EvaluationService
from app.negocio.prompts.prompts_service import PromptsService


class EvaluationRunRequest(BaseModel):
    source_path: str
    test_code: str


class EvaluationResponse(BaseModel):
    evaluation_id: str
    coverage: float
    mutation_score: float
    failure_detection: float
    all_passed: bool
    details: dict


class ImprovementPromptRequest(BaseModel):
    original_prompt: str
    test_code: str
    evaluation_results: dict


class ImprovementPromptResponse(BaseModel):
    improvement_prompt: str


router = APIRouter(prefix="/api/v1/evaluation", tags=["evaluation"])
evaluation_service = EvaluationService()
prompts_service = PromptsService()
_evaluation_results: dict[str, dict] = {}
_evaluation_counter: int = 0


@router.post("/run", response_model=EvaluationResponse)
def run_evaluation(req: EvaluationRunRequest):
    global _evaluation_counter
    _evaluation_counter += 1
    eval_id = f"eval_{_evaluation_counter}"

    source_path = Path(req.source_path)
    try:
        coverage = evaluation_service.run_coverage(source_path, req.test_code)
        mutation = evaluation_service.run_mutation_score(source_path, req.test_code)
        failure = evaluation_service.run_failure_detection(source_path, req.test_code)
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Required tools (coverage, mutmut, pytest) not available")

    thresholds = evaluation_service.check_thresholds(coverage, mutation, failure)

    result = {
        "evaluation_id": eval_id,
        "coverage": coverage,
        "mutation_score": mutation,
        "failure_detection": failure,
        "all_passed": thresholds["all_passed"],
        "details": thresholds,
    }
    _evaluation_results[eval_id] = result

    return EvaluationResponse(**result)


@router.get("/{evaluation_id}", response_model=EvaluationResponse)
def get_evaluation(evaluation_id: str):
    result = _evaluation_results.get(evaluation_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return EvaluationResponse(**result)


@router.post("/improvement-prompt", response_model=ImprovementPromptResponse)
def generate_improvement_prompt(req: ImprovementPromptRequest):
    prompt = prompts_service.generate_improvement_prompt(
        req.original_prompt, req.test_code, req.evaluation_results
    )
    if not prompt:
        raise HTTPException(status_code=400, detail="No se requiere mejora, todas las métricas cumplen")
    return ImprovementPromptResponse(improvement_prompt=prompt)
