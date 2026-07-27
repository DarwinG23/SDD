## ADDED Requirements

### Requirement: POST /api/v1/evaluation/improvement-prompt generates improvement prompt

The system SHALL automatically generate an improvement prompt when quality thresholds are not met.

#### Scenario: Generate improvement prompt after failed evaluation
- **WHEN** the evaluation detects metrics below thresholds (RN1, RN2, or RN3)
- **THEN** the system SHALL construct a prompt for the AI service that includes the current test code and the specific metrics that failed
- **THEN** the system SHALL return the generated improvement prompt

### Requirement: POST /api/v1/ai/regenerate-tests regenerates tests

The system SHALL expose an endpoint to regenerate unit tests using the improvement prompt.

#### Scenario: Successful regeneration
- **WHEN** a POST request is sent to `/api/v1/ai/regenerate-tests` with a `session_id` and improvement prompt
- **THEN** the system SHALL invoke the AI service with the improvement prompt
- **THEN** the system SHALL return the regenerated test code

#### Scenario: Regeneration failure
- **WHEN** the AI service fails during regeneration
- **THEN** the system SHALL return an error with the failure details

### Requirement: Improvement cycle loop (RN5)

The system SHALL support up to a configured maximum number of improvement cycles.

#### Scenario: Multiple improvement cycles
- **WHEN** regenerated tests still fail quality thresholds
- **THEN** the system SHALL repeat the improvement cycle up to a maximum of 3 iterations

#### Scenario: Max cycles reached
- **WHEN** the maximum improvement cycles are exhausted without passing all thresholds
- **THEN** the system SHALL report the best achieved metrics in the final report
