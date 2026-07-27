## Context

Current codebase uses a flat architecture: controllers directly instantiate services in `main.py`, with no Negocio or Persistencia layers. The `app/routers/` directory is empty. Frontend is Jinja2 templates. No database, no test execution, no evaluation, no reports.

Target architecture (from `docs/`):
- **Presentacion**: `controllers/` + `routers/` (separated)
- **Negocio**: `validation/`, `evaluation/`, `prompts/`, `reports/`
- **Servicios**: `ai_service/`, `test_runner/`
- **Persistencia**: `models/`, `repositories/` (SQLAlchemy + PostgreSQL)
- **Frontend**: React SPA
- **Deployment**: Docker Compose (Nginx + Backend + PostgreSQL)

## Goals / Non-Goals

**Goals:**
- Align codebase structure with documented 4-layer architecture
- Implement all missing modules: test execution, evaluation, improvement cycle, report generation
- Migrate frontend from Jinja2 to React
- Prepare persistence layer scaffolding with SQLAlchemy models
- Containerize with Docker Compose
- Preserve all existing functionality during restructure

**Non-Goals:**
- Multi-language support
- Migration of existing file storage to PostgreSQL (structure-only)
- CI/CD pipeline setup
- Authentication/authorization

## Decisions

### D1: Layer structure alignment with docs

The `app/` directory will be reorganized into four packages mirroring the documented architecture:

```
app/
  main.py                    # App entry, DI wiring
  routers/                   # API route definitions (moved from controllers)
    __init__.py
    validation.py            # POST /api/v1/validation/*
    ai.py                    # POST /api/v1/ai/*
    tests.py                 # POST /api/v1/tests/*
    evaluation.py            # POST /api/v1/evaluation/*
    reports.py               # POST /api/v1/reports/*
  controllers/               # Request handling logic
    __init__.py
    upload_controller.py     # Kept, simplified
    ai_controller.py         # Kept, simplified
  negocio/                   # Business logic layer
    __init__.py
    validation.py            # Syntax + prompt validation
    evaluation.py            # Coverage, mutation, failure detection
    prompts.py               # Improvement prompt generation
    reports.py               # Report compilation
  servicios/                 # External service integration
    __init__.py
    ai_service.py            # Ollama/QwenCoder client
    test_runner.py           # pytest subprocess execution
  persistencia/              # Data access layer
    __init__.py
    models.py                # SQLAlchemy ORM models
    repositories.py          # Data access repositories
  services/                  # Existing services (migrate gradually)
    file_storage.py
    validation.py
    ai_service.py
```

**Rationale**: Directly maps to `Diagrama_paquetes.md` layers. Negocio owns business rules, Servicios wraps external integrations, Persistencia abstracts data access.

### D2: Gradual controller migration

Controllers will be refactored to delegate to Negocio while maintaining the same API contracts. The `app/services/` directory will be kept during transition and deprecated once all logic moves to Negocio.

**Rationale**: Zero disruption to existing frontend during migration. API contracts remain unchanged.

### D3: pytest as isolated subprocess (RN4)

Test execution will run pytest via `asyncio.create_subprocess_exec` with a 60-second timeout. A dedicated ADR documents isolation strategy.

**Rationale**: Isolated execution prevents test failures from crashing the main process. Timeout ensures RN4 compliance.

### D4: React frontend alongside FastAPI

React app will live in `app/frontend/` with a build output served by FastAPI or Nginx. During development, the React dev server proxies `/api/` requests to the backend.

**Rationale**: FastAPI can serve the React SPA with a simple mount, avoiding a separate dev server in production while enabling React's full toolchain in development.

### D5: Docker Compose with three services

```
services:
  nginx:        # Reverse proxy (ports 443:443, 80:80)
  backend:      # FastAPI + Uvicorn
  postgres:     # PostgreSQL 16
```

**Rationale**: Matches `Diagrama_despliegue.md`. Nginx handles SSL termination and static file serving. Backend runs the Python app. PostgreSQL provides persistent storage.

### D6: SQLAlchemy models for domain entities

Models will follow the class diagram (`docs/Diagrama_clases.md`): Plantilla, Promt, CodigoFuente, PruebaUnitaria, Evaluacion, Reporte, Medicion, TipoMetrica, Rango, Fenomeno.

**Rationale**: The class diagram defines a complete domain model that accurately represents the system's data entities and their relationships.

## Risks / Trade-offs

- **[Risk] Existing file storage vs. new DB models**: File storage (`FileStorageService`) works with `/tmp/smartunittest/uploads/`. New Persistencia layer targets PostgreSQL. A dual-write period during migration could cause inconsistency. → **Mitigation**: Persistencia is structure-only for now; file storage remains the active backend.
- **[Risk] React migration scope**: Migrating from Jinja2 to React is a large frontend rewrite. → **Mitigation**: Keep both frontends functional during transition; React replaces Jinja2 only when feature-complete.
- **[Risk] pytest isolation complexity**: Running pytest as subprocess introduces process management overhead (timeouts, resource limits, temp files). → **Mitigation**: Use `asyncio.create_subprocess_exec` with strict timeout; documented in ADR.
- **[Risk] Docker Compose adds operational complexity**: Developers need Docker installed. → **Mitigation**: Maintain the current non-containerized dev workflow; Docker Compose is for production/staging deployment.
