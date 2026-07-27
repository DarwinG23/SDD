## Why

The current codebase structure deviates from the documented architecture in `docs/`. Core modules (test execution, evaluation, reports, improvement cycle) are missing, layer boundaries are flat, and deployment lacks containerization. This restructure aligns the codebase with the architecture docs while implementing the full planned system.

## What Changes

- Migrate from Jinja2 templates to React frontend
- Create Negocio layer with subpackages: validation, evaluation, prompts, reports
- Create Persistencia layer with SQLAlchemy models and repositories
- Move routing from controllers to dedicated `app/routers/` module
- Implement test execution via pytest subprocess (60s timeout)
- Implement evaluation (coverage ≥80%, mutation ≥70%, failure detection ≥60%)
- Implement improvement cycle with automated prompt regeneration
- Implement PDF report generation and download
- Create Docker Compose deployment (Nginx + Backend + PostgreSQL)
- Update nginx.conf for containerized deployment

## Capabilities

### New Capabilities
- `react-frontend`: React-based SPA replacing Jinja2 templates
- `test-execution`: pytest subprocess execution with 60s timeout and result reporting
- `code-evaluation`: Coverage, mutation score, and failure detection analysis against quality thresholds
- `improvement-cycle`: Automated prompt improvement and test regeneration when thresholds not met
- `report-generation`: PDF report compilation and download
- `docker-deployment`: Docker Compose with Nginx reverse proxy, FastAPI backend, and PostgreSQL

### Modified Capabilities
- `source-code-upload`: Adapt upload flow from Jinja2 to React frontend
- `structured-prompt-input`: Integrate structured prompt form with React components
- `ai-test-generation`: Route AI generation through the new Negocio layer
- `validation-process-ui`: Adapt overlay UI to React component architecture

## Non-goals

- Multi-language support (Python only)
- CI/CD integration
- Integration, performance, or security testing
- Support for multiple AI model providers beyond QwenCoder

## Impact

- **Backend**: New packages (`negocio/`, `persistencia/`, `routers/`); existing controllers restructured as pure handlers
- **Frontend**: Complete rewrite from Jinja2 templates to React SPA
- **Infrastructure**: Docker Compose setup, updated `nginx.conf`, PostgreSQL service
- **Dependencies**: New: `coverage.py`, `mutmut`, `reportlab` (or similar), `node`/`npm` for React
