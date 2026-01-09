# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any

from .base import BaseEntity
from ..types.ingestion import ChunkMethod


@dataclass(slots=True)
class Document(BaseEntity):
    id: str
    dataset_id: str
    name: str
    type: str
    location: str
    status: Optional[str] = None
    run: Optional[str] = None
    suffix: Optional[str] = None
    size: Optional[int] = None
    created_by: Optional[str] = None
    create_date: Optional[str] = None
    create_time: Optional[int] = None
    update_date: Optional[str] = None
    update_time: Optional[int] = None

    chunk_method: Optional[ChunkMethod | str] = None
    chunk_count: Optional[int] = None
    token_count: Optional[int] = None
    parser_config: Optional[dict[str, Any]] = None
    meta_fields: Optional[dict[str, Any]] = None
    pipeline_id: Optional[str] = None
    thumbnail: Optional[str] = None

    progress: Optional[float] = None
    progress_msg: Optional[str] = None
    process_begin_at: Optional[str] = None
    process_duration: Optional[float] = None
    enabled: Optional[int] = None  # 1 available, 0 unavailable

    __export_fields__ = (
        "id",
        "dataset_id",
        "name",
        "type",
        "location",
        "status",
        "size",
        "created_by",
        "create_date",
        "create_time",
        "update_date",
        "update_time",
        "chunk_method",
        "chunk_count",
        "token_count",
        "thumbnail",
        "pipeline_id",
        "enabled",
    )
