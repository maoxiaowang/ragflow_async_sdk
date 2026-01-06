import json
from enum import Enum
from typing import Any

from ..exceptions import RAGFlowAPIError
from ..http import AsyncHTTPClient


class BaseAPI:
    """
    Base class for all RAGFlow API modules.

    Provides core functionality for:
    - Storing the HTTP client
    - Normalizing request payloads
    - Validating and handling responses
    """

    def __init__(self, client: AsyncHTTPClient):
        """
        Initialize the API module with an HTTP client.

        Args:
            client: An instance of AsyncHTTPClient used for making requests.
        """
        self._client = client

    @staticmethod
    def _handle_response(
        response: dict[str, Any],
        *,
        require_data: bool = True,
    ) -> dict[str, Any]:
        """
        Validate and normalize a standard RAGFlow JSON response.

        This method should only be used for endpoints that return the standard format:
        {
            "code": 0,
            "data": ...
        }

        Args:
            response: The raw JSON response from the API.
            require_data: If True, raise an error if the 'data' field is missing.

        Returns:
            The validated response dict.

        Raises:
            RAGFlowAPIError: If the response is invalid, indicates a business error,
                             or the 'data' field is missing when required.
        """
        if not isinstance(response, dict):
            raise RAGFlowAPIError(
                status_code=500,
                message="Invalid RAGFlow response format (expected JSON object)",
                details=response,
            )

        code = response.get("code")

        if code != 0:
            raise RAGFlowAPIError(
                status_code=400,
                message=response.get("message", "RAGFlow API error"),
                code=str(code),
                details=response,
            )

        if require_data and "data" not in response:
            raise RAGFlowAPIError(
                status_code=500,
                message="RAGFlow response is empty",
                details=response
            )

        return response

    @staticmethod
    def _parse_sse_line(line: str) -> dict:
        """
        Parse a single Server-Sent Event (SSE) line into a dictionary.

        Strips the 'data:' prefix and parses JSON content.

        Args:
            line: A single SSE line from the server.

        Returns:
            Parsed dictionary.

        Raises:
            RAGFlowAPIError: If the line cannot be parsed as JSON.
        """
        if line.startswith("data:"):
            line = line[5:].strip()
        if not line:
            return {}
        try:
            return json.loads(line)
        except Exception as e:
            raise RAGFlowAPIError(
                message="Failed to parse SSE line as JSON",
                details=line,
                status_code=500,
            ) from e

    @staticmethod
    def _normalize_request(data: dict[str, Any]) -> dict[str, Any]:
        """
        Normalize a request payload by:
        - Removing None values
        - Converting Enums to their values
        - Recursively cleaning dicts and lists

        Args:
            data: Original request payload.

        Returns:
            Normalized dict suitable for sending to the API.
        """
        def normalize(value: Any) -> Any:
            if value is None:
                return None
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, dict):
                return {k: normalize(v) for k, v in value.items() if v is not None}
            if isinstance(value, (list, tuple)):
                return [normalize(v) for v in value if v is not None]
            return value

        return {k: normalize(v) for k, v in data.items() if v is not None}
