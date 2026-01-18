# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from typing import Optional
from urllib.parse import urlparse

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
    """
    The RAGFlow asynchronous SDK top-level client. This client provides
    access to all RAGFlow resources in an async manner.

    Args:
        server_url (str): The base URL of the RAGFlow server.
        api_key (str): API key for authentication.
        timeout (float, optional): HTTP request timeout in seconds. Defaults to 5.0.
        api_version (str, optional): API version to use. Currently only "v1" is supported. Defaults to "v1".
        **kwargs: Additional keyword arguments passed to HTTP client constructors.

    Attributes:
        datasets (DatasetAPI): Interface for dataset operations.
        documents (DocumentAPI): Interface for document operations.
        chunks (ChunkAPI): Interface for chunk operations.
        chats (ChatAPI): Interface for chat operations.
        sessions (SessionAPI): Interface for session operations.
        agents (AgentAPI): Interface for agent operations.
        systems (SystemAPI): Interface for system operations.
        files (FileAPI): Interface for file operations.

    Raises:
        RAGFlowConfigError: If the `server_url` is invalid or `api_version` is unsupported.

    Examples:
        ::

            import asyncio
            from ragflow_async_sdk import AsyncRAGFlowClient

            async def main():
                async with AsyncRAGFlowClient(
                    server_url="http://your-ragflow-address",
                    api_key="YOUR_API_KEY",
                ) as client:
                    # Example: Health check
                    system_health = await client.systems.healthz()
                    print(system_health.status)

            # Run the async main function
            asyncio.run(main())
    """
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
        # server URL verification
        parsed = urlparse(server_url)
        if not parsed.scheme or not parsed.netloc:
            raise RAGFlowConfigError(
                f"Invalid server_url: {server_url!r}. "
                "Please provide a valid URL (including scheme, e.g., http:// or https://)."
            )
        self.server_url = server_url.rstrip("/")

        # API version check
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
