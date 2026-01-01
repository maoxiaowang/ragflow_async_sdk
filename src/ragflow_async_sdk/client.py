from typing import Optional, Dict, Any
from urllib.parse import urljoin

from .http import AsyncHTTPClient
from ..exceptions import (
    RAGFlowError,
    RAGFlowAPIError,
    RAGFlowAuthError,
    RAGFlowNotFoundError,
    RAGFlowResponseError,
)
from ..resources.datasets import DatasetAPI

class AsyncRAGFlowClient:
    """RAGFlow 异步 SDK 顶层客户端"""
    def __init__(self, base_url: str, api_key: str, timeout: float = 10.0):
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        self._http = AsyncHTTPClient(base_url, headers=headers, timeout=timeout)

        # Resource API
        self.datasets = DatasetAPI(self._http)

    async def _handle_response(self, data: Dict[str, Any]) -> Any:
        """
        根据 RAGFlow 响应解析业务 code
        """
        if not isinstance(data, dict):
            raise RAGFlowResponseError("RAGFlow response is not a JSON object")

        if data.get("code") != 0:
            raise RAGFlowAPIError(data.get("message", "Unknown error"), payload=data)

        return data.get("data", {})

    async def close(self):
        await self._http.close()
