## Why

Actualmente al hacer clic en "Subir y validar" solo aparece un mensaje de texto debajo del formulario, sin indicación visual de proceso ni diferenciación clara entre éxito y error. El usuario necesita una experiencia de carga con overlay, retroalimentación visual inmediata y acciones claras después de la validación.

## What Changes

- Agregar overlay de carga a pantalla completa mientras se valida el código
- Si la validación es exitosa: overlay muestra mensaje verde "validado" con botón "Generar pruebas unitarias" (placeholder, sin acción real)
- Si la validación falla: overlay muestra error en rojo con botón "Volver a subir" que reinicia el formulario
- No se implementa la generación de pruebas aún — solo la UI hasta el botón

## Capabilities

### New Capabilities
- `validation-process-ui`: Interfaz de overlay de carga, resultado de validación con acciones (Generar pruebas / Volver a subir)

### Modified Capabilities
- `structured-prompt-input`: El formulario estructurado existente se modifica para integrarse con el nuevo overlay de resultado

## Impact

- `app/templates/upload.html`: Agregar HTML del overlay con secciones para carga, éxito y error
- `app/static/js/upload.js`: Reemplazar lógica de resultado actual por flujo con overlay
- `app/static/css/style.css`: Estilos para overlay, animaciones de carga, botones de acción
- Sin cambios en backend — solo frontend

## Non-goals

- No se implementa el endpoint de generación de pruebas (`POST /api/v1/ai/generate-tests`)
- No se ejecutan pruebas (pytest) ni evaluación de métricas
- No se generan reportes PDF
- No hay cambios en la lógica del servidor
