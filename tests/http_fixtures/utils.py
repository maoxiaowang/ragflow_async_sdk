import json
from typing import Any, Optional

import httpx


def _json_response(code: int = 0,  status: int = 200, **kwargs) -> httpx.Response:
    """
    For RAGFlow API responses, `code` is the only field that is always included.
    """
    payload = {
        "code": code,
        **kwargs,
    }

    return httpx.Response(
        status_code=status,
        json=payload,
        headers={"Content-Type": "application/json"},
    )


def _stream_response(content: bytes, status: int = 200) -> httpx.Response:
    return httpx.Response(
        status_code=status,
        content=content,
        headers={"Content-Type": "application/octet-stream"},
    )
