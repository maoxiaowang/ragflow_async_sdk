from __future__ import annotations

from typing import Any


class RAGFlowError(Exception):
    """Base exception for RAGFlow Async SDK."""


# -------------------------
# Pre-request
# -------------------------

class RAGFlowConfigError(RAGFlowError):
    """Invalid SDK configuration."""


class RAGFlowValidationError(RAGFlowError):
    """Invalid RAGFlow validation error."""


# -------------------------
# Transport level
# -------------------------

class RAGFlowTransportError(RAGFlowError):
    """Network / transport related error."""

    def __init__(self, message: str, *, cause: Exception | None = None):
        super().__init__(message)
        self.__cause__ = cause


class RAGFlowTimeoutError(RAGFlowTransportError):
    """Request timeout."""


class RAGFlowConnectionError(RAGFlowTransportError):
    """Connection failed."""


# -------------------------
# API level
# -------------------------

class RAGFlowAPIError(RAGFlowError):
    """API returned an error response."""

    def __init__(
            self,
            *,
            status_code: int,
            message: str,
            code: str | None = None,
            request_id: str | None = None,
            details: Any | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.request_id = request_id
        self.details = details


class RAGFlowAuthError(RAGFlowAPIError):
    """401 / 403"""


class RAGFlowNotFoundError(RAGFlowAPIError):
    """404"""


class RAGFlowConflictError(RAGFlowAPIError):
    """409"""


class RAGFlowRateLimitError(RAGFlowAPIError):
    """429"""


class RAGFlowServerError(RAGFlowAPIError):
    """5xx"""


# -------------------------
# Response parsing
# -------------------------

class RAGFlowResponseError(RAGFlowError):
    """Invalid or unexpected API response."""
