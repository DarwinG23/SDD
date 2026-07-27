## ADDED Requirements

### Requirement: POST /api/v1/reports/generate compiles metrics report

The system SHALL compile all evaluation metrics, test results, and improvement cycle data into a report entity.

#### Scenario: Generate report after evaluation
- **WHEN** a POST request is sent to `/api/v1/reports/generate` with a valid `evaluation_id`
- **THEN** the system SHALL compile coverage, mutation score, and failure detection metrics
- **THEN** the system SHALL include any improvement prompts generated during the cycle
- **THEN** the system SHALL return a JSON with `report_id` and status

### Requirement: GET /api/v1/reports/{reportId}/download returns PDF

The system SHALL generate and serve a PDF report with all results.

#### Scenario: Download PDF report
- **WHEN** a GET request is sent to `/api/v1/reports/{reportId}/download`
- **THEN** the system SHALL generate a PDF document
- **THEN** the response SHALL have Content-Type `application/pdf`

#### Scenario: Report includes all metrics
- **WHEN** the PDF is generated
- **THEN** it SHALL include code coverage percentage, mutation score, failure detection rate
- **THEN** it SHALL include pass/fail status for each threshold
- **THEN** it SHALL include improvement recommendations if applicable (RN6)

#### Scenario: Report ID not found
- **WHEN** a GET request is sent with a non-existent report ID
- **THEN** the system SHALL return a 404 response
