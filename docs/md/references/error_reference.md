# Error Reference

The RAGFlow SDK provides a set of exceptions to handle errors and validation issues in a consistent way. 
These exceptions help developers catch problems during API calls, data validation, or network/transport issues.

## Base API Error
`RAGFlowAPIError` is the base class for all API-related errors. It is raised whenever the server returns an error response.

| Exception | Description |
|-----------|-------------|
| `RAGFlowAuthError` | Raised when authentication with the RAGFlow server fails (e.g., invalid API key or expired token). |
| `RAGFlowNotFoundError` | Raised when a requested resource (dataset, document, session, etc.) does not exist. |
| `RAGFlowConflictError` | Raised when multiple resources are returned for a query that expects a single result. |
| `RAGFlowRateLimitError` | Raised when the server rejects a request due to exceeding rate limits. |
| `RAGFlowResponseError` | Raised when the server response is invalid, cannot be parsed as JSON, or contains unexpected data. |

**Usage Example:**

```python
from ragflow_async_sdk.exceptions import RAGFlowAPIError

try:
    dataset = await client.datasets.get_dataset(dataset_id="123")
except RAGFlowAPIError as e:
    print("API error:", e)
```

**Notes:**
- Contains attributes such as `code` and `message` from the server response.
- All other API-specific errors inherit from this base class.

## Validation Errors
Validation errors are raised when input parameters fail checks before sending requests to the server.

**Usage Example:**

```python
from ragflow_async_sdk.exceptions import RAGFlowValidationError

try:
    await client.datasets.get_dataset()
except RAGFlowValidationError as ve:
    print("Validation failed:", ve)

```
**Common cases:**
- Required parameters missing.
- Conflicting parameters provided.
- Invalid types or values.

## Configuration Errors
`RAGFlowConfigError` is raised when the SDK configuration is invalid or incomplete, such as missing `server_url` or `api_key`.

## Transport Level Errors
These exceptions handle network or request-level issues such as connectivity problems, timeouts, or invalid HTTP responses.

| Exception | Description |
|-----------|-------------|
| `RAGFlowTimeoutError` | Raised when an API request times out. |
| `RAGFlowConnectionError` | Raised when the client cannot connect to the server. |
| `RAGFlowTransportError` | Raised for generic transport-level errors (network, HTTP library issues). |
| `RAGFlowResponseError` | Raised when an HTTP response is invalid or cannot be parsed as JSON. |

**Usage Example:**

```python
from ragflow_async_sdk.exceptions import (
    RAGFlowTimeoutError,
    RAGFlowConnectionError,
    RAGFlowTransportError,
    RAGFlowHTTPResponseError,
)

try:
    dataset = await client.datasets.get_dataset(dataset_id="123")
except (RAGFlowTimeoutError, RAGFlowConnectionError) as e:
    print("Network error:", e)
except RAGFlowTransportError as te:
    print("Transport error:", te)
except RAGFlowHTTPResponseError as he:
    print("Invalid HTTP response:", he)
```

**Notes:**
- These exceptions are typically caused by network issues, misconfigured server URLs, or server-side errors.
- They allow developers to implement retries or alternative flows when communication fails.