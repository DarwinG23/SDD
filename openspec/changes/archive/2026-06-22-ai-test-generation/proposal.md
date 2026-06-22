## Why

Actualmente el sistema solo valida código fuente pero no genera las pruebas unitarias. El botón "Generar pruebas unitarias" en el overlay es un placeholder sin funcionalidad. Se necesita implementar el endpoint de IA que consuma OpenAI y devuelva las pruebas generadas, y conectarlo con la interfaz para mostrar el resultado.

## What Changes

- Crear endpoint `POST /api/v1/ai/generate-tests` que reciba el prompt estructurado y el código fuente, invoque OpenAI GPT-4, y devuelva las pruebas generadas
- Crear servicio `app/services/ai_service.py` para la comunicación con OpenAI API
- Crear router `app/routers/ai.py` con el endpoint de generación
- Configurar API Key vía variable de entorno en archivo `.env`
- Conectar botón "Generar pruebas unitarias" en el overlay de validación para llamar al endpoint
- Agregar overlay de carga indeterminado durante la generación
- Mostrar las pruebas generadas en un visor de código en la interfaz

## Capabilities

### New Capabilities
- `ai-test-generation`: Endpoint de generación de pruebas unitarias mediante OpenAI API, con visualización en frontend

### Modified Capabilities
- `validation-process-ui`: El overlay de validación exitosa ahora tiene el botón "Generar pruebas unitarias" funcional, conectado al nuevo endpoint

## Impact

- `app/routers/ai.py`: Nuevo router con endpoint `POST /api/v1/ai/generate-tests`
- `app/services/ai_service.py`: Nuevo servicio para llamar a OpenAI API
- `app/main.py`: Incluir nuevo router `ai.router`
- `.env`: Agregar variable `OPENAI_API_KEY`
- `app/templates/upload.html`: Agregar sección de visor de código en el overlay success
- `app/static/js/upload.js`: Reemplazar placeholder del botón con llamada real al endpoint y mostrar resultado
- `app/static/css/style.css`: Estilos para visor de código y overlay de generación

## Non-goals

- No se ejecuta pytest
- No se implementa evaluación de métricas (cobertura, mutación, detección)
- No se implementa la regeneración de pruebas (improvement-prompt)
- No se generan reportes PDF
