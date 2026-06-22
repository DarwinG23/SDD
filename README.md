# SmartUnitTest CON SDD

Proyecto para generar y validar pruebas unitarias automáticamente a partir de código fuente. Usa FastAPI para exponer endpoints de subida, validación y limpieza de sesiones, y un servicio que puede invocar un modelo de lenguaje para generar tests.

## Características
- Subida de código fuente vía `POST /api/v1/upload/source` (multipart/form-data).
- Validación de sintaxis Python y respuesta estructurada con errores.
- Limpieza de sesiones con `DELETE /api/v1/upload/source/{session_id}`.
- Integración opcional con un servicio de IA (OpenAI) para generación automática de tests.

## Requisitos
- Python 3.11+ (probado con 3.12)
- Virtualenv o entorno equivalente
- Dependencias en `requirements.txt`

## Instalación
1. Crear y activar un virtualenv:

```bash
python -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno: crea un fichero `.env` en la raíz con la clave esperada `OPENAI_API_KEY` si vas a usar la integración IA. No subas este fichero al repositorio.

```text
OPENAI_API_KEY=sk-...
```

## Ejecutar la aplicación
Arrancar con Uvicorn (desde la raíz del proyecto):

```bash
./venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La documentación interactiva estará en `http://localhost:8000/docs` y la especificación OpenAPI en `http://localhost:8000/openapi.json`.

## Endpoints principales
- `POST /api/v1/upload/source` — Subir fichero fuente (multipart): campos `file`, `project_name`, `prompt`.
	- Respuestas principales:
		- `200` — `{"valid": true, "uploadId": ..., "projectName": ...}`
		- `422` — `{"valid": false, "errors": [...]}` (errores de sintaxis)
		- `400` — validación/extension no permitida
- `DELETE /api/v1/upload/source/{session_id}` — Limpia los ficheros temporales de la sesión. Retorna `{"message": "Session cleaned up"}`.
- `GET /api/v1/upload/page` — Página HTML de subida (no incluida en el schema OpenAPI).

Vea la implementación en `app/routers/upload.py`.

## Uso (ejemplos curl)
Subir un archivo de ejemplo:

```bash
curl -v -F "file=@/ruta/a/test.py" -F "project_name=MiProyecto" -F "prompt=contexto" \
	http://localhost:8000/api/v1/upload/source
```

Limpiar una sesión:

```bash
curl -X DELETE http://localhost:8000/api/v1/upload/source/<SESSION_ID>
```

## Tests y cobertura
Ejecutar tests con el entorno del proyecto:

```bash
./venv/bin/pytest -q
./venv/bin/coverage run -m pytest -q && ./venv/bin/coverage report -m
```

## Configuración de la IA
El servicio de generación de tests usa la variable `OPENAI_API_KEY` y el cliente de OpenAI en `app/services/ai_service.py`. Si recibes `model_not_found` ajusta el nombre del modelo usado (`gpt-4` por defecto en el código) a uno disponible para tu cuenta.

No incluyas claves en repositorios públicos; revoca y rota la clave si fue expuesta.

## Estructura relevante
- `app/main.py` — arranque, carga de `.env`, registro de routers.
- `app/routers/upload.py` — endpoints de subida y limpieza.
- `app/services/file_storage.py` — almacenamiento temporal y limpieza.
- `app/services/validation.py` — validación de sintaxis Python.
- `app/services/ai_service.py` — integración con OpenAI para generación de tests.

## Contribuir
Pull requests bienvenidas. Para cambios grandes, abre un issue o discute el diseño primero.

## Licencia
MIT (ajusta según necesites)
