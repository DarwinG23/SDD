## Context

El sistema SmartUnitTest no cuenta actualmente con un punto de entrada para que el tester suba su propio código fuente. El flujo existente asume que el código ya está disponible en el sistema. Este diseño cubre la nueva funcionalidad de upload de archivos `.py` con captura simultánea de nombre de proyecto y prompt estructurado, almacenamiento temporal en disco y reenvío automático al módulo de validación.

**Stack**: FastAPI + Jinja2 Templates + Uvicorn (frontend y backend monolítico)
**Constraint principal**: El código NO se persiste en base de datos — solo vive durante la sesión del tester.

## Goals / Non-Goals

**Goals:**
- Interfaz web con drag & drop y selector de archivos nativo para subir un archivo `.py`
- Captura en un solo paso: archivo, nombre del proyecto y prompt estructurado
- Almacenamiento del archivo en disco temporal (`/tmp` o similar) asociado a la sesión
- Límite de 2 GB por archivo, validación de extensión `.py`
- Reenvío automático al endpoint `POST /api/v1/validation/code` tras upload exitoso
- Limpieza del archivo temporal al salir de la página / cerrar sesión
- Manejo de errores: archivo inválido, tamaño excedido, error de validación

**Non-Goals:**
- Subida de múltiples archivos o comprimidos (ZIP, RAR)
- Persistencia en base de datos o filesystem permanente
- Editor de código en el navegador
- Soporte multi-lenguaje (solo Python)
- Control de versiones o historial

## Decisions

### 1. Nuevo endpoint vs adaptar `POST /api/v1/validation/code`

**Decisión:** Nuevo endpoint `POST /api/v1/upload/source`

| Opción | Pros | Contras |
|--------|------|---------|
| Adaptar `/validation/code` | Menos cambios, reuso inmediato | Mezcla responsabilidades (upload ≠ validation), rompe contrato existente |
| **Nuevo `/upload/source`** | Responsabilidad única, puede manejar multipart/form-data, devuelve un `uploadId` para跟踪 | Un endpoint más |

El nuevo endpoint recibe el multipart (archivo + metadatos), escribe a disco temporal, y dispara la validación internamente. Devuelve el resultado de validación al frontend.

### 2. Almacenamiento temporal en disco

**Decisión:** Directorio `/tmp/smartunittest/uploads/{sessionId}/`

- Cada sesión tiene su propio directorio, limpiado al cerrar sesión (evento `session destroy` o `window.beforeunload` + cleanup endpoint)
- El archivo se guarda con nombre original sanitizado (UUID prefix para evitar colisiones)
- Tamaño máximo 2 GB validado antes de escritura

### 3. Limpieza de archivos temporales

**Decisión:** Estrategia híbrida
- **Lado frontend**: `beforeunload` → llama a `DELETE /api/v1/upload/source/{sessionId}` para limpiar
- **Lado backend**: Tarea cron interna (o `BackgroundTasks` de FastAPI) que limpia archivos con más de 1 hora de antigüedad en `/tmp/smartunittest/uploads/` (deadman switch por si el usuario cierra el navegador abruptamente)

### 4. Frontend drag & drop

**Decisión:** Componente vanilla HTML/JS con soporte para `dragenter`, `dragover`, `drop` y `click` para abrir explorador de archivos. Sin librerías externas para evitar dependencias adicionales. Integrado en Jinja2 template.

### 5. Flujo post-upload

**Decisión:** El endpoint `/upload/source` escribe a disco, luego invoca síncronamente `POST /api/v1/validation/code` pasándole la ruta del archivo temporal. Devuelve al frontend el resultado de validación (éxito/error). Si la validación falla, el archivo temporal se elimina inmediatamente.

```
Frontend                    Backend                       Validation
   │                          │                              │
   │  POST /upload/source     │                              │
   │  (file + name + prompt)  │                              │
   │─────────────────────────>│                              │
   │                          │  Guarda en /tmp/{session}/   │
   │                          │  Valida extensión .py        │
   │                          │  Valida tamaño < 2GB         │
   │                          │                              │
   │                          │  POST /validation/code       │
   │                          │─────────────────────────────>│
   │                          │                              │
   │                          │  Resultado validación        │
   │                          │<─────────────────────────────│
   │                          │                              │
   │  {valid: true/false,     │                              │
   │   uploadId, errors}      │                              │
   │<─────────────────────────│                              │
```

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Archivos de 2GB agotan disco temporal | Validar espacio disponible antes de escribir; configurar cuota máxima por sesión |
| Usuario cierra navegador sin limpiar | Tarea cron de limpieza periódica (TTL 1 hora) |
| Subida simultánea de muchos usuarios satura disco | Monitorear uso de `/tmp`; establecer límite de sesiones concurrentes si es necesario |
| Nombre de archivo malicioso (path traversal) | Sanitizar nombre: usar UUID + extensión original, descartar el nombre original del cliente |
| Timeout de conexión en archivos grandes | Usar streaming upload con `UploadFile` de FastAPI; configurar `nginx client_max_body_size` a 2GB |
