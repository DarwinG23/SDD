## Context

Actualmente el sistema valida código fuente y muestra un overlay con botón "Generar pruebas unitarias" que no hace nada. No existe conexión con OpenAI ni endpoint de generación. El contrato de API especifica `POST /api/v1/ai/generate-tests` pero no está implementado.

## Goals / Non-Goals

**Goals:**
- Crear servicio `ai_service.py` que consuma OpenAI GPT-4 y genere pruebas pytest
- Crear endpoint `POST /api/v1/ai/generate-tests` que reciba `session_id` y retorne `test_code`
- Conectar el botón "Generar pruebas unitarias" del overlay al endpoint
- Mostrar pruebas generadas en visor de código con opción de copiar
- Configurar API Key vía `.env`

**Non-Goals:**
- No se ejecuta pytest
- No se implementa evaluación de métricas
- No hay regeneración con improvement-prompt

## Decisions

### D1: Servicio OpenAI separado

Se crea `app/services/ai_service.py` con función `generate_tests(session_id: str) -> str` que:
1. Lee el prompt desde el archivo de sesión o lo recibe como parámetro
2. Construye el mensaje para GPT-4 con system prompt especializado en pytest
3. Llama a OpenAI API vía `openai` Python SDK
4. Extrae el bloque de código Python de la respuesta
5. Retorna el string con las pruebas generadas

**Alternativa considerada:** Integrar la llamada directamente en el router. Se descartó por separación de responsabilidades.

### D2: El endpoint recibe session_id en lugar de código/prompt

El frontend envía `session_id` al endpoint. El backend usa `file_storage.get_file_path(session_id)` para leer el código fuente y recupera el prompt de la sesión. Esto evita enviar código grande en el body de la request.

**Alternativa considerada:** Enviar código y prompt en el body. Se descartó porque el archivo ya está almacenado en el servidor.

### D3: Visor de código en el overlay success

Se agrega una sección oculta en el overlay success con un `<pre><code>` para mostrar las pruebas. Cuando el endpoint responde, se oculta el spinner y se muestra el código. Se agrega un botón "Copiar" que usa `navigator.clipboard.writeText()`.

### D4: Manejo de errores

Si OpenAI falla o la API key no está configurada, el overlay muestra el error y un botón "Reintentar" que vuelve a llamar al endpoint.

## Risks / Trade-offs

- **[Riesgo] La API de OpenAI puede ser lenta (5-30 segundos)**: mitigado con overlay de carga indeterminado y timeout de 60 segundos en el servidor.
- **[Riesgo] La API Key puede estar ausente o ser inválida**: mitigado con validación al iniciar y error claro al usuario.
- **[Riesgo] OpenAI puede generar código con sintaxis inválida**: el usuario recibe el código generado; la validación de sintaxis ocurre al ejecutar (fuera de este cambio).
- **[Trade-off] Almacenar el prompt en la sesión** vs enviarlo en cada request: se almacena en la sesión para no depender del frontend, pero requiere que la sesión exista.
