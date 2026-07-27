## 1. Build and serving configuration

- [x] 1.1 Configure `vite.config.ts` — set `build.outDir` to `../static/react`, `base` to `/static/react/`, `emptyOutDir` to `true`
- [x] 1.2 Add FastAPI `StaticFiles` mount for `/static/react` in `app/main.py`
- [x] 1.3 Add FastAPI catch-all route (`/`) serving `static/react/index.html`
- [x] 1.4 Verify React SPA loads from FastAPI at `http://localhost:8000/`

## 2. Design system and visual theme

- [x] 2.1 Refine `:root` CSS custom properties: neon green `#00ff41`, cyber cyan `#00d4ff`, purple `#b400ff`, bg-deep `#0a0a0f`, text `#c0caf5`
- [x] 2.2 Add glassmorphism utility classes: `.glass-card` (backdrop-blur, semi-transparent bg, neon border), `.hologram`, `.neon-border`
- [x] 2.3 Create `MatrixRain` React component (canvas with falling katakana, auto-resize, `prefers-reduced-motion` support)
- [x] 2.4 Add scanline overlay (CSS pseudo-element with repeating horizontal lines and scroll animation)
- [x] 2.5 Add Google Fonts import: Space Grotesk (headings/body) and JetBrains Mono (code/labels)
- [x] 2.6 Define keyframe animations in a single `animations.css`: `pulse-glow`, `glitch`, `border-run`, `float`, `spin`
- [x] 2.7 Add responsive layout: max-width 960px container centered, `<640px` breakpoint with full-width cards and reduced padding
- [x] 2.8 Apply consistent styling to all existing React components (matching design tokens)

## 3. Stepper component and view flow

- [x] 3.1 Create `Stepper` component with 4-step indicator: Upload, Configure, Generate, Results
- [x] 3.2 Implement step states: active (highlighted), completed (checkmark, clickable), pending (dimmed, non-interactive)
- [x] 3.3 Add "Next" and "Back" navigation buttons with conditional enable/disable
- [x] 3.4 Restructure `App.tsx` as step state machine using `useState` for `currentStep`
- [x] 3.5 Conditionally render each step's content based on `currentStep`
- [x] 3.6 Create `GeneratingOverlay` component with spinner, typing text effect, and floating code particles (`{`, `}`, `[`, `]`, `(`, `)`)

## 4. Upload step

- [x] 4.1 Enhance `UploadPage` with drag-and-drop zone for `.py` files (visual feedback on dragover)
- [x] 4.2 Add file extension validation on drop — reject non-`.py` with error message
- [x] 4.3 Add project name input field with terminal-style label (`$ nombre del proyecto`)
- [x] 4.4 Show uploaded file name and "remove file" button after selection
- [x] 4.5 Wire file upload to `POST /api/v1/upload/source` and store `sessionId`
- [x] 4.6 Enable "Next" only after successful upload

## 5. Configure step

- [x] 5.1 Create `ConfigureStep` containing `StructuredPromptForm`
- [x] 5.2 Ensure all three fields (Contexto, Código, Pruebas) are filled before enabling "Generate Tests"
- [x] 5.3 Wire "Generate Tests" to call `POST /api/v1/ai/generate-tests`
- [x] 5.4 Advance stepper to Generating step on successful API call

## 6. Generating step

- [x] 6.1 Show spinner, typing animation, and floating code particles during generation
- [x] 6.2 Display generated test code in a code viewer with monospace font and macOS-style window dots
- [x] 6.3 Add "Copy code" button using `navigator.clipboard.writeText`
- [x] 6.4 Add "Next" button to advance to Results step
- [x] 6.5 Handle generation errors: show error message and "Retry" button

## 7. Results step

- [x] 7.1 Display test execution results: pass/fail badge, stdout section, stderr section (`TestResultsViewer`)
- [x] 7.2 Display quality evaluation metrics table: coverage (≥80%), mutation score (≥70%), failure detection (≥60%) (`EvaluationMetrics`)
- [x] 7.3 Add color-coded pass (green checkmark) / fail (red cross) indicators per metric
- [x] 7.4 Add "Download Report" button wired to `POST /api/v1/reports/generate` + download URL
- [x] 7.5 Verify PDF binary download response mapping

## 8. Docker build fix

- [x] 8.1 Fix `Dockerfile.frontend`: update build to `npx vite build --outDir dist --base /`
- [x] 8.2 Fix UploadPage error handling: properly display FastAPI 422 validation errors (syntax errors, missing fields)

## 9. Verification and cleanup

- [ ] 9.1 Verify end-to-end flow: upload → configure → generate → results
- [ ] 9.2 Verify Matrix rain respects `prefers-reduced-motion` media query
- [ ] 9.3 Verify responsive layout at 320px, 640px, 960px, and 1440px viewports
- [ ] 9.4 Verify all quality thresholds display correct pass/fail indicators
- [ ] 9.5 Verify PDF report downloads correctly
- [ ] 9.6 Remove Jinja2 template routes (`/api/v1/upload/page`) after manual QA pass
- [ ] 9.7 Delete deprecated files: `base.html`, `upload.html`, `style.css`, `upload.js`
