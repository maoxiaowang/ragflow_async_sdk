from dataclasses import dataclass
from typing import Optional, List

from ..models.base import BaseEntity


@dataclass(slots=True)
class Chunk(BaseEntity):
    id: str
    dataset_id: str
    document_id: str
    content: str
    available: Optional[bool] = True
    docnm_kwd: Optional[str] = None  # document file name / keyword
    image_id: Optional[str] = None
    create_time: Optional[str] = None
    create_timestamp: Optional[float] = None
    important_keywords: Optional[List[str]] = None
    positions: Optional[List[str]] = None

    __export_fields__ = (
        "id",
        "dataset_id",
        "document_id",
        "content",
        "available",
        "docnm_kwd",
        "image_id",
        "create_time",
        "create_timestamp",
        "important_keywords",
    )
