import io
from datetime import datetime
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors


class PDFGenerator:
    def generate_report(self, report_data: dict[str, Any]) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        title_style = ParagraphStyle("Title2", parent=styles["Title"], fontSize=18, spaceAfter=20)
        heading_style = ParagraphStyle("Heading2", parent=styles["Heading2"], fontSize=14, spaceAfter=10)
        normal_style = styles["Normal"]

        elements.append(Paragraph("SmartUnitTest - Reporte de Evaluación", title_style))
        elements.append(Paragraph(f"Generado: {report_data.get('generated_at', datetime.now().isoformat())}", normal_style))
        elements.append(Spacer(1, 10 * mm))

        evaluation = report_data.get("evaluation", {})
        elements.append(Paragraph("Métricas de Calidad", heading_style))

        table_data = [["Métrica", "Valor", "Umbral", "Estado"]]
        for metric in ["coverage", "mutation_score", "failure_detection"]:
            data = evaluation.get(metric, {})
            table_data.append([
                metric.replace("_", " ").title(),
                f"{data.get('value', 0):.1f}%",
                f"{data.get('threshold', 0):.0f}%",
                "✓ Cumple" if data.get("passed") else "✗ No cumple",
            ])

        table = Table(table_data, colWidths=[120, 80, 80, 100])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 5 * mm))

        summary = report_data.get("summary", "unknown")
        result_text = "RESULTADO: PRUEBAS APROBADAS" if summary == "passed" else "RESULTADO: PRUEBAS NO APROBADAS - SE REQUIERE MEJORA"
        result_style = ParagraphStyle(
            "Result", parent=normal_style,
            fontSize=12, spaceAfter=10,
            textColor=colors.green if summary == "passed" else colors.red,
            backColor=colors.HexColor("#F0FDF4") if summary == "passed" else colors.HexColor("#FEF2F2"),
        )
        elements.append(Paragraph(result_text, result_style))

        if report_data.get("improvement_cycles", 0) > 0:
            elements.append(Spacer(1, 5 * mm))
            elements.append(Paragraph(f"Ciclos de mejora ejecutados: {report_data['improvement_cycles']}", normal_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
