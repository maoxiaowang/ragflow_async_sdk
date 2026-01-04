import logging
from typing import Optional, List, Tuple, Dict

import httpx
from httpx import Response

logger = logging.getLogger(__name__)


class HTTPClientError(Exception):
    """Base HTTP client error"""


class HTTPTimeoutError(HTTPClientError):
    pass


class HTTPConnectionError(HTTPClientError):
    pass


class HTTPTransportError(HTTPClientError):
    pass


class HTTPResponseError(HTTPClientError):
    pass


class AsyncHTTPClient:
    """通用异步 HTTP 客户端，封装 httpx.AsyncClient"""

    def __init__(self, base_url: str, *, headers: Optional[dict] = None, timeout: float = 10.0, **kwargs):
        self.base_url = base_url.rstrip("/")
        kwargs.setdefault("trust_env", False)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers or {},
            timeout=timeout,
            **kwargs
        )

    def _build_url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    async def _request(
            self,
            method: str,
            path: str,
            *,
            params: Optional[dict] = None,
            json: Optional[dict] = None,
            files: Optional[List[Tuple[str, Tuple[str, bytes, Optional[str]]]]] = None,
            expect_json: bool = True,
            timeout: Optional[float] = None,
            **kwargs,
    ) -> Dict | Response:
        url = self._build_url(path)

        try:
            resp = await self._client.request(
                method, url, params=params, json=json, files=files, timeout=timeout, **kwargs
            )
            resp.raise_for_status()
        except httpx.TimeoutException as e:
            raise HTTPTimeoutError(f"Timeout on {method} {url}") from e
        except httpx.ConnectError as e:
            raise HTTPConnectionError(f"Connection error on {method} {url}") from e
        except httpx.RequestError as e:
            raise HTTPTransportError(f"Transport error on {method} {url}") from e

        if not expect_json:
            return resp
        try:
            return resp.json()
        except Exception as e:
            raise HTTPResponseError(f"Failed to parse JSON from {method} {url}") from e

    # HTTP verbs
    async def get(self, path: str, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs):
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs):
        return await self._request("DELETE", path, **kwargs)

    async def close(self):
        await self._client.aclose()
