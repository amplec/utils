# AMPLEC Utilities
The `utils` repository of the `amplec` organisation houses all the utilities, shared functions and logging mechanisms that are used all across the AMPLEC project.

## Features (WIP)

### Logger Class

The `Logger` class provides a custom logging implementation tailored for the AMPLEC project. It shares functional similarities with Python's built-in `logging.Logger` but offers a simplified design with added custom behavior, such as tracking the call hierarchy. This class is subject to change as the AMPLEC project evolves.

#### Key Features and Differences from `logging.Logger`

1. **Logging Modes**  
   - Supports three modes: `console`, `elastic`, and `dual` (both console and ElasticSearch).  
   - If the mode is `elastic` or `dual`, an ElasticSearch URL and API key must be provided.  
   - This differs from `logging.Logger`, which uses configurable handlers (e.g., file handlers, stream handlers) to manage outputs.

2. **Call Hierarchy Tracking**  
   - Includes a `_get_call_tree` method that appends the call hierarchy to log messages, providing insights into the execution path.  
   - This feature is not present in `logging.Logger`.

3. **Simplified Log Levels**  
   - Supports `info`, `warning`, `error`, and `debug`.  
   - No built-in configurability for additional levels, handlers, or formatting options.

4. **Output Behavior**  
   - Directly prints to the console, indexes into an ElasticSearch instance, or does both, depending on the selected mode.  
   - This differs from `logging.Logger`, which relies on handlers for more granular control over outputs.

#### Limitations

- Does not support advanced features like log rotation, custom formatters, or third-party integrations available in `logging.Logger`.  
- Log levels and output formats are statically implemented.

### SimplePersistence Class

The `SimplePersistence` class provides a straightforward mechanism for managing submission data. It supports storing, loading, and cleaning up submission files while maintaining metadata.

#### Features
1. **Initialization**:
   - Creates a base directory and metadata file (`metadata.json`) for submissions if they do not exist.
   - Logs operations via a provided `Logger` instance.

2. **Storing Submissions**:
   - Saves submission data to a `.txt` file.
   - Updates the `metadata.json` with submission details, including the indexing date.
   - Performs automatic cleanup of old submissions.

3. **Loading Submissions**:
   - Retrieves submission data and metadata by ID.
   - Provides an option to load only the payload (content).

4. **Automatic Cleanup**:
   - Deletes submissions older than a specified number of days (default: 28 days).
   - Updates the metadata file accordingly.

#### Key Methods
- `store_submission(submission_id: str, payload: list[str])`: Stores a submission and updates metadata.
- `load_submission(submission_id: str)`: Loads both payload and metadata for a submission.
- `load_only_payload(submission_id: str)`: Retrieves only the payload for a submission.
- `cleanup_submissions(older_than_days: int = 28)`: Removes submissions older than the specified duration.
- `_load_metadata()`: Loads metadata from `metadata.json`.
- `_save_metadata(metadata: dict)`: Saves the metadata dictionary to `metadata.json`.



*More will be added as the project progresses*
