from dataclasses import dataclass
from typing import Optional

from ..models.base import BaseEntity

__all__ = [
    'Dataset'
]


@dataclass(slots=True)
class Dataset(BaseEntity):
    id: str
    name: str
    permission: str
    status: str

    description: Optional[str] = None
    avatar: Optional[str] = None
    language: Optional[str] = None

    document_count: Optional[int] = None
    chunk_count: Optional[int] = None
    token_num: Optional[int] = None

    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    __export_fields__ = (
        "id",
        "name",
        "permission",
        "status",
        "description",
        "avatar",
        "language",
        "document_count",
        "chunk_count",
        "token_num",
        "created_at",
        "updated_at",
    )
