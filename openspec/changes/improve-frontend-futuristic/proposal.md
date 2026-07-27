## Why

The current Jinja2-based frontend uses a single-page overlay approach that feels cluttered and lacks visual flow. A React SPA with a polished cyberpunk/sci-fi theme will deliver a more immersive, responsive experience that matches the cutting-edge nature of AI-powered test generation.

## What Changes

- Replace Jinja2 template frontend with React SPA served by FastAPI
- Restructure the single-page overlay flow into a stepper-based multi-view experience (Upload → Configure → Generate → Results)
- Implement a clean sci-fi design system: glassmorphism cards, holographic accents, animated borders, and matrix rain background
- Add Matrix rain canvas and scanline effects to the React version
- Polish all React components with consistent typography (Space Grotesk + JetBrains Mono), neon color tokens, and micro-animations
- Deprecate Jinja2 templates (base.html, upload.html) and vanilla JS (upload.js)

## Capabilities

### New Capabilities
- `view-redesign`: Stepper-based multi-view flow with dedicated pages for upload, prompt configuration, test generation, and results
- `visual-theme`: Cyberpunk/sci-fi design system with glassmorphism, holographic effects, matrix rain, neon tokens, and tech animations

### Modified Capabilities

- (none — no existing specs)

## Non-goals

- New backend functionality or API endpoints
- CI/CD integration for the React build pipeline
- Multi-language support for the frontend
- Integration or e2e testing for the frontend
- Mobile-native or PWA capabilities
- Accessibility overhaul beyond basic compliance

## Impact

- `app/templates/base.html` and `app/templates/upload.html` — deprecated
- `app/static/js/upload.js` — deprecated
- `app/static/css/style.css` — deprecated
- `app/frontend/` — enhanced and promoted to primary frontend
- FastAPI upload controller — may need route adjustments to serve React SPA build
- `app/main.py` — may need static file mount for React build output
