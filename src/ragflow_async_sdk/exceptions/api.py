# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from typing import Any

from .base import RAGFlowError


class RAGFlowAPIError(RAGFlowError):
    """API returned an error response."""

    default_status_code = 400
    default_message = "An API error occurred."

    def __init__(
        self,
        message: str | None = None,
        *,
        status_code: int | None = None,
        code: str | None = None,
        details: Any | None = None,
    ):
        super().__init__(message or self.default_message)
        self.status_code = status_code or self.default_status_code
        self.code = code
        self.details = details


class RAGFlowAuthError(RAGFlowAPIError):
    """401 / 403"""
    default_status_code = 401
    default_message = "Authentication failed."


class RAGFlowNotFoundError(RAGFlowAPIError):
    """404"""
    default_status_code = 404
    default_message = "Resource not found."


class RAGFlowConflictError(RAGFlowAPIError):
    """409"""
    default_status_code = 409
    default_message = "Resource conflict occurred."


class RAGFlowRateLimitError(RAGFlowAPIError):
    """429"""
    default_status_code = 429
    default_message = "Rate limit exceeded."


class RAGFlowResponseError(RAGFlowAPIError):
    """Invalid or unexpected API response."""
    default_status_code = 500
    default_message = "Invalid or unexpected API response."
