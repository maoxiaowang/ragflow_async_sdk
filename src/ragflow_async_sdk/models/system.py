# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

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
    )

    status: Optional[str] = None

    db: Optional[str] = None
    redis: Optional[str] = None
    doc_engine: Optional[str] = None

    storage: Optional[str] = None

    # detailed diagnostic info
    _meta: Optional[dict[str, Any]] = None
