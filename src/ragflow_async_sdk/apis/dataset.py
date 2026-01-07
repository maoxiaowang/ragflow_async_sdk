from typing import Optional, Any

from .base import BaseAPI
from ..exceptions import RAGFlowValidationError, RAGFlowAPIError
from ..models.dataset import Dataset, KnowledgeGraph
from ..models.task import TaskStatus
from ..types import OrderBy, ChunkMethod, Permission
from ..utils.entity_helpers import get_single_or_raise
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params, validate_enum, resolve_unique_field


class DatasetAPI(BaseAPI):
    """API for managing datasets."""

    async def create_dataset(
        self,
        name: str,
        *,
        chunk_method: ChunkMethod | str | None = ChunkMethod.NAIVE,
        parser_config: dict | None = None,
        parse_type: str | None = None,
        pipeline_id: str | None = None,
        description: str | None = None,
        avatar: str | None = None,
        permission: Permission | str = Permission.ME,
    ) -> Dataset:
        """
        Create a new dataset.

        Args:
            name: Dataset name.
            chunk_method: Chunking method, mutually exclusive with parse_type/pipeline_id.
            parser_config: Parser configuration for the dataset.
            parse_type: Parsing type (used with pipeline_id).
            pipeline_id: Pipeline ID (used with parse_type).
            description: Optional description.
            avatar: Optional avatar URL.
            permission: Access permission for the dataset.

        Returns:
            Dataset instance of the created dataset.

        Raises:
            RAGFlowValidationError: If parameters are invalid.
            RAGFlowAPIError: If creation fails.
        """
        require_params(name=name)

        chunk_method = validate_enum(chunk_method, ChunkMethod, "chunk_method")
        permission = validate_enum(permission, Permission, "permission")

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
            "permission": permission,
        }

        if chunk_method is not None:
            payload["chunk_method"] = chunk_method
            payload["parser_config"] = parser_config or {}

        if parse_type is not None:
            payload["parse_type"] = parse_type
            payload["pipeline_id"] = pipeline_id

        payload = self._normalize_request(payload)
        resp = await self._client.post("/datasets", json=payload)
        resp = self._handle_response(resp)

        data = resp["data"]

        return Dataset.from_raw(data)

    @staticmethod
    def _default_parser_config(method: ChunkMethod) -> dict:
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

    async def list_datasets(
        self,
        *,
        page: int = 1,
        page_size: int = 30,
        order_by: OrderBy | str = OrderBy.CREATE_TIME,
        desc: bool = True,
        dataset_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> tuple[list[Dataset], int]:
        """
        List datasets with optional filters.

        Args:
            page: Page number.
            page_size: Items per page.
            order_by: Field to order by.
            desc: Descending order if True.
            dataset_id: Optional dataset ID filter.
            name: Optional dataset name filter.

        Returns:
            Tuple of list of Dataset instances and total count.

        Raises:
            RAGFlowAPIError: If listing fails.
        """
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

        raw_items: list[dict[str, Any]] = resp.get("data", [])
        total = resp.get("total_datasets", 0)

        datasets = [Dataset.from_raw(item) for item in raw_items]
        return datasets, total

    async def get_dataset(
            self,
            *,
            dataset_id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> Dataset:
        """
        Get a single dataset by ID or name.

        Exactly one of dataset_id or name must be provided.

        Args:
            dataset_id: Dataset ID.
            name: Dataset name.

        Returns:
            Dataset instance if found, otherwise None.

        Raises:
            RAGFlowValidationError: If both or neither parameters are provided.
            RAGFlowConflictError: If multiple datasets match the query.
        """
        param_name, param_value = resolve_unique_field(dataset_id=dataset_id, name=name)

        datasets, _ = await self.list_datasets(
            page=1,
            page_size=2,
            dataset_id=dataset_id,
            name=name,
        )

        return get_single_or_raise(
            items=datasets,
            key_name=param_name,
            key_value=param_value,
            entity_name="Dataset",
        )

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
            parser_config: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Update dataset fields.

        Only provide fields to be updated.

        Args:
            dataset_id: Target dataset ID.
            name: Optional new name.
            avatar: Optional avatar URL.
            description: Optional description.
            embedding_model: Optional embedding model.
            permission: Optional access permission.
            pagerank: Optional pagerank value.
            chunk_method: Optional chunk method.
            parser_config: Optional parser configuration.

        Raises:
            RAGFlowValidationError: If dataset_id is missing or parameters invalid.
            RAGFlowAPIError: If update fails.
        """
        require_params(dataset_id=dataset_id)

        chunk_method = validate_enum(chunk_method, ChunkMethod, "chunk_method")
        permission = validate_enum(permission, Permission, "permission")

        # parser_config default for chunk_method
        if chunk_method is not None and parser_config is None:
            parser_config = self._default_parser_config(chunk_method)

        payload: dict[str, Any] = {
            "name": name,
            "avatar": avatar,
            "description": description,
            "embedding_model": embedding_model,
            "permission": permission,
            "pagerank": pagerank,
        }

        if chunk_method is not None:
            payload["chunk_method"] = chunk_method
            payload["parser_config"] = parser_config or {}

        payload = self._normalize_request(payload)

        if not payload:
            raise RAGFlowValidationError("No fields provided to update.")

        url = f"/datasets/{dataset_id}"
        resp = await self._client.put(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def delete_datasets(
            self,
            ids: Optional[str | list[str]] = None,
    ) -> None:
        """
        Delete datasets by ID.

        Args:
            ids: Dataset IDs to delete.
                 - None: delete all datasets
                 - []: delete none
                 - [id1, id2]: delete specific datasets

        Raises:
            RAGFlowAPIError: If deletion fails.
        """
        payload = {"ids": normalize_ids(ids)}
        payload = self._normalize_request(payload)

        if "ids" not in payload:
            # If null provided, all datasets will be deleted.
            payload["ids"] = None

        resp = await self._client.delete("/datasets", json=payload)
        self._handle_response(resp, require_data=False)

    async def get_knowledge_graph(self, dataset_id: str) -> KnowledgeGraph:
        """
        Retrieve the knowledge graph of a dataset.

        Args:
            dataset_id: Target dataset ID.

        Returns:
            KnowledgeGraph instance containing nodes, edges, metadata, and mind map.

        Raises:
            RAGFlowValidationError: If dataset_id is not provided.
            RAGFlowAPIError: If retrieval fails.
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/knowledge_graph"
        resp = await self._client.get(url)
        resp = self._handle_response(resp)

        data = resp.get("data") or {}
        return KnowledgeGraph.from_raw(data)

    async def construct_knowledge_graph(self, dataset_id: str) -> str:
        """
        Run GraphRAG construction for a dataset.

        Args:
            dataset_id: Target dataset ID.

        Returns:
            Graphrag task ID.

        Raises:
            RAGFlowValidationError: If dataset_id is missing.
            RAGFlowAPIError: If task creation fails or response is invalid.
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
        Get the status of knowledge graph construction.

        Args:
            dataset_id: Target dataset ID.

        Returns:
            TaskStatus instance with progress, messages, and timestamps.

        Raises:
            RAGFlowValidationError: If dataset_id is missing.
            RAGFlowAPIError: If status retrieval fails.
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

        Raises:
            RAGFlowValidationError: If dataset_id is missing.
            RAGFlowAPIError: If deletion fails or response is invalid.
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

        Args:
            dataset_id: Target dataset ID.

        Returns:
            Raptor task ID.

        Raises:
            RAGFlowValidationError: If dataset_id is missing.
            RAGFlowAPIError: If task creation fails or response is invalid.
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
        Get the status of RAPTOR construction.

        Args:
            dataset_id: Target dataset ID.

        Returns:
            TaskStatus instance with progress, messages, and timestamps.

        Raises:
            RAGFlowValidationError: If dataset_id is missing.
            RAGFlowAPIError: If status retrieval fails.
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/trace_raptor"
        resp = await self._client.get(url)
        resp = self._handle_response(resp)

        return TaskStatus.from_raw(resp.get("data") or {})
