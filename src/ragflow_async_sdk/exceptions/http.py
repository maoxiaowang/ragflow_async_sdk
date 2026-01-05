from .base import RAGFlowError


class RAGFlowHTTPError(RAGFlowError):
    """Base HTTP client error"""


class RAGFlowTimeoutError(RAGFlowHTTPError):
    """Request timeout."""


class RAGFlowConnectionError(RAGFlowHTTPError):
    """Connection failed."""


class RAGFlowTransportError(RAGFlowHTTPError):
    """Network / transport error."""


class RAGFlowHTTPResponseError(RAGFlowHTTPError):
    """Invalid or non-JSON HTTP response."""
