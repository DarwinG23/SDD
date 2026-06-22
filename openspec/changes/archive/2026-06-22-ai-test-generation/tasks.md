## 1. Backend — Servicio de IA

- [x] 1.1 Crear `app/services/ai_service.py` con función `generate_tests(prompt: str, code: str) -> str` usando Ollama (Qwen 2.5 Coder 7B)
- [x] 1.2 Implementar llamada a Ollama API (`/api/generate`) con httpx, system prompt especializado en pytest
- [x] 1.3 Implementar extracción de bloque de código Python de la respuesta
- [x] 1.4 Agregar manejo de errores: conexión rechazada, timeout, error de Ollama

## 2. Backend — Router de IA

- [x] 2.1 Crear `app/routers/ai.py` con endpoint `POST /api/v1/ai/generate-tests` que recibe `session_id` y `prompt`
- [x] 2.2 Integrar `ai_service.generate_tests()` en el endpoint
- [x] 2.3 Registrar `ai.router` en `app/main.py`

## 3. Backend — Configuración

- [x] 3.1 Agregar `httpx` a `requirements.txt` (ya estaba), remover `openai`
- [x] 3.2 Crear archivo `.env` con `OLLAMA_URL=http://localhost:11434`
- [x] 3.3 Limpiar variables de OpenAI en `app/main.py`

## 4. Frontend — Conectar botón Generar pruebas

- [x] 4.1 Reemplazar placeholder del botón "Generar pruebas unitarias" con llamada real a `POST /api/v1/ai/generate-tests`
- [x] 4.2 Agregar estado de carga indeterminado en el overlay durante la generación
- [x] 4.3 Agregar visor de código (`<pre><code>`) en overlay success para mostrar pruebas generadas
- [x] 4.4 Implementar botón "Copiar" al portapapeles
- [x] 4.5 Manejar errores: mostrar mensaje y botón "Reintentar"

## 5. Tests — Pruebas unitarias

- [x] 5.1 Actualizar tests para `ai_service.py` (mock de httpx/Ollama en lugar de OpenAI)
- [x] 5.2 Actualizar tests para endpoint `POST /api/v1/ai/generate-tests`
- [x] 5.3 Verificar que los tests existentes continúan pasando (20/20)
