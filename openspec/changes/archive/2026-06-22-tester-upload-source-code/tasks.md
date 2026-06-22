## 1. Backend — Endpoint de Upload

- [x] 1.1 Crear ruta `POST /api/v1/upload/source` en FastAPI que reciba `UploadFile`, `project_name` (str) y `prompt` (str)
- [x] 1.2 Implementar validación de extensión `.py` y tamaño máximo 2 GB antes de escritura
- [x] 1.3 Implementar sanitización de nombre de archivo: UUID prefix + extensión, descartar nombre original del cliente
- [x] 1.4 Escribir archivo a `/tmp/smartunittest/uploads/{sessionId}/` con manejo de directorios por sesión

## 2. Backend — Integración con Validación

- [x] 2.1 Invocar `POST /api/v1/validation/code` internamente tras escritura exitosa
- [x] 2.2 Manejar respuesta de validación: devolver resultado al frontend, eliminar archivo si falla validación
- [x] 2.3 Agregar endpoint `DELETE /api/v1/upload/source/{sessionId}` para limpieza manual desde frontend

## 3. Backend — Limpieza Automática

- [x] 3.1 Implementar tarea `BackgroundTasks` en FastAPI para limpiar directorios de sesión inactivos (>1 hora)
- [x] 3.2 Registrar la tarea de limpieza al iniciar la aplicación (evento `startup`)

## 4. Frontend — Página de Upload (Jinja2 Template)

- [x] 4.1 Crear template `upload.html` con layout base de la aplicación
- [x] 4.2 Implementar componente drag & drop vanilla JS (eventos `dragenter`, `dragover`, `drop`, `click`)
- [x] 4.3 Agregar campo de texto para nombre de proyecto y textarea para prompt estructurado
- [x] 4.4 Implementar validación frontend: extensión `.py`, campos requeridos antes de submit
- [x] 4.5 Implementar llamada `fetch` a `POST /api/v1/upload/source` con FormData
- [x] 4.6 Mostrar resultado de validación (éxito/error) en la interfaz
- [x] 4.7 Implementar `beforeunload` → `DELETE /api/v1/upload/source/{sessionId}` para limpieza al salir

## 5. Configuración de Infraestructura

- [x] 5.1 Configurar `nginx client_max_body_size 2048m` para permitir archivos de hasta 2 GB
- [x] 5.2 Configurar timeout de conexión en nginx para uploads grandes (`proxy_read_timeout`, `proxy_send_timeout`)
- [x] 5.3 Verificar que `/tmp` tenga espacio suficiente y configurar monitoreo

## 6. Pruebas

- [x] 6.1 Escribir tests unitarios para endpoint `POST /api/v1/upload/source` (éxito, extensión inválida, tamaño excedido)
- [x] 6.2 Escribir tests para sanitización de nombre de archivo (path traversal, caracteres especiales)
- [x] 6.3 Escribir tests de integración: upload → validación → limpieza
- [x] 6.4 Escribir tests para la tarea de limpieza automática (TTL 1 hora)
- [x] 6.5 Verificar cobertura con coverage.py (mínimo 80%)
