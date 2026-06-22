## Why

Actualmente el sistema no permite al tester subir su propio código fuente como punto de entrada. El flujo comienza con un código que ya está disponible en el sistema, pero no existe una interfaz para que el tester arrastre o seleccione un archivo `.py` desde su máquina e inicie el ciclo de validación, generación de pruebas y evaluación. Esta funcionalidad es el primer paso del dominio del negocio y cierra la brecha entre el tester y el sistema.

## What Changes

- Nueva interfaz web de upload con drag & drop y selector de archivos nativo
- El upload captura en un solo paso: archivo `.py`, nombre del proyecto y prompt estructurado
- El archivo se almacena en memoria (sesión del navegador / archivo temporal en servidor) sin persistencia en base de datos
- Al salir de la página o cerrar la sesión, el código se descarta automáticamente
- Una vez subido, el archivo se envía automáticamente al endpoint de validación existente `POST /api/v1/validation/code`
- Límite de tamaño máximo: 2 GB por archivo
- Solo se permite un archivo a la vez, extensión `.py`

## Capabilities

### New Capabilities
- `source-code-upload`: Subida de archivo `.py` vía interfaz web con drag & drop, captura de metadatos (nombre de proyecto, prompt estructurado), almacenamiento efímero en sesión y reenvío automático al módulo de validación.

### Modified Capabilities
- *(ninguna — no existen specs previas)*

## Non-goals

- Subida de múltiples archivos o archivos comprimidos (ZIP, RAR, etc.)
- Persistencia del código en base de datos o filesystem permanente
- Editor de código en el navegador
- Soporte para otros lenguajes que no sean Python
- Control de versiones o historial de subidas
- Integración con CI/CD o repositorios externos (Git, S3, etc.)

## Impact

- **Frontend**: Nueva vista/página de upload con componente drag & drop, campo de nombre de proyecto, editor/input de prompt estructurado
- **Backend**: Nuevo endpoint `POST /api/v1/upload/source` (o adaptación del existente `/api/v1/validation/code`) que reciba el archivo + metadatos, lo almacene temporalmente y dispare la validación
- **Seguridad**: Validación de extensión `.py`, tamaño máximo 2 GB, sanitización del archivo antes de validación sintáctica
- **Infraestructura**: El almacenamiento temporal debe considerar el límite de 2 GB — requiere configuración de tiempo de espera y buffer adecuados en el servidor
