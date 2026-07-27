## ADDED Requirements

### Requirement: AI generation routed through Negocio layer

The AI test generation SHALL be routed through the new Negocio layer instead of directly from controllers to services.

#### Scenario: Generate tests via Negocio
- **WHEN** a POST request is sent to `/api/v1/ai/generate-tests` with `session_id` and `prompt`
- **THEN** the router SHALL delegate to the Negocio prompts module
- **THEN** the Negocio layer SHALL call the Servicios AI service
- **THEN** the response SHALL return the generated test code

### Requirement: Regeneration endpoint preserved

The system SHALL maintain the `POST /api/v1/ai/regenerate-tests` endpoint through the Negocio layer.

#### Scenario: Regenerate tests via Negocio
- **WHEN** a POST request is sent to `/api/v1/ai/regenerate-tests`
- **THEN** the Negocio layer SHALL process the improvement prompt
- **THEN** the AI service SHALL generate improved test code

### Requirement: AI service uses QwenCoder via Ollama

The AI service SHALL continue using the local Ollama instance with QwenCoder model.

#### Scenario: Ollama connection
- **WHEN** the AI service receives a generation request
- **THEN** it SHALL send the request to the configured Ollama URL (default: `http://localhost:11434`)
- **THEN** it SHALL use the `qwen2.5-coder:7b` model
