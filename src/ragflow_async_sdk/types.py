from typing import TypedDict, Optional, Dict, Any, List


class Dataset(TypedDict):
    id: str
    name: str
    description: Optional[str]
    permission: str
    chunk_method: str
    embedding_model: str
    parser_config: Optional[Dict[str, Any]]
    created_at: str
