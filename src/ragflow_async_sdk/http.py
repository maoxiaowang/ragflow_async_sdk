import logging
from typing import Optional, Callable, Awaitable, TypeVar

import httpx

from .exceptions.http import (
    RAGFlowTimeoutError, RAGFlowConnectionError, RAGFlowTransportError, RAGFlowHTTPResponseError
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


class AsyncHTTPClient:
    """Common Async HTTP Client"""

    def __init__(
            self,
            base_url: str,
            *,
            headers: Optional[dict] = None,
            timeout: float = 5.0,
            **kwargs,
    ):
        self.base_url = base_url.rstrip("/")
        kwargs.setdefault("trust_env", False)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers or {},
            timeout=timeout,
            **kwargs,
        )

    # -------------------------
    # internal helpers
    # -------------------------

    def _build_url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _build_headers(
            self,
            *,
            headers: Optional[dict] = None,
            with_auth: bool = True,
    ) -> dict:
        final_headers = dict(self._client.headers)

        if headers:
            final_headers.update(headers)

        if not with_auth:
            final_headers.pop("authorization", None)

        return final_headers

    @staticmethod
    async def _with_httpx_exceptions(
            coro: Callable[[], Awaitable[T]],
            *,
            method: str,
            url: str,
    ) -> T:
        """
        Translate httpx exceptions into SDK-level exceptions.
        """
        try:
            return await coro()
        except httpx.TimeoutException as e:
            raise RAGFlowTimeoutError(f"Timeout on {method} {url}") from e
        except httpx.ConnectError as e:
            raise RAGFlowConnectionError(f"Connection error on {method} {url}") from e
        except httpx.RequestError as e:
            raise RAGFlowTransportError(f"Transport error on {method} {url}") from e

    async def _send(
            self,
            request_coro: Callable[[], Awaitable[httpx.Response]],
            *,
            method: str,
            url: str,
            raise_for_status: bool = True,
    ) -> httpx.Response:
        """
        Send request and handle httpx + HTTP status errors.
        """
        async def wrapped():
            resp = await request_coro()
            if raise_for_status:
                resp.raise_for_status()
            return resp

        return await self._with_httpx_exceptions(
            wrapped,
            method=method,
            url=url,
        )

    # -------------------------
    # core request
    # -------------------------

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        files: Optional[list[tuple[str, tuple[str, bytes, Optional[str]]]]] = None,
        expect_json: bool = True,
        timeout: Optional[float] = None,
        with_auth: bool = True,
        headers: Optional[dict] = None,
        **kwargs,
) -> dict | httpx.Response:
        url = self._build_url(path)
        final_headers = self._build_headers(
            headers=headers,
            with_auth=with_auth,
        )

        resp = await self._send(
            lambda: self._client.request(
                method,
                url,
                params=params,
                json=json,
                files=files,
                headers=final_headers,
                timeout=timeout,
                **kwargs,
            ),
            method=method,
            url=url,
        )

        if not expect_json:
            return resp

        try:
            return resp.json()
        except Exception as e:
            raise RAGFlowHTTPResponseError(
                f"Failed to parse JSON from {method} {url}"
            ) from e

    async def close(self):
        await self._client.aclose()

    # -------------------------
    # HTTP verbs
    # -------------------------

    async def get(self, path: str, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs):
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs):
        return await self._request("DELETE", path, **kwargs)

    async def raw_get(
            self,
            path: str,
            *,
            headers: Optional[dict] = None,
            timeout: Optional[float] = None,
    ) -> httpx.Response:
        """
        Raw GET request, used for healthz or non-standard endpoints.
        """

        final_headers = self._build_headers(
            headers=headers,
        )

        return await self._send(
            lambda: self._client.get(
                path,
                headers=final_headers,
                timeout=timeout,
            ),
            method="GET",
            url=path,
            raise_for_status=False,
        )

    def stream(
            self,
            method: str,
            url: str,
            **kwargs,
    ):
        """
        Thin wrapper around httpx.AsyncClient.stream
        """
        return self._client.stream(method, url, **kwargs)
