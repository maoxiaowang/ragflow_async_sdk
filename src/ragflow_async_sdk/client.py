# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from typing import Optional

from .apis import (
    DatasetAPI,
    DocumentAPI,
    ChunkAPI,
    ChatAPI,
    AgentAPI,
    SessionAPI,
    FileAPI,
    SystemAPI
)
from .exceptions import RAGFlowConfigError
from .http import AsyncHTTPClient


class AsyncRAGFlowClient:
    """RAGFlow async SDK top-level client."""

    def __init__(
        self,
        server_url: str,
        api_key: str,
        timeout: float = 5.0,
        api_version: str = "v1",
        _http_client: Optional[AsyncHTTPClient] = None,
        _raw_http_client: Optional[AsyncHTTPClient] = None,
        **kwargs,
    ):
        if api_version not in ("v1",):
            raise RAGFlowConfigError("API version only supports v1 now")
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        base_url = f'{server_url.rstrip()}/api/{api_version}'
        self._http = _http_client or AsyncHTTPClient(base_url, headers=headers, timeout=timeout, **kwargs)
        self._raw_http = _raw_http_client or AsyncHTTPClient(server_url, headers={}, timeout=timeout, **kwargs)

        # Resource
        self.datasets = DatasetAPI(self._http)
        self.documents = DocumentAPI(self._http)
        self.chunks = ChunkAPI(self._http)
        self.chats = ChatAPI(self._http)
        self.sessions = SessionAPI(self._http)
        self.agents = AgentAPI(self._http)
        self.systems = SystemAPI(self._raw_http)
        self.files = FileAPI(self._http)

    async def close(self):
        await self._http.close()
        await self._raw_http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
