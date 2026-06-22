## Why

El campo de prompt estructurado actual es un textarea libre sin guía, lo que permite entradas inconsistentes que no garantizan las secciones requeridas (contexto, código, pruebas) para la generación de tests unitarios con IA. Se necesita un formulario fijo que estructure la entrada y evite errores del usuario.

## What Changes

- Reemplazar el textarea libre de prompt por un formulario con secciones fijas: Contexto, Código, Pruebas.
- El nombre del proyecto se auto-detecta desde el nombre del archivo `.py` subido, en un campo editable.
- El frontend combina las secciones en un solo prompt estructurado antes de enviarlo al backend.
- No hay cambios en el backend (upload.py permanece igual, recibe `prompt` y `project_name` como antes).

## Capabilities

### New Capabilities
- `structured-prompt-input`: Formulario estructurado con secciones fijas (Contexto, Código, Pruebas) para la entrada del prompt de generación de tests.

### Modified Capabilities
<!-- No existing specs to modify -->

## Impact

- `app/templates/upload.html`: Reemplazar textarea por campos estructurados.
- `app/static/js/upload.js`: Construir prompt combinado desde las secciones + auto-detectar nombre desde archivo.
- `app/static/css/style.css`: Estilos para los nuevos campos del formulario.
- Sin cambios en backend, validación, tests, ni lógica de negocio.

## Non-goals

- No se modifica la generación de tests por IA ni los reportes PDF.
- No se modifica la validación de sintaxis Python ni la ejecución de pruebas.
- No se tocan los endpoints del backend ni la lógica de negocio.
- No se agregan nuevos endpoints ni campos al modelo de datos.
