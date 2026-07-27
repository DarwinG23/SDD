## ADDED Requirements

### Requirement: Upload flow integrated with React frontend

The upload system SHALL work with the new React SPA while preserving existing upload behavior.

#### Scenario: Upload from React form
- **WHEN** the React upload form submits a .py file, project name, and prompt
- **THEN** the system SHALL validate the file extension (.py only) and file size (max 2 GB)
- **THEN** the system SHALL store the file in the session directory
- **THEN** the system SHALL perform syntax validation via `POST /api/v1/validation/code`

### Requirement: Validation endpoints preserved in Negocio layer

The validation logic SHALL move from the Presentation layer to the Negocio layer while keeping the same API contract.

#### Scenario: Code validation routed through Negocio
- **WHEN** a POST request is sent to `/api/v1/validation/code`
- **THEN** the router SHALL delegate to the Negocio validation module
- **THEN** the response format SHALL remain unchanged (`valid: bool`, `errors: [...]`)
