from typing import Any


class PromptsService:
    def generate_improvement_prompt(
        self,
        original_prompt: str,
        test_code: str,
        evaluation_results: dict[str, Any],
    ) -> str:
        failed_metrics = []
        for metric, data in evaluation_results.items():
            if metric == "all_passed":
                continue
            if not data["passed"]:
                failed_metrics.append(
                    f"- {metric}: {data['value']:.1f}% (threshold: {data['threshold']}%)"
                )

        if not failed_metrics:
            return ""

        prompt_parts = [
            "Se requiere mejorar las pruebas unitarias generadas. Las siguientes métricas no alcanzaron los umbrales mínimos:\n",
            "\n".join(failed_metrics),
            f"\n\nPruebas actuales:\n```python\n{test_code}\n```",
            "\n\nGenera una versión mejorada de las pruebas que cumpla con todos los umbrales de calidad.",
        ]
        return "\n".join(prompt_parts)
