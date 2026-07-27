## ADDED Requirements

### Requirement: POST /api/v1/tests/execute runs pytest as subprocess

The system SHALL expose an endpoint that invokes pytest as an isolated external OS process with a 60-second timeout.

#### Scenario: Successful test execution
- **WHEN** a POST request is sent to `/api/v1/tests/execute` with a valid `session_id`
- **THEN** the system SHALL run pytest on the uploaded source code
- **THEN** the system SHALL return a JSON response with `success: true`, `stdout`, `stderr`, and `exit_code`

#### Scenario: Timeout exceeds 60 seconds
- **WHEN** pytest execution exceeds 60 seconds
- **THEN** the system SHALL terminate the process
- **THEN** the system SHALL return a timeout error response

#### Scenario: Syntax error in test code
- **WHEN** the generated test code contains syntax errors
- **THEN** pytest SHALL report the errors in stderr
- **THEN** the system SHALL return the error details in the response

### Requirement: GET /api/v1/tests/{testId}/result retrieves execution result

The system SHALL allow retrieving a previously executed test result by ID.

#### Scenario: Retrieve existing result
- **WHEN** a GET request is sent to `/api/v1/tests/{testId}/result` with a valid test ID
- **THEN** the system SHALL return the stored execution result including status and output

#### Scenario: Test ID not found
- **WHEN** a GET request is sent with a non-existent test ID
- **THEN** the system SHALL return a 404 response

### Requirement: Isolated execution environment

The system SHALL execute tests in a controlled subprocess with resource limits.

#### Scenario: Subprocess isolation
- **WHEN** pytest is executed
- **THEN** it SHALL run as a separate OS process with its own memory space
- **THEN** the system SHALL enforce a 60-second timeout via `asyncio.wait_for` or equivalent
