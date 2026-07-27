## ADDED Requirements

### Requirement: React SPA replaces Jinja2 templates

The system SHALL provide a React-based single-page application that replaces all existing Jinja2 templates.

#### Scenario: Application shell serves React build
- **WHEN** a user accesses the root URL
- **THEN** the server SHALL serve the React `index.html` for all frontend routes

#### Scenario: Upload page rendered by React
- **WHEN** the user navigates to the upload page
- **THEN** the React app SHALL render the upload form with drag-and-drop, project name, and structured prompt fields

#### Scenario: API communication via fetch
- **WHEN** the React app calls any backend endpoint
- **THEN** it SHALL use `fetch` or a configured HTTP client against `/api/v1/` endpoints

### Requirement: React project toolchain

The system SHALL include a React project with build tooling.

#### Scenario: Build produces static assets
- **WHEN** the React project is built
- **THEN** it SHALL produce static files in a configured output directory served by FastAPI or Nginx

#### Scenario: Development mode available
- **WHEN** running in development mode
- **THEN** the React dev server SHALL proxy API requests to the backend

### Requirement: State management for session

The React app SHALL manage session state across the test generation flow.

#### Scenario: Session persists across steps
- **WHEN** the user completes file upload
- **THEN** the session ID SHALL be available for subsequent API calls (AI generation, test execution, evaluation)
