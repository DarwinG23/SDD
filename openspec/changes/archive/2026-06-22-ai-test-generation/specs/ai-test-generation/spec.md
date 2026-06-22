## ADDED Requirements

### Requirement: RF001 - Endpoint de generación de pruebas

El sistema SHALL proveer un endpoint `POST /api/v1/ai/generate-tests` que genere pruebas unitarias usando OpenAI API.

#### Scenario: Solicitud exitosa de generación
- **WHEN** el frontend envía una solicitud POST a `/api/v1/ai/generate-tests` con `session_id` y `prompt` en el body
- **THEN** el sistema MUST invocar OpenAI API (GPT-4) con el prompt estructurado
- **THEN** el sistema MUST devolver un JSON con `success: true` y `test_code` conteniendo las pruebas generadas

#### Scenario: Error de API Key
- **WHEN** la variable `OPENAI_API_KEY` no está configurada
- **THEN** el sistema MUST devolver un error HTTP 503 con mensaje "API key no configurada"

#### Scenario: Error de OpenAI
- **WHEN** la API de OpenAI retorna un error
- **THEN** el sistema MUST devolver un error HTTP 502 con los detalles del error

### Requirement: RF002 - Servicio de IA (ai_service)

El sistema SHALL implementar un servicio modular para la comunicación con OpenAI API.

#### Scenario: Construcción del prompt para OpenAI
- **WHEN** el servicio recibe el prompt estructurado y el código fuente
- **THEN** el sistema MUST construir un mensaje para OpenAI que incluya el contexto, código y las instrucciones de pruebas
- **THEN** el sistema MUST solicitar a GPT-4 que genere pruebas unitarias en formato pytest

#### Scenario: Parseo de respuesta
- **WHEN** OpenAI responde con el código de pruebas
- **THEN** el sistema MUST extraer el bloque de código Python de la respuesta
- **THEN** el sistema MUST devolver solo el código de pruebas sin markdown ni envolturas

### Requirement: RF003 - Integración con botón del overlay

El sistema SHALL conectar el botón "Generar pruebas unitarias" del overlay con el endpoint real.

#### Scenario: Clic en generar pruebas
- **WHEN** el usuario hace clic en "Generar pruebas unitarias" en el overlay de validación exitosa
- **THEN** el overlay MUST cambiar a estado de carga con spinner indeterminado
- **THEN** el frontend MUST llamar a `POST /api/v1/ai/generate-tests` con el session_id y prompt

#### Scenario: Generación exitosa
- **WHEN** el endpoint responde con las pruebas generadas
- **THEN** el overlay MUST ocultar el spinner
- **THEN** el sistema MUST mostrar las pruebas generadas en un visor de código dentro del overlay

#### Scenario: Error en generación
- **WHEN** el endpoint responde con error
- **THEN** el overlay MUST mostrar el mensaje de error
- **THEN** el overlay MUST ofrecer botón "Reintentar" para volver a intentar

### Requirement: RF004 - Visualización de pruebas generadas

El sistema SHALL mostrar las pruebas generadas en un visor de código con formato legible.

#### Scenario: Visor de código
- **WHEN** las pruebas se han generado exitosamente
- **THEN** el overlay MUST mostrar un bloque `<pre><code>` con el código de pruebas generado
- **THEN** el visor MUST tener resaltado visual (fondo oscuro, fuente monospace)

#### Scenario: Copia del código
- **WHEN** el usuario ve las pruebas generadas
- **THEN** el sistema MUST proveer un botón "Copiar" que copie el código al portapapeles
