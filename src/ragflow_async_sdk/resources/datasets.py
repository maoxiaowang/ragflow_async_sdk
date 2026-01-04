from typing import Optional, List, Tuple, Any

from .base import BaseAPI
from ..exceptions import RAGFlowValidationError
from ..models.dataset import DatasetRaw, Dataset
from ..types.ingestion import OrderBy, ChunkMethod
from ..types.permission import Permission

__all__ = [
    "DatasetAPI"
]


class DatasetAPI(BaseAPI):

    async def list(
            self,
            *,
            page: int = 1,
            page_size: int = 30,
            order_by: OrderBy = OrderBy.CREATE_TIME,
            desc: bool = True,
            id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> Tuple[List[Dataset], int]:
        params = {
            "page": page,
            "page_size": page_size,
            "orderBy": order_by,
            "desc": desc,
            "id": id,
            "name": name,
        }
        params = self._clean_params(params)

        resp = await self._client.get("/datasets", params=params)
        resp = await self._handle_response(resp)

        raw_items: List[DatasetRaw] = resp.get("data", [])
        total = resp.get("total", 0)

        datasets = [Dataset.from_raw(item) for item in raw_items]
        return datasets, total

    @staticmethod
    def _default_parser_config(method: ChunkMethod | str) -> dict:
        if method is ChunkMethod.NAIVE:
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

    async def create(
            self,
            name: str,
            *,
            chunk_method: ChunkMethod | str | None = None,
            parser_config: dict | None = None,
            parse_type: str | None = None,
            pipeline_id: str | None = None,
            description: str | None = None,
            avatar: str | None = None,
            permission: Permission = Permission.ME,
    ) -> Dataset:
        if isinstance(chunk_method, str):
            try:
                chunk_method = ChunkMethod(chunk_method)
            except ValueError:
                raise RAGFlowValidationError(
                    f"Invalid chunk_method: {chunk_method!r}. "
                    f"Allowed: {', '.join([m.value for m in ChunkMethod])}"
                )

        # ingestion mode validation
        if chunk_method is not None and (parse_type or pipeline_id):
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

        if chunk_method is not None and parser_config is None:
            parser_config = self._default_parser_config(chunk_method)

        payload: dict[str, Any] = {
            "name": name,
            "avatar": avatar,
            "description": description,
            "permission": permission.value,
        }

        if chunk_method is not None:
            payload["chunk_method"] =chunk_method.value
            payload["parser_config"] = parser_config or {}

        if parse_type is not None:
            payload["parse_type"] = parse_type
            payload["pipeline_id"] = pipeline_id

        payload = self._clean_params(payload)
        resp = await self._client.post("/datasets", json=payload)
        resp = await self._handle_response(resp)

        return Dataset.from_raw(resp)
