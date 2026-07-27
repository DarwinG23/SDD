## Context

SmartUnitTest's current frontend uses Jinja2 templates served by FastAPI with a single-page overlay approach. A partial React SPA exists in `app/frontend/` with all necessary components but lacks routing, a stepper flow, Matrix rain, and is not yet served by FastAPI. The existing style is cyberpunk/Matrix-inspired and should be refined toward a cleaner sci-fi aesthetic with glassmorphism and holographic elements.

## Goals / Non-Goals

**Goals:**
- Serve React SPA build from FastAPI as the primary frontend
- Restructure view flow into a 4-step stepper (Upload → Configure → Generate → Results)
- Implement a polished cyberpunk/sci-fi design system with glassmorphism, holograms, and Matrix rain
- Add Matrix rain canvas animation to the React version
- Keep all existing functionality intact — visual-only change
- Deprecate Jinja2 templates and vanilla JS

**Non-Goals:**
- New backend API endpoints or functionality changes
- State management library beyond React built-ins
- Routing library (single-page stepper, no URL routing needed)
- End-to-end or integration tests for the new frontend

## Decisions

**Decision 1: FastAPI serving strategy — Vite build output mounted as static files**
- Build output goes to `app/static/react/` via Vite config
- FastAPI mounts `StaticFiles` at `/static/react` and serves `index.html` at `/`
- `vite.config.ts` sets `base: '/static/react/'` so assets resolve correctly
- In development, use Vite dev server on port 5173 with proxy to FastAPI on port 8000
- Chosen over alternatives: Jinja2 wrapper (adds unnecessary indirection), separate server (complicates deployment)

**Decision 2: View flow — Controlled stepper with React state (no router)**
- A `Stepper` component manages step progression with `useState`
- Steps: `upload` → `configure` → `generating` → `results`
- Each step conditionally renders the relevant section(s)
- Navigation: "Next" / "Back" buttons, step indicator dots
- Chosen over React Router: only 4 steps in fixed order, no URL-based navigation needed

**Decision 3: Component architecture — App.tsx as state machine coordinator**
- `App.tsx` holds all session state (`sessionId`, `testCode`, `testResult`, `evaluation`, `reportId`) and current step
- Existing components (`UploadPage`, `StructuredPromptForm`, `TestResultsViewer`, `EvaluationMetrics`, `ReportDownload`) adapted to receive step as prop
- New components: `MatrixRain` (canvas animation), `Stepper` (step indicator + navigation), `GeneratingOverlay` (animated generation state)
- `ValidationOverlay` refactored from modal to inline step content

**Decision 4: Styling — Enhanced CSS custom properties with glassmorphism focus**
- Retain existing `:root` tokens with refined sci-fi palette (cyan primary, green accent, purple secondary)
- Introduce glassmorphism utility classes: `.glass-card`, `.hologram`, `.neon-border`
- Matrix rain as a dedicated React canvas component (ported from `upload.js`)
- Scanline overlay as CSS pseudo-element (already in React style.css)
- Keyframe animations organized in a single `animations.css` import

**Decision 5: Vite build configuration — Output to FastAPI static directory**
- `build.outDir`: `../static/react` (relative to `app/frontend/`)
- `build.emptyOutDir`: `true`
- `base`: `/static/react/`
- Clean build before each deployment

**Decision 6: Deprecation strategy — Gradual with feature flag fallback**
- Phase 1: Serve React SPA at `/` alongside Jinja2 at `/api/v1/upload/page`
- Phase 2: After verification, remove Jinja2 routes and template files
- Quick rollback: re-enable Jinja2 route (code kept in git history)

## Risks / Trade-offs

- **[Matrix rain performance]** Heavy canvas animation may impact low-end devices → Mitigation: add `frameSkip` param and `prefers-reduced-motion` media query to disable animation
- **[Build path mismatch]** Incorrect Vite `base` config will break asset loading in production → Mitigation: automated check via `index.html` asset reference validation in CI
- **[Stepper complexity]** State management across 4 steps with async operations can get tangled → Mitigation: `useReducer` for step state if `useState` becomes unwieldy
- **[Jinja2 removal timing]** Premature deprecation could block users if React SPA has issues → Mitigation: keep Jinja2 route active during Phase 1, remove only after manual QA pass
