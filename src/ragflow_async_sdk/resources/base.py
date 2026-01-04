from enum import Enum
from typing import Any

from ..exceptions import RAGFlowAPIError
from ..http import AsyncHTTPClient


class BaseAPI:

    def __init__(
            self,
            client: AsyncHTTPClient,
            auto_parse_datetime=False
    ):
        self._client = client

    def _handle_stream_response(self, data: bytes):
        ...

    @staticmethod
    def _handle_response(response: dict[str, Any], require_data: bool = True) -> dict[str, Any]:
        if not isinstance(response, dict):
            raise RAGFlowAPIError(
                status_code=500,
                message="RAGFlow response is not a JSON object",
                details=response
            )

        code = response.get("code")
        if code != 0:
            raise RAGFlowAPIError(
                status_code=400,
                message=response.get("message", "Unknown RAGFlow error"),
                code=str(code),
                details=response
            )

        data = response.get("data")
        if data is None and require_data:
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