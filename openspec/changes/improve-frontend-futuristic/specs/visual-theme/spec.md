## ADDED Requirements

### Requirement: Design system with CSS custom properties
The system SHALL define a complete design token system using CSS custom properties on `:root`. Tokens SHALL include colors (neon green `#00ff41`, cyber cyan `#00d4ff`, purple `#b400ff`, background deep `#0a0a0f`, text `#c0caf5`), spacing, border radius, and font families. All components SHALL reference these tokens exclusively for consistent theming.

#### Scenario: Design tokens are globally available
- **WHEN** any component renders
- **THEN** it uses CSS custom properties from `:root` for colors, spacing, and typography

### Requirement: Glassmorphism card style
Section cards SHALL use a glassmorphism effect with semi-transparent dark background (`rgba(12, 12, 24, 0.85)`), backdrop blur (`12px`), subtle neon border (`rgba(0, 255, 65, 0.15)`), and a left accent gradient bar. Cards SHALL glow on hover.

#### Scenario: Card renders with glass effect
- **WHEN** a section card is displayed
- **THEN** it shows a semi-transparent background with blur, subtle border, and left accent bar

#### Scenario: Card responds to hover
- **WHEN** the user hovers over a card
- **THEN** the border becomes brighter and the card background becomes more opaque

### Requirement: Matrix rain canvas background
The application SHALL render a Matrix rain animation on a `<canvas>` element behind all content. Columns SHALL contain falling katakana characters with varying speeds and brightness. The canvas SHALL auto-resize to fill the viewport and respect `prefers-reduced-motion`.

#### Scenario: Matrix rain renders on page load
- **WHEN** the application loads
- **THEN** a canvas with falling katakana characters animates in the background

#### Scenario: Canvas resizes with viewport
- **WHEN** the browser window resizes
- **THEN** the canvas adjusts to fill the viewport

### Requirement: Scanline overlay
The application SHALL display a CRT scanline overlay effect. A fixed pseudo-element SHALL render repeating horizontal lines that animate vertically with a slow scroll.

#### Scenario: Scanlines are visible
- **WHEN** the application is displayed
- **THEN** a scanline overlay effect is visible across the entire viewport

### Requirement: Typography system
The application SHALL use two Google Fonts: Space Grotesk for headings and body text, and JetBrains Mono for code, metrics, and labels. Labels and code-related text SHALL use uppercase with letter spacing. Terminal-style prefixes (`$`, `#`, `//`) SHALL prefix labels and comments.

#### Scenario: Headers use Space Grotesk
- **WHEN** a heading element renders
- **THEN** it uses the Space Grotesk font family

#### Scenario: Code uses JetBrains Mono
- **WHEN** code or metric text renders
- **THEN** it uses the JetBrains Mono font family

### Requirement: Keyframe animation system
The system SHALL define a set of reusable keyframe animations: `pulse-glow` (pulsing neon box-shadow), `glitch` (subtle position jitter), `border-run` (animated gradient sweep), `float` (gentle vertical bob), and `spin` (rotating spinner). Cards with glow SHALL use `pulse-glow` with a 3s cycle.

#### Scenario: Animated card glow
- **WHEN** a card with glow class is rendered
- **THEN** it pulses with a neon box-shadow on a 3-second cycle

#### Scenario: Animated border sweep
- **WHEN** a card with border-run is rendered
- **THEN** the top border gradient animates horizontally

### Requirement: Responsive layout
The application SHALL adapt to viewport widths down to 320px. The main content container SHALL use a max-width of 960px centered in the viewport. On screens below 640px, cards SHALL use full width with reduced padding.

#### Scenario: Desktop layout
- **WHEN** the viewport is wider than 960px
- **THEN** content is centered with a max-width of 960px

#### Scenario: Mobile layout
- **WHEN** the viewport is 640px or narrower
- **THEN** cards use full width with reduced padding
