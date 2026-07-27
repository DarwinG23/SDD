## 1. Layer Restructure — Package Scaffolding

- [x] 1.1 Create `app/negocio/` package with subpackages: `validation`, `evaluation`, `prompts`, `reports`
- [x] 1.2 Create `app/persistencia/` package with subpackages: `models`, `repositories`
- [x] 1.3 Create `app/routers/` package and move route definitions out of controllers
- [x] 1.4 Create `app/servicios/` package with `ai_service`, `test_runner` modules
- [x] 1.5 Add `__init__.py` with public API exports for each new package
- [x] 1.6 Refactor `main.py` to wire dependencies through new layer hierarchy

## 2. Negocio Layer — Business Logic

- [x] 2.1 Move syntax validation logic from `app/services/validation.py` to `app/negocio/validation/`
- [x] 2.2 Move prompt validation logic to `app/negocio/validation/`
- [x] 2.3 Implement `app/negocio/evaluation/` module with coverage computation (coverage.py)
- [x] 2.4 Implement mutation score computation in evaluation module (mutmut)
- [x] 2.5 Implement failure detection rate computation in evaluation module
- [x] 2.6 Implement threshold check logic for RN1 (80%), RN2 (70%), RN3 (60%)
- [x] 2.7 Implement `app/negocio/prompts/` module for improvement prompt generation
- [x] 2.8 Implement `app/negocio/reports/` module for report data compilation

## 3. Servicios Layer — External Integrations

- [x] 3.1 Keep existing `AIService` in `app/servicios/ai_service.py` (Ollama/QwenCoder)
- [x] 3.2 Create `app/servicios/test_runner.py` with pytest subprocess execution
- [x] 3.3 Implement 60-second timeout for pytest subprocess via `asyncio.wait_for`
- [x] 3.4 Add test result parsing (stdout, stderr, exit code) in test_runner

## 4. Persistencia Layer — Data Models

- [x] 4.1 Define SQLAlchemy Base and session factory in `app/persistencia/__init__.py`
- [x] 4.2 Create models: `Plantilla`, `Promt`, `CodigoFuente`, `PruebaUnitaria`
- [x] 4.3 Create models: `Evaluacion`, `Medicion`, `TipoMetrica`, `Rango`, `Fenomeno`
- [x] 4.4 Create models: `Reporte`
- [x] 4.5 Create repositories for each model in `app/persistencia/repositories/`
- [x] 4.6 Add Alembic configuration for database migrations

## 5. New API Endpoints — Routers

- [x] 5.1 Create `app/routers/validation.py` with `POST /api/v1/validation/code`, `POST /api/v1/validation/prompt`
- [x] 5.2 Create `app/routers/ai.py` with `POST /api/v1/ai/generate-tests`, `POST /api/v1/ai/regenerate-tests`
- [x] 5.3 Create `app/routers/tests.py` with `POST /api/v1/tests/execute`, `GET /api/v1/tests/{testId}/result`
- [x] 5.4 Create `app/routers/evaluation.py` with `POST /api/v1/evaluation/run`, `GET /api/v1/evaluation/{evalId}`, `POST /api/v1/evaluation/improvement-prompt`
- [x] 5.5 Create `app/routers/reports.py` with `POST /api/v1/reports/generate`, `GET /api/v1/reports/{reportId}/download`
- [x] 5.6 Register all routers in `main.py`

## 6. PDF Report Generation

- [x] 6.1 Add reportlab (or equivalent) dependency to `pyproject.toml`
- [x] 6.2 Implement PDF document generation with metrics, thresholds, and recommendations
- [x] 6.3 Validate binary response returns `Content-Type: application/pdf`

## 7. Frontend — React Migration

- [x] 7.1 Initialize React project in `app/frontend/` with Vite
- [x] 7.2 Create upload page component with drag-and-drop zone
- [x] 7.3 Create structured prompt form component (Context, Code, Tests sections)
- [x] 7.4 Create validation overlay component (loading, success, error states)
- [x] 7.5 Create test results viewer component
- [x] 7.6 Create evaluation metrics display component
- [x] 7.7 Create report download component
- [x] 7.8 Implement API client module for `/api/v1/` endpoints in React
- [x] 7.9 Configure React dev server proxy to backend
- [x] 7.10 Configure production build output served by FastAPI static mount

## 8. Docker Compose Deployment

- [x] 8.1 Create `Dockerfile` for backend (Python + dependencies)
- [x] 8.2 Create `Dockerfile` for frontend (Node build, then nginx or static)
- [x] 8.3 Create `docker-compose.yml` with nginx, backend, postgres services
- [x] 8.4 Update `nginx.conf` for containerized reverse proxy
- [x] 8.5 Add `.dockerignore` files

## 9. Tests

- [x] 9.1 Add unit tests for each Negocio module (validation, evaluation, prompts, reports)
- [x] 9.2 Add unit tests for test_runner subprocess execution and timeout
- [x] 9.3 Add integration tests for all new API endpoints
- [x] 9.4 Add test verifying coverage threshold (coverage.py pipeline ≥80%)
- [x] 9.5 Add test verifying mutation score threshold (mutmut pipeline ≥70%)
- [x] 9.6 Add test verifying failure detection threshold (≥60%)
- [x] 9.7 Verify existing tests still pass after restructure
- [x] 9.8 Run full test suite with coverage verification
