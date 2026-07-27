from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from app.negocio.reports.reports_service import ReportsService
from app.negocio.reports.pdf_generator import PDFGenerator


class ReportGenerateRequest(BaseModel):
    evaluation_results: dict
    test_code: str = ""
    test_result: dict | None = None
    improvement_cycles: int = 0


class ReportGenerateResponse(BaseModel):
    report_id: str
    status: str


router = APIRouter(prefix="/api/v1/reports", tags=["reports"])
reports_service = ReportsService()
pdf_generator = PDFGenerator()
_generated_reports: dict[str, dict] = {}
_report_counter: int = 0


@router.post("/generate", response_model=ReportGenerateResponse)
def generate_report(req: ReportGenerateRequest):
    global _report_counter
    _report_counter += 1
    report_id = f"report_{_report_counter}"

    report_data = reports_service.compile_report_data(
        req.evaluation_results, req.test_code, req.test_result, req.improvement_cycles
    )
    pdf_bytes = pdf_generator.generate_report(report_data)

    _generated_reports[report_id] = {
        "data": report_data,
        "pdf_bytes": pdf_bytes,
    }

    return ReportGenerateResponse(report_id=report_id, status="generated")


@router.get("/{report_id}/download")
def download_report(report_id: str):
    report = _generated_reports.get(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    pdf_bytes = report["pdf_bytes"]
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={report_id}.pdf"},
    )
