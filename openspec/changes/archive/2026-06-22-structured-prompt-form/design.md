## Context

El formulario actual de carga de código fuente tiene un textarea libre para el prompt estructurado, sin guía ni validación de estructura. El usuario debe ingresar manualmente las secciones "Contexto", "Código" y "Pruebas" sin formato predefinido. Además, el nombre del proyecto se ingresa manualmente sin relación con el archivo subido.

El backend espera los campos `prompt` (string) y `project_name` (string) en el POST a `/api/v1/upload/source`. No se deben modificar endpoints ni la lógica del servidor.

## Goals / Non-Goals

**Goals:**
- Reemplazar el textarea libre por tres áreas de texto fijas: Contexto, Código, Pruebas
- Auto-detectar el nombre del proyecto desde el nombre del archivo `.py` subido (campo editable)
- Combinar las secciones en un único prompt estructurado en el frontend antes del envío
- Mantener compatibilidad total con backend existente

**Non-Goals:**
- No se modifican endpoints del backend
- No se agregan nuevos campos al modelo de datos
- No se cambian los módulos de validación, IA, testing, evaluación o reportes
- No se modifica la lógica de almacenamiento de archivos

## Decisions

### D1: Tres textareas independientes en lugar de un solo textarea

Se reemplaza el `<textarea id="prompt">` por tres `<textarea>` individuales con ids `context`, `code` y `tests`, cada uno con su label y placeholder. Esto fuerza al usuario a llenar cada sección por separado, garantizando que todas las secciones requeridas estén presentes.

**Alternativa considerada:** Un solo textarea con placeholders internos. Se descartó porque no garantiza estructura y permite omisiones.

### D2: Combinación de campos en JavaScript

El JS de `upload.js` construye el prompt concatenando los valores de los tres textareas con el formato:
```
Contexto:
{context}

Código:
{code}

Pruebas:
{tests}
```
Este string se asigna al campo `prompt` del `FormData` que se envía al backend.

**Alternativa considerada:** Enviar tres campos separados y ensamblar en backend. Se descartó por la restricción de no modificar backend.

### D3: Auto-detección del nombre desde el file input

Se agrega un evento `change` al `<input type="file">` que lee `file.name`, remueve la extensión `.py` y asigna el resultado al campo `project-name`. El campo sigue siendo editable por el usuario.

### D4: Sin cambios en el backend

Para mantener la compatibilidad, `upload.py` y `file_storage.py` no se modifican. El backend recibe `prompt` y `project_name` exactamente como antes. El prompt combinado desde el frontend sigue el mismo formato que un usuario escribiría manualmente.

## Risks / Trade-offs

- **[Riesgo] El usuario podría desordenar el formato del prompt si edita manualmente el campo project-name**: aceptable porque el nombre del proyecto no afecta el contenido del prompt de generación de tests.
- **[Riesgo] Si el backend cambiara en el futuro para recibir campos separados, el frontend necesitaría adaptarse**: mitigado porque la restricción actual es frontend-only; un cambio futuro requeriría su propio cambio.
- **[Trade-off] Las tres áreas de texto ocupan más espacio vertical** que un solo textarea. Mitigación: usar alturas reducidas (3-4 líneas) para cada sección.
