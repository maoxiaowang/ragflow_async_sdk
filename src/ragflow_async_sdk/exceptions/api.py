from __future__ import annotations

from typing import Any

from .base import RAGFlowError


class RAGFlowAPIError(RAGFlowError):
    """API returned an error response."""

    def __init__(
            self,
            *,
            status_code: int,
            message: str,
            code: str | None = None,
            details: Any | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
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
