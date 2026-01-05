from enum import Enum
from typing import Any

from ..exceptions import RAGFlowAPIError
from ..http import AsyncHTTPClient


class BaseAPI:
    """
    Base class for all RAGFlow API modules.
    Handles response validation and request normalization.
    """

    def __init__(
            self,
            client: AsyncHTTPClient,
    ):
        self._client = client

    def _handle_stream_response(self, data: bytes):
        """
        Handle streaming responses (SSE / chunked).
        Subclasses can override this method.
        """
        ...

    @staticmethod
    def _handle_response(
        response: dict[str, Any],
        *,
        require_data: bool = True,
    ) -> dict[str, Any]:
        """
        Validate and normalize a standard RAGFlow JSON response.

        This method should ONLY be used for endpoints that return:
        {
            "code": 0,
            "data": ...
        }
        """
        # Response must be a JSON object
        if not isinstance(response, dict):
            raise RAGFlowAPIError(
                status_code=500,
                message="Invalid RAGFlow response format (expected JSON object)",
                details=response,
            )

        code = response.get("code")

        # RAGFlow business error
        if code != 0:
            raise RAGFlowAPIError(
                status_code=400,
                message=response.get("message", "RAGFlow API error"),
                code=str(code),
                details=response,
            )

        # "data" field is required by default
        if require_data and "data" not in response:
            raise RAGFlowAPIError(
                status_code=500,
                message="RAGFlow response is empty",
                details=response
            )

        return response

    @staticmethod
    def _normalize_request(data: dict[str, Any]) -> dict[str, Any]:
        def normalize(value: Any) -> Any:
            if value is None:
                return None

            if isinstance(value, Enum):
                return value.value

            if isinstance(value, dict):
                return {
                    k: normalize(v)
                    for k, v in value.items()
                    if v is not None
                }

            if isinstance(value, (list, tuple)):
                return [normalize(v) for v in value if v is not None]

            return value

        return {
            k: normalize(v)
            for k, v in data.items()
            if v is not None
        }