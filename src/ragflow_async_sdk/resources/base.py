from typing import Dict, Any

from ragflow_async_sdk.exceptions import RAGFlowAPIError
from ragflow_async_sdk.http import AsyncHTTPClient


class BaseAPI:

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    @staticmethod
    def _clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in params.items() if v is not None}

    async def _handle_stream_response(self, data: bytes):
        ...

    @staticmethod
    async def _handle_response(data: Dict[str, Any]) -> Any:
        if not isinstance(data, dict):
            raise RAGFlowAPIError(status_code=500, message="RAGFlow response is not a JSON object")

        if data.get("code") != 0:
            raise RAGFlowAPIError(status_code=400, message=data.get("message", "Unknown RAGFlow error"))

        return data.get("data", {})
