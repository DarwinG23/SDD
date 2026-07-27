## ADDED Requirements

### Requirement: POST /api/v1/evaluation/run computes quality metrics

The system SHALL expose an endpoint that runs coverage analysis, mutation testing, and failure detection on executed tests.

#### Scenario: Full evaluation run
- **WHEN** a POST request is sent to `/api/v1/evaluation/run` with a valid `test_id` and `source_id`
- **THEN** the system SHALL compute code coverage using coverage.py
- **THEN** the system SHALL compute mutation score using mutmut
- **THEN** the system SHALL compute failure detection rate
- **THEN** the system SHALL return a JSON response with all three metrics

#### Scenario: Coverage below threshold (RN1)
- **WHEN** the code coverage is below 80%
- **THEN** the system SHALL mark the evaluation as failing RN1

#### Scenario: Mutation score below threshold (RN2)
- **WHEN** the mutation score is below 70%
- **THEN** the system SHALL mark the evaluation as failing RN2

#### Scenario: Failure detection below threshold (RN3)
- **WHEN** the failure detection rate is below 60%
- **THEN** the system SHALL mark the evaluation as failing RN3

### Requirement: GET /api/v1/evaluation/{evaluationId} retrieves metrics

The system SHALL allow retrieving stored evaluation results by ID.

#### Scenario: Retrieve existing evaluation
- **WHEN** a GET request is sent to `/api/v1/evaluation/{evaluationId}` with a valid evaluation ID
- **THEN** the system SHALL return the full metrics and pass/fail status for each threshold

#### Scenario: Evaluation not found
- **WHEN** a GET request is sent with a non-existent evaluation ID
- **THEN** the system SHALL return a 404 response

### Requirement: Threshold-based pass/fail determination

The system SHALL determine quality pass/fail based on business rules RN1, RN2, RN3.

#### Scenario: All thresholds met
- **WHEN** coverage >= 80% AND mutation >= 70% AND failure detection >= 60%
- **THEN** the evaluation SHALL be marked as passed

#### Scenario: Any threshold not met
- **WHEN** any metric is below its threshold
- **THEN** the evaluation SHALL be marked as failed
- **THEN** the system SHALL trigger improvement cycle generation
