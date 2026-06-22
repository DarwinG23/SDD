import os
import re

import httpx


class AIService:
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = "qwen2.5-coder:7b"
    SYSTEM_PROMPT = (
        "Eres un experto en generación de pruebas unitarias en Python con pytest. "
        "Genera solo el código de las pruebas, sin explicaciones ni markdown. "
        "Las pruebas deben usar pytest y cubrir casos normales, bordes y de error. "
        "Incluye docstrings descriptivos en cada función de prueba."
    )

    def _build_user_message(self, prompt: str, code: str) -> str:
        return (
            f"Contexto y requerimientos:\n{prompt}\n\n"
            f"Código fuente a probar:\n```python\n{code}\n```"
        )

    def _extract_code_block(self, response_text: str) -> str:
        match = re.search(r"```(?:python)?\s*\n(.*?)```", response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response_text.strip()

    def generate_tests(self, prompt: str, code: str) -> str:
        full_prompt = f"{self.SYSTEM_PROMPT}\n\n{self._build_user_message(prompt, code)}"
        try:
            with httpx.Client(timeout=120) as client:
                response = client.post(
                    f"{self.OLLAMA_URL}/api/generate",
                    json={
                        "model": self.OLLAMA_MODEL,
                        "prompt": full_prompt,
                        "stream": False,
                        "options": {"temperature": 0.3, "num_predict": 2000},
                    },
                )
                response.raise_for_status()
                data = response.json()
                raw = data.get("response", "")
                return self._extract_code_block(raw)
        except httpx.ConnectError:
            raise ValueError(
                f"No se pudo conectar a Ollama en {self.OLLAMA_URL}. "
                "Asegúrate de que Ollama esté ejecutándose."
            )
        except httpx.TimeoutException:
            raise ValueError("La generación con Ollama excedió el tiempo de espera (120s).")
