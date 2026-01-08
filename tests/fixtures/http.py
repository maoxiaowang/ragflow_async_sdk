import logging
from typing import Any, Callable, Awaitable, AsyncIterator, Optional
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)

class FakeAsyncClient:
    """
    Fake async HTTP client for SDK tests.

    Features:
    - Intercepts HTTP requests
    - Dispatches to registered route handlers
    - Records calls for assertions
    """

    def __init__(self, server_url):
        self.headers: dict[str, str] = {}
        self.calls: list[dict[str, Any]] = []
        self.server_url = server_url

        # (METHOD, URL) -> async handler(**kwargs) -> httpx.Response
        self.routes: dict[
            tuple[str, str],
            Callable[..., Awaitable[httpx.Response]],
        ] = {}

    # -------------------------
    # Route registration
    # -------------------------
    def route(self, method: str, url: str, handler: Callable[..., Awaitable[httpx.Response]]) -> None:
        """Register a fake route."""
        self.routes[(method.upper(), url)] = handler

    # -------------------------
    # Core request
    # -------------------------
    async def request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        files: Optional[list[tuple[str, tuple[str, bytes, Optional[str]]]]] = None,
        expect_json: bool = True,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict | httpx.Response:
        """Intercept request, match template route, call handler, return dict."""
        request_kwargs = {
            "method": method.upper(),
            "url": url,
            "params": params,
            "json": json,
            "files": files,
            "expect_json": expect_json,
            "data": data,
            "headers": headers,
            "timeout": timeout,
        }
        self.calls.append(request_kwargs)

        for (m, template), handler in self.routes.items():
            if m != method.upper():
                continue

            template_parts = template.strip("/").split("/")
            url_parts = urlparse(url).path.strip("/").split("/")

            if len(template_parts) != len(url_parts):
                continue

            path_params = {}
            matched = True
            for t, u in zip(template_parts, url_parts):
                if t.startswith("{") and t.endswith("}"):
                    key = t[1:-1]
                    path_params[key] = u
                elif t != u:
                    matched = False
                    break

            if matched:
                # Call HTTP fixtures
                result = await handler(
                    **request_kwargs,
                    **path_params,
                )
                if isinstance(result, httpx.Response):
                    if expect_json:
                        try:
                            return result.json()
                        except Exception as e:
                            raise RuntimeError(f"Mocked httpx.Response cannot be parsed as JSON: {e}")
                    return result

                if isinstance(result, dict):
                    return result

                raise TypeError(f"Mock handler must return dict or httpx.Response with JSON, got {type(result)}")

        # No routes found error
        w0 = max(len(k[0]) for k, _ in self.routes.items())
        w1 = max(len(k[1]) for k, _ in self.routes.items()) + 2

        for key, value in self.routes.items():
            logger.debug(f"[{key[0]:<{w0}}] {key[1]:<{w1}}: {value.__name__}")
        raise AssertionError(f"No mock route matched for {method.upper()} {url}")

    # -------------------------
    # Convenience methods
    # -------------------------
    async def get(self, url: str, **kwargs):
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs):
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs):
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs):
        return await self.request("DELETE", url, **kwargs)

    def stream(self, *args, **kwargs) -> AsyncIterator[httpx.Response]:
        """Placeholder for streaming support (not implemented)."""
        raise NotImplementedError("stream is not mocked yet")

    @staticmethod
    async def close() -> None:
        """Async no-op close for compatibility."""
        return None
