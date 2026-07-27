## ADDED Requirements

### Requirement: Stepper navigation
The system SHALL present a 4-step stepper (Upload → Configure → Generate → Results) that guides the user through the test generation workflow. The user SHALL navigate forward and backward through steps using "Next" and "Back" buttons. The current step SHALL be visually highlighted in the stepper indicator.

#### Scenario: User advances to next step
- **WHEN** the user completes the current step and clicks "Next"
- **THEN** the steper advances to the next step

#### Scenario: User returns to previous step
- **WHEN** the user clicks "Back"
- **THEN** the stepper returns to the previous step

### Requirement: Step state indicators
Each step in the stepper SHALL display one of three states: active (current), completed (past), or pending (future). Completed steps SHALL show a checkmark icon and be clickable for navigation. Pending steps SHALL be visually dimmed and non-interactive.

#### Scenario: Completed step shows checkmark
- **WHEN** the user completes a step
- **THEN** the step indicator shows a checkmark icon and becomes clickable

#### Scenario: Pending step is dimmed
- **WHEN** the user is on an earlier step
- **THEN** later steps appear dimmed and cannot be clicked

### Requirement: Upload step
The upload step SHALL provide a drag-and-drop zone for `.py` files, a project name input field, and a submit button. The system SHALL validate file extension on drop, show file name after selection, and allow file removal.

#### Scenario: User uploads a valid .py file
- **WHEN** the user drops a `.py` file onto the drop zone
- **THEN** the file name is displayed and the submit button becomes enabled

#### Scenario: User drops invalid file type
- **WHEN** the user drops a non-`.py` file
- **THEN** an error message is shown and the file is rejected

### Requirement: Configure step
The configure step SHALL present a structured prompt form with three fields: Contexto, Código, and Pruebas. Each field SHALL have a label with terminal-style prefix (`$`). The form SHALL only enable submission when all fields are filled.

#### Scenario: User fills all prompt fields
- **WHEN** the user fills all three prompt fields
- **THEN** the "Generate Tests" button becomes enabled

#### Scenario: User submits prompt configuration
- **WHEN** the user clicks "Generate Tests" with all fields completed
- **THEN** the stepper advances to the Generating step and calls the AI generation API

### Requirement: Generating step
The generating step SHALL display an animated loading state during test generation with a spinner, typing text effect, and floating code particles (`{`, `}`, `[`, `]`, `(`, `)`). After generation completes, it SHALL transition to show the generated test code with a code viewer.

#### Scenario: Generation in progress
- **WHEN** the AI API is generating tests
- **THEN** the generating step shows a spinner, typing animation, and floating code particles

#### Scenario: Generation completes successfully
- **WHEN** the AI API returns test code successfully
- **THEN** the generated test code is displayed in a code viewer with syntax highlighting

### Requirement: Results step
The results step SHALL display test execution results (pass/fail badge, stdout, stderr), quality evaluation metrics (coverage ≥ 80%, mutation score ≥ 70%, failure detection ≥ 60%) in a table, and a report download button. Each metric SHALL show pass/fail status with color indicators.

#### Scenario: All metrics pass
- **WHEN** all quality metrics meet their thresholds
- **THEN** each metric shows a green checkmark and the overall status shows "All tests passed"

#### Scenario: A metric fails threshold
- **WHEN** a quality metric is below its threshold
- **THEN** that metric shows a red cross and an improvement prompt is generated

#### Scenario: User downloads report
- **WHEN** the user clicks "Download Report"
- **THEN** the system generates a PDF report and triggers a download
