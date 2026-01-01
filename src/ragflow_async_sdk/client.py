from .exceptions import (
    RAGFlowConfigError,
)
from .http import AsyncHTTPClient
from .resources.datasets import DatasetAPI


class AsyncRAGFlowClient:
    """RAGFlow async SDK top-level client."""

    def __init__(self, base_url: str, api_key: str, timeout: float = 10.0, api_version: str = "v1", **kwargs):
        if api_version not in ("v1",):
            raise RAGFlowConfigError("API version only supports v1 now")
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        base_url = f'{base_url.rstrip()}/api/{api_version}'
        self._http = AsyncHTTPClient(base_url, headers=headers, timeout=timeout, **kwargs)

        # Resource
        self.datasets = DatasetAPI(self._http)

    async def close(self):
        await self._http.close()
