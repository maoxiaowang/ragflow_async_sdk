# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from pathlib import Path
from urllib.parse import urlparse, unquote

import mimetypes

import httpx


async def file_from_path(
    path: str | Path,
    *,
    filename: str | None = None,
    content_type: str | None = None,
) -> tuple[str, bytes, str]:
    """
    Create a file upload tuple from a local file path.

    The returned tuple is compatible with multipart/form-data uploads:
    (filename, file_bytes, content_type).

    This function does not catch any exceptions raised during file reading.

    Args:
        path: Path to the local file.
        filename: Optional override for the uploaded filename.
                  Defaults to the basename of the path.
        content_type: Optional MIME type of the file.

    Returns:
        A tuple of (filename, file_bytes, content_type).

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be accessed.
        IsADirectoryError: If the path points to a directory.
        OSError: For other file I/O related errors.
    """
    try:
        import aiofiles
    except ImportError as e:
        raise RuntimeError(
            "file_from_path requires optional dependency 'aiofiles'. "
            "Install it with: pip install aiofiles"
        ) from e

    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(p)
    if p.is_dir():
        raise IsADirectoryError(p)

    async with aiofiles.open(p, "rb") as f:
        content = await f.read()

    final_name = filename or p.name
    final_type = (
        content_type
        or mimetypes.guess_type(final_name)[0]
        or "application/octet-stream"
    )

    return final_name, content, final_type


def file_from_bytes(
    filename: str,
    content: bytes,
    content_type: str | None = None,
) -> tuple[str, bytes, str]:
    """
    Create a file upload tuple from raw bytes.

    Args:
        filename: Filename to use for upload.
        content: File content as bytes.
        content_type: Optional MIME type.

    Returns:
        A tuple of (filename, file_bytes, content_type).

    Raises:
        TypeError: If content is not bytes-like.
    """
    if not isinstance(content, (bytes, bytearray)):
        raise TypeError("content must be bytes or bytearray")

    return (
        filename,
        bytes(content),
        content_type or "application/octet-stream",
    )


async def file_from_url(
    url: str,
    *,
    filename: str | None = None,
    content_type: str | None = None,
) -> tuple[str, bytes, str]:
    """
    Download a file from a URL and create a file upload tuple.

    Args:
        url: File URL.
        filename: Optional override for the uploaded filename.
        content_type: Optional MIME type.

    Returns:
        A tuple of (filename, file_bytes, content_type).

    Raises:
        httpx.RequestError: For network-related errors.
        httpx.HTTPStatusError: For non-2xx HTTP responses.
        ValueError: If filename cannot be inferred.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

    parsed = urlparse(url)
    inferred_name = Path(parsed.path).name
    final_name = filename or inferred_name

    if not final_name:
        raise ValueError("filename cannot be inferred from URL, please specify it explicitly")

    final_type = (
        content_type
        or resp.headers.get("content-type")
        or mimetypes.guess_type(final_name)[0]
        or "application/octet-stream"
    )

    return final_name, resp.content, final_type


def parse_content_disposition(header: str, default: str) -> str:
    """
    Parse the filename from a Content-Disposition HTTP header.

    Supports two formats:
    - Standard: filename="example.pdf"
    - RFC 5987: filename*=UTF-8''example.pdf

    Args:
        header: The Content-Disposition header from the HTTP response.
        default: The default filename to return if parsing fails.

    Returns:
        The parsed filename as a string.
    """
    if not header:
        return default

    for part in header.split(";"):
        part = part.strip()
        if part.startswith("filename*="):
            # RFC 5987 format
            return unquote(part.split("''")[-1].strip())
        elif part.startswith("filename="):
            # Standard format
            return part.split("=")[-1].strip().strip('"')
    return default
