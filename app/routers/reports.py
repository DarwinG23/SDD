import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from app.negocio.reports.reports_service import ReportsService
from app.negocio.reports.pdf_generator import PDFGenerator
from app.negocio.prompts.prompts_service import PromptsService


logger = logging.getLogger(__name__)
REPORTS_DIR = Path("/tmp/smartunittest/uploads/reports")


class ReportGenerateRequest(BaseModel):
    evaluation_results: dict
    test_code: str = ""
    test_result: dict | None = None
    original_prompt: str = ""
    improvement_cycles: int = 0


class ReportGenerateResponse(BaseModel):
    report_id: str
    status: str


router = APIRouter(prefix="/api/v1/reports", tags=["reports"])
reports_service = ReportsService()
pdf_generator = PDFGenerator()
prompts_service = PromptsService()
_report_counter: int = 0


@router.post("/generate", response_model=ReportGenerateResponse)
def generate_report(req: ReportGenerateRequest):
    global _report_counter
    _report_counter += 1
    report_id = f"report_{_report_counter}"

    report_data = reports_service.compile_report_data(
        req.evaluation_results, req.test_code, req.test_result, req.improvement_cycles
    )

    improvement_prompt = ""
    if not req.evaluation_results.get("all_passed"):
        try:
            improvement_prompt = prompts_service.generate_improvement_prompt(
                req.original_prompt, req.test_code, req.evaluation_results.get("details", req.evaluation_results)
            )
            logger.info("Improvement prompt generated (%d chars)", len(improvement_prompt))
        except Exception as e:
            logger.warning("Error generating improvement prompt: %s", e)
    report_data["improvement_prompt"] = improvement_prompt

    pdf_bytes = pdf_generator.generate_report(report_data)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{report_id}.pdf"
    report_path.write_bytes(pdf_bytes)

    return ReportGenerateResponse(report_id=report_id, status="generated")


@router.get("/{report_id}/download")
def download_report(report_id: str):
    report_path = REPORTS_DIR / f"{report_id}.pdf"
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    pdf_bytes = report_path.read_bytes()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={report_id}.pdf"},
    )
