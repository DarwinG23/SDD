## ADDED Requirements

### Requirement: Docker Compose with three services

The system SHALL provide a `docker-compose.yml` with Nginx, Backend, and PostgreSQL services.

#### Scenario: Docker Compose starts all services
- **WHEN** `docker compose up` is executed
- **THEN** Nginx SHALL start and listen on port 443 (HTTPS) proxying to backend on port 80 (HTTP)
- **THEN** the FastAPI backend SHALL start with Uvicorn
- **THEN** PostgreSQL SHALL start on port 5432

### Requirement: Nginx reverse proxy configuration

Nginx SHALL act as a reverse proxy forwarding HTTPS requests to the FastAPI backend.

#### Scenario: Request proxied to backend
- **WHEN** a request reaches Nginx on port 443
- **THEN** Nginx SHALL forward it to `http://backend:8000`
- **THEN** the response SHALL be returned to the client

### Requirement: Backend container with dependencies

The backend SHALL run in a container with all Python dependencies installed.

#### Scenario: Backend starts successfully
- **WHEN** the backend container starts
- **THEN** Uvicorn SHALL serve the FastAPI app on port 8000
- **THEN** the container SHALL have access to the upload directory volume

### Requirement: PostgreSQL persistence

The system SHALL use PostgreSQL for persistent storage of evaluations, reports, and metrics.

#### Scenario: Database connection established
- **WHEN** the backend starts
- **THEN** it SHALL connect to PostgreSQL using credentials from environment variables
- **THEN** tables SHALL be created via SQLAlchemy ORM
