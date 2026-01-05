from dataclasses import dataclass
from typing import Any, Dict, Optional

from .base import BaseEntity


@dataclass
class SystemHealth(BaseEntity):
    """
    System health status.
    """

    __export_fields__ = (
        "status",
        "db",
        "redis",
        "doc_engine",
        "storage",
        "_meta",
    )

    status: Optional[str] = None

    db: Optional[str] = None
    redis: Optional[str] = None
    doc_engine: Optional[str] = None

    storage: Optional[str] = None

    # detailed diagnostic info
    _meta: Optional[Dict[str, Any]] = None
