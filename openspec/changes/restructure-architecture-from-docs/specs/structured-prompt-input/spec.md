## ADDED Requirements

### Requirement: Structured prompt form in React

The structured prompt input SHALL be implemented as React components with the same three-section format.

#### Scenario: Three-section form rendered by React
- **WHEN** the React upload page loads
- **THEN** the form SHALL display three text areas: Context, Code, and Tests

#### Scenario: Prompt construction in React
- **WHEN** the user submits the form
- **THEN** the React app SHALL concatenate the sections with headers "Context:", "Código:", "Pruebas:" into a single `prompt` field
- **THEN** the combined prompt SHALL be sent to the backend

### Requirement: Prompt validation preserved

The system SHALL continue validating the prompt structure before AI generation.

#### Scenario: Prompt validation in Negocio
- **WHEN** the prompt is submitted
- **THEN** the Negocio validation module SHALL verify that all required sections are present
- **THEN** invalid prompts SHALL return a validation error
