## 1. Template - Formulario estructurado

- [x] 1.1 Reemplazar textarea libre por tres textareas con ids `context`, `code`, `tests` y labels "Contexto", "Código", "Pruebas"
- [x] 1.2 Agregar placeholders descriptivos en cada textarea guiando al usuario
- [x] 1.3 Agregar evento `change` en el input file para auto-detectar el nombre del proyecto

## 2. JavaScript - Lógica de frontend

- [x] 2.1 Implementar función que combine los tres textareas en un solo prompt con formato "Contexto:\n{context}\n\nCódigo:\n{code}\n\nPruebas:\n{tests}"
- [x] 2.2 Implementar validación que impida enviar si alguna sección está vacía, mostrando mensaje de error
- [x] 2.3 Implementar auto-detección del nombre del proyecto desde `file.name` (remover extensión `.py`)
- [x] 2.4 Asignar el prompt combinado al campo `prompt` del FormData antes del envío

## 3. CSS - Estilos visuales

- [x] 3.1 Definir estilos para las tres áreas de texto con altura reducida (3-4 líneas)
- [x] 3.2 Agregar estilos para diferenciar visualmente cada sección del formulario
- [x] 3.3 Mantener consistencia visual con el resto del formulario existente

## 4. Tests - Actualización de pruebas

- [x] 4.1 Actualizar payloads en `tests/test_upload_api.py` para usar el prompt combinado con el nuevo formato
- [x] 4.2 Verificar que los tests existentes pasan con el cambio frontend-only
