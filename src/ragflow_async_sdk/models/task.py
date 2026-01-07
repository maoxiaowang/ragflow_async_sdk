# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ragflow_async_sdk.models.base import BaseEntity


@dataclass(slots=True)
class TaskStatus(BaseEntity):
    id: Optional[str] = None
    task_type: Optional[str] = None
    progress: Optional[float] = None
    progress_msg: Optional[str] = None
    begin_at: Optional[str] = None
    create_date: Optional[str] = None
    create_time: Optional[int] = None
    update_date: Optional[str] = None
    update_time: Optional[int] = None
    process_duration: Optional[float] = None
    retry_count: Optional[int] = None
    from_page: Optional[int] = None
    to_page: Optional[int] = None
    chunk_ids: Optional[str] = None
    digest: Optional[str] = None
    doc_id: Optional[str] = None

    __export_fields__ = (
        "id",
        "task_type",
        "progress",
        "progress_msg",
        "begin_at",
        "create_date",
        "create_time",
        "update_date",
        "update_time",
    )
