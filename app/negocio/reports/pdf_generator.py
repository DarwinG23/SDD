import io
from datetime import datetime
from typing import Any

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


class PDFGenerator:
    METRIC_LABELS = {
        "coverage": "Cobertura",
        "mutation_score": "Mutation Score",
        "failure_detection": "Detección de Fallos",
    }

    METRIC_COLORS = {
        "coverage": colors.HexColor("#3B82F6"),
        "mutation_score": colors.HexColor("#F59E0B"),
        "failure_detection": colors.HexColor("#10B981"),
    }

    def _build_metrics_chart(self, evaluation: dict[str, Any]) -> Drawing:
        labels: list[str] = []
        values: list[float] = []
        thresholds: list[float] = []
        for metric in ["coverage", "mutation_score", "failure_detection"]:
            data = evaluation.get(metric, {})
            labels.append(self.METRIC_LABELS.get(metric, metric))
            values.append(data.get("value", 0))
            thresholds.append(data.get("threshold", 0))

        drawing = Drawing(460, 180)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 40
        bc.height = 110
        bc.width = 380
        bc.data = [values, thresholds]
        bc.categoryAxis.categoryNames = labels
        bc.categoryAxis.labels.fontSize = 8
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 20
        bc.valueAxis.labels.fontSize = 8
        bc.bars[0].fillColor = colors.HexColor("#3B82F6")
        bc.bars[1].fillColor = colors.HexColor("#94A3B8")
        bc.groupSpacing = 25
        bc.barSpacing = 4
        drawing.add(bc)

        from reportlab.graphics.widgets.markers import makeMarker
        drawing.add(
            ParagraphStyle("legend", fontSize=7)
        )
        return drawing

    def _build_metrics_table(self, evaluation: dict[str, Any]) -> Table:
        table_data = [["Métrica", "Valor", "Umbral", "Estado"]]
        for metric in ["coverage", "mutation_score", "failure_detection"]:
            data = evaluation.get(metric, {})
            passed = data.get("passed", False)
            table_data.append([
                self.METRIC_LABELS.get(metric, metric),
                f"{data.get('value', 0):.1f}%",
                f"{data.get('threshold', 0):.0f}%",
                "✓ Cumple" if passed else "✗ No cumple",
            ])

        t = Table(table_data, colWidths=[140, 80, 80, 100])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E40AF")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return t

    def generate_report(self, report_data: dict[str, Any]) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm)
        styles = getSampleStyleSheet()
        elements: list = []

        title_style = ParagraphStyle("Title2", parent=styles["Title"], fontSize=20, spaceAfter=4, textColor=colors.HexColor("#1E3A5F"))
        subtitle_style = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=9, textColor=colors.HexColor("#64748B"), spaceAfter=16)
        heading_style = ParagraphStyle("Heading2", parent=styles["Heading2"], fontSize=14, spaceAfter=10, textColor=colors.HexColor("#1E3A5F"))
        normal_style = styles["Normal"]
        mono_style = ParagraphStyle("Mono", parent=styles["Code"], fontSize=7, leading=9, spaceAfter=6)

        elements.append(Paragraph("SmartUnitTest", title_style))
        elements.append(Paragraph("Reporte de Evaluación de Pruebas Unitarias", subtitle_style))
        elements.append(Paragraph(
            f"<b>Generado:</b> {report_data.get('generated_at', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))}",
            normal_style
        ))
        elements.append(Spacer(1, 8 * mm))

        test_result = report_data.get("test_result", {})
        if test_result:
            elements.append(Paragraph("Resultados de Ejecución", heading_style))
            passed = test_result.get("passed", 0)
            failed = test_result.get("failed", 0)
            total = passed + failed
            color = colors.HexColor("#16A34A") if failed == 0 else colors.HexColor("#DC2626")
            status_text = "Todas las pruebas pasaron" if failed == 0 else f"Pruebas fallaron"
            elements.append(Paragraph(
                f'<font color="{color.hexval()}"><b>{status_text}</b></font>  |  '
                f"Pasaron: {passed}  |  Fallaron: {failed}  |  Total: {total}",
                normal_style
            ))
            stdout = test_result.get("stdout", "")
            if stdout:
                elements.append(Spacer(1, 3 * mm))
                elements.append(Paragraph("<b>Salida estándar:</b>", normal_style))
                elements.append(Paragraph(stdout.replace("\n", "<br/>"), mono_style))
            elements.append(Spacer(1, 6 * mm))

        elements.append(Paragraph("Métricas de Calidad", heading_style))
        evaluation = report_data.get("evaluation", {})
        elements.append(self._build_metrics_table(evaluation))
        elements.append(Spacer(1, 4 * mm))
        try:
            chart = self._build_metrics_chart(evaluation)
            elements.append(chart)
        except Exception:
            pass
        elements.append(Spacer(1, 6 * mm))

        summary = report_data.get("summary", "unknown")
        all_passed = summary == "passed"
        result_color = colors.HexColor("#16A34A") if all_passed else colors.HexColor("#DC2626")
        result_bg = colors.HexColor("#F0FDF4") if all_passed else colors.HexColor("#FEF2F2")
        result_text = (
            "RESULTADO FINAL: TODAS LAS MÉTRICAS CUMPLEN"
            if all_passed
            else "RESULTADO FINAL: ALGUNAS MÉTRICAS NO CUMPLEN - SE REQUIERE MEJORA"
        )
        result_style = ParagraphStyle(
            "Result", parent=normal_style,
            fontSize=12, spaceAfter=10, spaceBefore=6,
            textColor=result_color,
            backColor=result_bg,
            borderPadding=8,
        )
        elements.append(Paragraph(result_text, result_style))

        if report_data.get("improvement_cycles", 0) > 0:
            elements.append(Spacer(1, 4 * mm))
            elements.append(Paragraph(
                f"Ciclos de mejora ejecutados: {report_data['improvement_cycles']}",
                normal_style
            ))

        improvement_prompt = report_data.get("improvement_prompt", "")
        if improvement_prompt:
            elements.append(Spacer(1, 6 * mm))
            elements.append(Paragraph("Sugerencia de Prompt de Mejora", heading_style))
            elements.append(Paragraph(
                "Las siguientes métricas no alcanzaron los umbrales. "
                "Se generó automáticamente un prompt optimizado para la siguiente iteración:",
                normal_style
            ))
            elements.append(Spacer(1, 2 * mm))
            prompt_style = ParagraphStyle(
                "ImproveMono", parent=styles["Code"],
                fontSize=7.5, leading=10, spaceAfter=6,
                backColor=colors.HexColor("#F1F5F9"),
                borderPadding=8,
            )
            elements.append(Paragraph(
                improvement_prompt.replace("\n", "<br/>"),
                prompt_style
            ))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
