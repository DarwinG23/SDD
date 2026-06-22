## ADDED Requirements

### Requirement: RF001 - Overlay de carga durante validación

El sistema SHALL mostrar un overlay a pantalla completa mientras se procesa la validación del código fuente.

#### Scenario: Apertura del overlay al enviar
- **WHEN** el usuario hace clic en "Subir y validar"
- **THEN** el sistema MUST mostrar un overlay semitransparente que cubra toda la pantalla
- **THEN** el overlay MUST contener un indicador de carga animado (spinner)
- **THEN** el overlay MUST bloquear la interacción con el formulario subyacente

#### Scenario: Cierre del overlay al completar
- **WHEN** la validación finaliza (éxito o error)
- **THEN** el overlay MUST ocultar el spinner y mostrar el resultado correspondiente

### Requirement: RF002 - Resultado de validación exitosa

El sistema SHALL mostrar un resultado visual de validación exitosa con opción a generar pruebas.

#### Scenario: Visualización de éxito
- **WHEN** la validación del código es exitosa
- **THEN** el overlay MUST mostrar un ícono de verificación y el mensaje "Código válido" en color verde
- **THEN** el overlay MUST mostrar un botón "Generar pruebas unitarias"

#### Scenario: Botón Generar pruebas (placeholder)
- **WHEN** el usuario hace clic en "Generar pruebas unitarias"
- **THEN** el sistema MUST mostrar un mensaje indicando que la funcionalidad estará disponible próximamente (sin implementar generación real)

### Requirement: RF003 - Resultado de validación fallida

El sistema SHALL mostrar un resultado visual de error con opción a reintentar.

#### Scenario: Visualización de error
- **WHEN** la validación del código falla
- **THEN** el overlay MUST mostrar un ícono de error y los detalles del error en color rojo
- **THEN** el overlay MUST mostrar un botón "Volver a subir"

#### Scenario: Reintentar después de error
- **WHEN** el usuario hace clic en "Volver a subir"
- **THEN** el overlay MUST cerrarse
- **THEN** el formulario MUST reiniciarse (limpiar archivo, nombre, secciones de prompt)

### Requirement: RF004 - Integración con formulario estructurado

El sistema SHALL reemplazar el área de resultado actual por el nuevo overlay.

#### Scenario: Eliminación del resultado inline
- **WHEN** el overlay está activo
- **THEN** el div de resultado inline (`#result`) MUST permanecer oculto
- **THEN** todo el feedback de validación MUST mostrarse exclusivamente en el overlay
