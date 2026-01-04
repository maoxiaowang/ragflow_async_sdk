from dataclasses import dataclass
from typing import Optional, TypedDict, NotRequired, Dict, Any

__all__ = [
    'Dataset'
]



class DatasetRaw(TypedDict):
    """
    Raw dataset structure returned by RAGFlow API.
    This structure may change between API versions.
    """
    id: str
    name: str
    permission: str
    status: str

    avatar: NotRequired[str]
    description: NotRequired[str]
    language: NotRequired[str]

    # counts
    chunk_count: NotRequired[int]
    document_count: NotRequired[int]
    token_num: NotRequired[int]

    # ingestion / algo (volatile)
    chunk_method: NotRequired[str]
    parser_config: NotRequired[dict]
    embedding_model: NotRequired[str]
    similarity_threshold: NotRequired[float]
    vector_similarity_weight: NotRequired[float]

    # system
    tenant_id: NotRequired[str]
    created_by: NotRequired[str]

    # time
    create_time: NotRequired[int]
    update_time: NotRequired[int]
    create_date: NotRequired[str]
    update_date: NotRequired[str]


@dataclass(slots=True)
class Dataset:
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

    Raw = DatasetRaw

    @classmethod
    def from_raw(cls, raw: DatasetRaw) -> "Dataset":
        return cls(
            id=raw["id"],
            name=raw["name"],
            permission=raw["permission"],
            status=raw["status"],
            description=raw.get("description"),
            avatar=raw.get("avatar"),
            language=raw.get("language"),
            document_count=raw.get("document_count"),
            chunk_count=raw.get("chunk_count"),
            token_num=raw.get("token_num"),
            created_at=raw.get("create_time"),
            updated_at=raw.get("update_time"),
        )
