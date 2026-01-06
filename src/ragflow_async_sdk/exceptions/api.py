from typing import Any

from .base import RAGFlowError


class RAGFlowAPIError(RAGFlowError):
    """API returned an error response."""

    default_status_code = 400

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
        details: Any | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code or self.default_status_code
        self.code = code
        self.details = details


class RAGFlowAuthError(RAGFlowAPIError):
    """401 / 403"""
    default_status_code = 401


class RAGFlowNotFoundError(RAGFlowAPIError):
    """404"""
    default_status_code = 404


class RAGFlowConflictError(RAGFlowAPIError):
    """409"""
    default_status_code = 409


class RAGFlowRateLimitError(RAGFlowAPIError):
    """429"""
    default_status_code = 429


class RAGFlowResponseError(RAGFlowAPIError):
    """Invalid or unexpected API response."""
    default_status_code = 500