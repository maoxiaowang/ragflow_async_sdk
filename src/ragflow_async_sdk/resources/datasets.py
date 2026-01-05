from typing import Optional, Any, List, Dict, Tuple

from .base import BaseAPI
from ..exceptions import RAGFlowValidationError, RAGFlowAPIError
from ..models.dataset import Dataset, KnowledgeGraph
from ..models.task import TaskStatus
from ..types.ingestion import OrderBy, ChunkMethod
from ..types.permission import Permission
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params

__all__ = [
    "DatasetAPI"
]


class DatasetAPI(BaseAPI):

    # =========================
    # Dataset
    # =========================

    async def create_dataset(
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
        require_params(name=name)

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

        payload = {
            "name": name,
            "avatar": avatar,
            "description": description,
            "permission": permission.value,
        }

        if chunk_method is not None:
            payload["chunk_method"] = chunk_method.value
            payload["parser_config"] = parser_config or {}

        if parse_type is not None:
            payload["parse_type"] = parse_type
            payload["pipeline_id"] = pipeline_id

        payload = self._normalize_request(payload)
        resp = await self._client.post("/datasets", json=payload)
        resp = self._handle_response(resp)

        data = resp["data"]

        return Dataset.from_raw(data)

    async def list_datasets(
            self,
            *,
            page: int = 1,
            page_size: int = 30,
            order_by: OrderBy = OrderBy.CREATE_TIME,
            desc: bool = True,
            dataset_id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> Tuple[List[Dataset], int]:
        params = {
            "page": page,
            "page_size": page_size,
            "orderby": order_by,
            "desc": desc,
            "id": dataset_id,
            "name": name,
        }
        params = self._normalize_request(params)
        resp = await self._client.get("/datasets", params=params)
        resp = self._handle_response(resp)

        raw_items: List[Dict[str, Any]] = resp.get("data", [])
        total = resp.get("total_datasets", 0)

        datasets = [Dataset.from_raw(item) for item in raw_items]
        return datasets, total

    @staticmethod
    def _default_parser_config(method: ChunkMethod | str) -> Dict:
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

        return {}

    async def update_dataset(
            self,
            dataset_id: str,
            *,
            name: Optional[str] = None,
            avatar: Optional[str] = None,
            description: Optional[str] = None,
            embedding_model: Optional[str] = None,
            permission: Optional[Permission | str] = None,
            pagerank: Optional[int] = None,
            chunk_method: Optional[ChunkMethod | str] = None,
            parser_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Update a dataset's configuration.

        Only provide the fields you want to update. For chunk_method changes,
        parser_config can be provided; otherwise defaults are used.
        """
        require_params(dataset_id=dataset_id)

        # normalize chunk_method
        if chunk_method is not None:
            if isinstance(chunk_method, str):
                try:
                    chunk_method = ChunkMethod(chunk_method)
                except ValueError:
                    raise RAGFlowValidationError(
                        f"Invalid chunk_method: {chunk_method!r}. "
                        f"Allowed: {[m.value for m in ChunkMethod]}"
                    )

        # parser_config default for chunk_method
        if chunk_method is not None and parser_config is None:
            parser_config = self._default_parser_config(chunk_method)

        # normalize permission
        if isinstance(permission, str):
            try:
                permission = Permission(permission)
            except ValueError:
                raise RAGFlowValidationError(
                    f"Invalid permission: {permission!r}. "
                    f"Allowed: {[p.value for p in Permission]}"
                )

        payload: dict[str, Any] = {
            "name": name,
            "avatar": avatar,
            "description": description,
            "embedding_model": embedding_model,
            "permission": permission.value if permission else None,
            "pagerank": pagerank,
        }

        if chunk_method is not None:
            payload["chunk_method"] = chunk_method.value
            payload["parser_config"] = parser_config or {}

        payload = self._normalize_request(payload)

        if not payload:
            raise RAGFlowValidationError("No fields provided to update.")

        url = f"/datasets/{dataset_id}"
        resp = await self._client.put(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def delete_datasets(
            self,
            ids: Optional[str | List[str]] = None,
    ) -> None:
        """
        Delete datasets by ID.

        Args:
            ids: List of dataset IDs to delete.
                 - None: delete all datasets
                 - []: delete nothing
                 - [id1, id2]: delete specified datasets

        Raises:
            RAGFlowAPIError: if deletion fails
        """
        payload: dict[str, Any] = {"ids": normalize_ids(ids)}
        payload = self._normalize_request(payload)

        if "ids" not in payload:
            # If null provided, all datasets will be deleted.
            payload["ids"] = None

        resp = await self._client.delete("/datasets", json=payload)
        self._handle_response(resp, require_data=False)

    # =========================
    # Knowledge Graph
    # =========================

    async def get_knowledge_graph(self, dataset_id: str) -> KnowledgeGraph:
        """
        Retrieve the knowledge graph of a dataset.

        Args:
            dataset_id: Target dataset ID.

        Returns:
            KnowledgeGraph instance containing nodes, edges, metadata, mind_map.
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/knowledge_graph"
        resp = await self._client.get(url)
        resp = self._handle_response(resp)

        data = resp.get("data") or {}
        return KnowledgeGraph.from_raw(data)

    async def construct_knowledge_graph(self, dataset_id: str) -> str:
        """
        Run GraphRAG (knowledge graph) construction for a dataset.

        Returns:
            graphrag_task_id
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/run_graphrag"
        resp = await self._client.post(url)
        resp = self._handle_response(resp)

        data = resp.get("data") or {}
        task_id = data.get("graphrag_task_id")

        if not task_id:
            raise RAGFlowAPIError(
                message="Missing graphrag_task_id in response",
                details=resp,
                status_code=500,
            )
        return task_id

    async def get_graphrag_status(self, dataset_id: str) -> TaskStatus:
        """
        Get the knowledge graph construction status.

        Returns:
            TaskStatus instance containing progress, messages, timestamps, etc.
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/trace_graphrag"
        resp = await self._client.get(url)
        resp = self._handle_response(resp)

        return TaskStatus.from_raw(resp.get("data") or {})

    async def delete_knowledge_graph(self, dataset_id: str) -> None:
        """
        Delete the knowledge graph of a dataset.

        Args:
            dataset_id: Target dataset ID.

        Returns:
            True if deletion succeeded.
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/knowledge_graph"
        resp = await self._client.delete(url)
        resp = self._handle_response(resp)

        result = resp.get("data")
        if not isinstance(result, bool):
            raise RAGFlowAPIError(
                message="Unexpected response type for delete knowledge graph",
                details=resp,
                status_code=500,
            )

    async def construct_raptor(self, dataset_id: str) -> str:
        """
        Run RAPTOR construction for a dataset.

        Returns:
            raptor_task_id
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/run_raptor"
        resp = await self._client.post(url)
        resp = self._handle_response(resp)

        data = resp.get("data") or {}
        task_id = data.get("raptor_task_id")

        if not task_id:
            raise RAGFlowAPIError(
                message="Missing raptor_task_id in response",
                details=resp,
                status_code=500,
            )
        return task_id

    async def get_raptor_status(self, dataset_id: str) -> TaskStatus:
        """
        Get the RAPTOR construction status.

        Returns:
            TaskStatus instance containing progress, messages, timestamps, etc.
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/trace_raptor"
        resp = await self._client.get(url)
        resp = self._handle_response(resp)

        return TaskStatus.from_raw(resp.get("data") or {})
