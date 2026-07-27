import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class PromptsService:
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = "qwen2.5-coder:7b"
    SYSTEM_PROMPT = (
        "Eres un experto en mejora de prompts para generación de pruebas unitarias. "
        "Dado el prompt original, las pruebas generadas y las métricas de evaluación, "
        "genera un nuevo prompt optimizado que ayude a la IA a generar mejores pruebas. "
        "El prompt debe incluir tres secciones: Contexto, Código y Pruebas.\n"
        "- Contexto: describe el propósito general del sistema.\n"
        "- Código: describe las FUNCIONALIDADES a probar (NO incluyas código fuente literal).\n"
        "- Pruebas: describe los casos de prueba esperados.\n"
        "Sugiere mejoras concretas basadas en las métricas que fallaron. "
        "Responde SOLO con el nuevo prompt, sin explicaciones adicionales."
    )

    def generate_improvement_prompt(
        self,
        original_prompt: str,
        test_code: str,
        evaluation_results: dict[str, Any],
    ) -> str:
        failed_metrics = []
        for metric, data in evaluation_results.items():
            if isinstance(data, dict) and not data.get("passed", True):
                failed_metrics.append(
                    f"- {metric}: {data.get('value', 0):.1f}% (umbral: {data.get('threshold', 0)}%)"
                )

        if not failed_metrics:
            return ""

        prompt_section = f"Prompt original:\n{original_prompt}\n\n" if original_prompt else ""
        user_message = (
            f"{prompt_section}"
            f"Pruebas generadas:\n```python\n{test_code}\n```\n\n"
            f"Métricas que no cumplen:\n" + "\n".join(failed_metrics) + "\n\n"
            "Genera un prompt de mejora con las secciones Contexto, Código (descripción de funcionalidades, NO código fuente) y Pruebas."
        )

        try:
            with httpx.Client(timeout=120) as client:
                response = client.post(
                    f"{self.OLLAMA_URL}/api/generate",
                    json={
                        "model": self.OLLAMA_MODEL,
                        "prompt": f"{self.SYSTEM_PROMPT}\n\n{user_message}",
                        "stream": False,
                        "options": {"temperature": 0.5, "num_predict": 1500},
                    },
                )
                response.raise_for_status()
                return response.json().get("response", "").strip()
        except Exception as e:
            logger.warning("Error calling Ollama for improvement prompt: %s", e)
            return self._fallback_prompt(original_prompt, failed_metrics)

    @staticmethod
    def _fallback_prompt(original_prompt: str, failed_metrics: list[str]) -> str:
        return (
            f"Prompt de mejora sugerido:\n\n"
            f"Basado en el análisis, las siguientes métricas no alcanzaron los umbrales:\n"
            + "\n".join(failed_metrics) +
            f"\n\nPrompt original:\n{original_prompt}\n\n"
            "Revisa y ajusta el contexto, la descripción del código y los casos de prueba "
            "para enfocarte en las áreas que necesitan mejorar."
        )
