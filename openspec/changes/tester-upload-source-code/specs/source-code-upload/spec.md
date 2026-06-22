## ADDED Requirements

### Requirement: Tester can upload a .py file via drag & drop

The system SHALL provide a drag & drop zone on the upload page that allows the tester to drag a single `.py` file from their file system. Dropping the file SHALL populate the upload area and display the filename. Dropping a file with an extension other than `.py` SHALL show an error message and reject the file.

#### Scenario: Successful drag & drop of .py file
- **WHEN** the tester drags a valid `.py` file onto the upload zone
- **THEN** the file is accepted and the filename is displayed in the upload area

#### Scenario: Drag & drop of non-.py file is rejected
- **WHEN** the tester drags a file with an extension other than `.py` onto the upload zone
- **THEN** an error message is displayed indicating only `.py` files are allowed

### Requirement: Tester can upload a .py file via file browser

The system SHALL provide a click-to-browse button that opens the native file explorer, allowing the tester to select a single `.py` file. Clicking the upload zone (when empty) SHALL also trigger the file explorer.

#### Scenario: Upload via file browser button
- **WHEN** the tester clicks the "Browse files" button
- **THEN** the native file explorer opens filtered to `.py` files

### Requirement: Upload captures file, project name, and prompt in one step

The upload form SHALL include three inputs: the file (drag & drop or browser), a text field for the project name, and a text area for the structured prompt. All three SHALL be required before submission.

#### Scenario: Complete upload with all fields
- **WHEN** the tester has dropped a `.py` file, entered a project name, and filled the prompt
- **AND** the tester clicks "Upload"
- **THEN** the file, project name, and prompt are sent to the backend

#### Scenario: Upload attempt with missing project name
- **WHEN** the tester has dropped a `.py` file and filled the prompt
- **AND** the project name field is empty
- **AND** the tester clicks "Upload"
- **THEN** the system shows a validation error: "Project name is required"

#### Scenario: Upload attempt with missing prompt
- **WHEN** the tester has dropped a `.py` file and entered a project name
- **AND** the prompt field is empty
- **AND** the tester clicks "Upload"
- **THEN** the system shows a validation error: "Prompt is required"

### Requirement: File size limit of 2 GB

The system SHALL reject any uploaded file larger than 2 GB before writing it to disk and SHALL display a clear error message to the tester.

#### Scenario: File exceeds maximum size
- **WHEN** the tester uploads a `.py` file larger than 2 GB
- **THEN** the system rejects the upload and displays "File exceeds the 2 GB limit"

### Requirement: Maximum one file at a time

The system SHALL only accept a single `.py` file per upload. If the tester drops or selects a new file while one is already present, the system SHALL replace the previous file.

#### Scenario: Replacing an existing file
- **WHEN** the tester has already added a `.py` file to the upload area
- **AND** the tester drops or selects a new `.py` file
- **THEN** the previous file is replaced by the new one

### Requirement: File is stored temporarily on disk and not persisted to database

The system SHALL store the uploaded file in a temporary directory (`/tmp/smartunittest/uploads/{sessionId}/`) and SHALL NOT persist it to the database. The file SHALL be removed when the tester leaves the page or closes the session.

#### Scenario: File stored in temp directory
- **WHEN** the tester successfully uploads a `.py` file
- **THEN** the file is written to `/tmp/smartunittest/uploads/{sessionId}/` with a sanitized name
- **AND** no record of the file content exists in the database

### Requirement: Automatic cleanup on session end

The system SHALL delete the temporary file and its session directory when the tester navigates away from the page or closes the browser. A backend cleanup task SHALL also remove files older than 1 hour as a safety net.

#### Scenario: Cleanup on page exit
- **WHEN** the tester closes the browser tab or navigates away
- **THEN** the frontend sends a cleanup request to `DELETE /api/v1/upload/source/{sessionId}`
- **AND** the backend removes the session directory and all files within

#### Scenario: Cleanup timeout for abandoned sessions
- **WHEN** a session directory has existed for more than 1 hour without activity
- **THEN** the backend cleanup task deletes it automatically

### Requirement: Uploaded file is forwarded to validation endpoint

After a successful upload and storage, the system SHALL automatically send the file to `POST /api/v1/validation/code` for syntax validation. The frontend SHALL display the validation result (success or error with details).

#### Scenario: Validation after successful upload
- **WHEN** the file is successfully uploaded and stored
- **THEN** the system forwards the file to `POST /api/v1/validation/code`
- **AND** the validation result is returned to the frontend

#### Scenario: Validation failure after upload
- **WHEN** the file uploads successfully but validation fails
- **THEN** the system displays the validation error to the tester
- **AND** the temporary file is deleted immediately
