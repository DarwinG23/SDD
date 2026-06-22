## ADDED Requirements

### Requirement: RF001 - Formulario estructurado de prompt

El sistema SHALL reemplazar el textarea libre de prompt por un formulario con tres secciones fijas: Contexto, Código y Pruebas.

#### Scenario: Visualización de secciones del formulario
- **WHEN** el usuario accede a la página de carga de código fuente
- **THEN** el sistema MUST mostrar tres áreas de texto etiquetadas: "Contexto", "Código" y "Pruebas"

#### Scenario: Envío con todas las secciones completas
- **WHEN** el usuario completa las tres secciones y envía el formulario
- **THEN** el frontend MUST combinar las secciones en un único string `prompt` con el formato: "Contexto:\n{contexto}\n\nCódigo:\n{codigo}\n\nPruebas:\n{pruebas}"

#### Scenario: Validación de sección vacía
- **WHEN** el usuario intenta enviar el formulario con una o más secciones vacías
- **THEN** el sistema MUST mostrar un mensaje de error indicando qué secciones deben completarse

### Requirement: RF002 - Auto-detección del nombre del proyecto

El sistema SHALL detectar automáticamente el nombre del proyecto desde el nombre del archivo `.py` subido.

#### Scenario: Auto-detección al subir archivo
- **WHEN** el usuario selecciona o arrastra un archivo `.py` al área de carga
- **THEN** el campo "Nombre del proyecto" MUST auto-completarse con el nombre del archivo sin la extensión `.py`

#### Scenario: Edición del nombre auto-detectado
- **WHEN** el campo "Nombre del proyecto" se auto-completa
- **THEN** el usuario MUST poder editar manualmente el valor auto-detectado

#### Scenario: Archivo sin nombre visible
- **WHEN** el campo de archivo está vacío
- **THEN** el campo "Nombre del proyecto" MUST permanecer vacío o mantener el valor ingresado manualmente

### Requirement: RF003 - Combinación de campos en el frontend

El sistema SHALL construir el prompt estructurado en el frontend antes del envío al backend.

#### Scenario: Construcción del prompt en el envío
- **WHEN** el usuario hace clic en "Subir y validar"
- **THEN** el frontend MUST concatenar las secciones en un solo campo `prompt` con saltos de línea entre secciones y MUST incluir los encabezados "Contexto:", "Código:" y "Pruebas:" como parte del string

#### Scenario: Formato del prompt combinado
- **WHEN** el frontend construye el prompt
- **THEN** el formato resultante SHALL ser:
  Contexto:
  {texto del contexto}

  Código:
  {texto del código}

  Pruebas:
  {texto de las pruebas}

#### Scenario: Backend recibe prompt único
- **WHEN** el frontend envía la solicitud POST a `/api/v1/upload/source`
- **THEN** el campo `prompt` MUST contener el string combinado de todas las secciones
- **THEN** el backend MUST procesar el prompt sin cambios, manteniendo compatibilidad con la interfaz existente

### Requirement: RF004 - Estilos visuales del formulario

El sistema SHALL aplicar estilos visuales consistentes a los nuevos campos del formulario estructurado.

#### Scenario: Apariencia de las áreas de texto
- **WHEN** el formulario estructurado se renderiza
- **THEN** cada sección MUST tener un área de texto con altura reducida individual y diseño que las diferencie visualmente

#### Scenario: Etiquetas descriptivas
- **WHEN** el formulario se muestra
- **THEN** cada sección MUST tener una etiqueta y un placeholder que guíen al usuario sobre qué contenido ingresar
