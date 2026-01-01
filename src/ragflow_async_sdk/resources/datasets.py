from enum import Enum
from typing import Optional, List, Tuple, Dict, Any, TypedDict

from .base import BaseAPI
from ..exceptions import RAGFlowValidationError
from ..types import Dataset

__all__ = [
    "DatasetAPI"
]


class ChunkMethod(str, Enum):
    NAIVE = "naive"
    BOOK = "book"
    EMAIL = "email"
    LAWS = "laws"
    MANUAL = "manual"
    ONE = "one"
    PAPER = "paper"
    PICTURE = "picture"
    PRESENTATION = "presentation"
    QA = "qa"
    TABLE = "table"
    TAG = "tag"


class RaptorConfig(TypedDict, total=False):
    use_raptor: bool


class GraphRagConfig(TypedDict, total=False):
    use_graphrag: bool


class NaiveParserConfig(TypedDict, total=False):
    auto_keywords: int
    auto_questions: int
    chunk_token_num: int
    delimiter: str
    html4excel: bool
    layout_recognize: str
    tag_kb_ids: List[str]
    task_page_size: int
    raptor: RaptorConfig
    graphrag: GraphRagConfig


# 其他 chunk_method 用的
class SimpleParserConfig(TypedDict, total=False):
    raptor: RaptorConfig

class Permission(str, Enum):
    ME = "me"
    TEAM = "team"


class DatasetAPI(BaseAPI):

    async def list(
            self,
            *,
            page: int = 1,
            page_size: int = 30,
            order_by: str = "create_time",
            desc: bool = True,
            id: Optional[int] = None,
            name: Optional[str] = None,
    ) -> Tuple[List[Dataset], int]:
        params = {"page": page, "page_size": page_size, "orderBy": order_by, "desc": desc, "id": id, "name": name}
        params = self._clean_params(params)
        resp = await self._client.get("/datasets", params=params)

        return (
            resp.get("data", []),
            resp.get("total_datasets", 0),
        )

    async def create(
            self,
            name: str,
            *,
            chunk_method: Optional[ChunkMethod|str] = None,
            parser_config: Optional[dict] = None,
            parse_type: Optional[str] = None,
            pipeline_id: Optional[str] = None,
            description: Optional[str] = None,
            avatar: Optional[str] = None,
            permission: Optional[Permission|str] = None,
    ) -> Dataset:
        """
        Create a dataset.

        You can choose ONE ingestion mode:
        - Built-in chunking: specify chunk_method (optional parser_config)
        - Ingestion pipeline: specify both parse_type and pipeline_id

        If none is provided, defaults to chunk_method = "naive".
        """

        def default_parser_config(method) -> dict:
            if method == ChunkMethod.NAIVE:
                return {
                    "chunk_token_num": 512,
                    "delimiter": "\n",
                    "raptor": {"use_raptor": False},
                    "graphrag": {"use_graphrag": False},
                }

            if method in {
                ChunkMethod.QA,
                ChunkMethod.MANUAL,
                ChunkMethod.PAPER,
                ChunkMethod.BOOK,
                ChunkMethod.LAWS,
                ChunkMethod.PRESENTATION,
            }:
                return {"raptor": {"use_raptor": False}}

            # table / picture / one / email / tag
            return {}

        # ingestion mode validation
        if chunk_method and (parse_type or pipeline_id):
            raise RAGFlowValidationError(
                "chunk_method is mutually exclusive with parse_type and pipeline_id"
            )

        if (parse_type is None) ^ (pipeline_id is None):
            raise RAGFlowValidationError(
                "parse_type and pipeline_id must be provided together"
            )

        # default behavior
        if chunk_method is None and parse_type is None:
            chunk_method = ChunkMethod.NAIVE

        # parser_config default
        if chunk_method and parser_config is None:
            parser_config = default_parser_config(chunk_method)

        payload = {
            "name": name,
            "avatar": avatar,
            "description": description,
            "permission": permission.value if permission else None,
        }

        if chunk_method:
            payload["chunk_method"] = chunk_method.value
            payload["parser_config"] = parser_config or {}

        if parse_type:
            payload["parse_type"] = parse_type
            payload["pipeline_id"] = pipeline_id

        payload = self._clean_params(payload)

        resp = await self._client.post("/datasets", json=payload)
        resp = await self._handle_response(resp)

        return resp
