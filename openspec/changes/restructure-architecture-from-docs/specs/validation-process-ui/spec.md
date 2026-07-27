## ADDED Requirements

### Requirement: Validation overlay in React

The validation overlay UI SHALL be implemented as a React component with the same behavior as the current implementation.

#### Scenario: Overlay shows during validation
- **WHEN** the user submits code for validation
- **THEN** the React app SHALL display a full-screen overlay with a loading spinner
- **THEN** the overlay SHALL block interaction with the form

#### Scenario: Success result in overlay
- **WHEN** validation succeeds
- **THEN** the overlay SHALL show a success icon and "Código válido" message
- **THEN** the overlay SHALL show a "Generar pruebas unitarias" button

#### Scenario: Error result in overlay
- **WHEN** validation fails
- **THEN** the overlay SHALL show error details
- **THEN** the overlay SHALL show a "Volver a subir" button
