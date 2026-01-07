from json import JSONDecodeError
from typing import Optional, Any

from .base import BaseAPI
from ..exceptions import RAGFlowValidationError, RAGFlowAPIError
from ..models.document import Document
from ..types import OrderBy, ChunkMethod
from ..utils.entity_helpers import get_single_or_raise
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params, validate_enum, resolve_unique_field


class DocumentAPI(BaseAPI):
    """API for managing documents."""

    async def upload_documents(
        self,
        dataset_id: str,
        files: list[tuple[str, bytes, str]],
    ) -> list[Document]:
        """
        Upload multiple documents to a dataset.

        Args:
            dataset_id: Target dataset ID.
            files: List of files to upload, each as (filename, content_bytes, content_type).

        Returns:
            Tuple containing the list of uploaded documents and the number of documents.
        """
        require_params(dataset_id=dataset_id)

        if not files:
            raise RAGFlowValidationError("No files provided for upload")

        files_to_send = [("file", f) for f in files]
        resp = await self._client.post(
            f"/datasets/{dataset_id}/documents",
            files=files_to_send,
        )

        return [Document.from_raw(item) for item in self._handle_response(resp)["data"]]

    async def update_document(
        self,
        dataset_id: str,
        document_id: str,
        *,
        name: Optional[str] = None,
        meta_fields: Optional[dict[str, Any]] = None,
        chunk_method: Optional[str | ChunkMethod] = None,
        parser_config: Optional[dict[str, Any]] = None,
        enabled: Optional[int] = None,
    ) -> Document:
        """
        Update a document's metadata or parsing configuration.

        Only provide the fields you want to update.

        Args:
            dataset_id: Dataset containing the document.
            document_id: Document ID to update.
            name: New name of the document.
            meta_fields: Metadata fields to update.
            chunk_method: Parsing chunk method (str or ChunkMethod).
            parser_config: Parser configuration if chunk_method is changed.
            enabled: 1 to enable, 0 to disable document.

        Returns:
            Updated Document instance.
        """
        require_params(dataset_id=dataset_id, document_id=document_id)
        chunk_method = validate_enum(chunk_method, ChunkMethod, "chunk_method")

        payload = {
            "name": name,
            "meta_fields": meta_fields,
            "chunk_method": chunk_method,
            "parser_config": parser_config,
            "enabled": enabled,
        }
        payload = self._normalize_request(payload)

        if not payload:
            raise RAGFlowValidationError("No fields provided to update.")

        url = f"/datasets/{dataset_id}/documents/{document_id}"
        resp = await self._client.put(url, json=payload)
        resp = self._handle_response(resp)

        return Document.from_raw(resp.get("data") or {})

    async def download_document(self, dataset_id: str, document_id: str) -> bytes:
        """
        Download a document as bytes.

        Args:
            dataset_id: Dataset containing the document.
            document_id: Document ID to download.

        Returns:
            Document content as bytes.

        Raises:
            RAGFlowAPIError: If download fails.
        """
        require_params(dataset_id=dataset_id, document_id=document_id)

        url = f"/datasets/{dataset_id}/documents/{document_id}"
        resp = await self._client.get(url, expect_json=False)

        if resp.status_code != 200:
            try:
                data = resp.json()
            except (JSONDecodeError, TypeError):
                data = resp.text
            raise RAGFlowAPIError(
                message=f"Failed to download document {document_id}",
                details={"status": resp.status_code, "response": data},
                status_code=resp.status_code,
            )
        return resp.content

    async def list_documents(
        self,
        dataset_id: str,
        *,
        page: int = 1,
        page_size: int = 30,
        order_by: OrderBy | str = OrderBy.CREATE_TIME,
        desc: bool = True,
        keywords: Optional[str] = None,
        document_id: Optional[str] = None,
        name: Optional[str] = None,
        create_time_from: int = 0,
        create_time_to: int = 0,
        suffix: Optional[list[str]] = None,
        run: Optional[list[str]] = None,
        metadata_condition: Optional[dict[str, Any]] = None,
    ) -> tuple[list[Document], int]:
        """
        List documents in a dataset with optional filtering.

        Args:
            dataset_id: Dataset ID.
            page: Page number.
            page_size: Items per page.
            order_by: Field to sort by.
            desc: Whether to sort descending.
            keywords: Search keywords.
            document_id: Filter by specific document ID.
            name: Filter by document name.
            create_time_from: Filter documents created after this timestamp.
            create_time_to: Filter documents created before this timestamp.
            suffix: Filter by file suffixes.
            run: Filter by ingestion run IDs.
            metadata_condition: Filter by metadata conditions.

        Returns:
            Tuple of (list of Document objects, total count).
        """
        if not dataset_id:
            raise RAGFlowValidationError("dataset_id is required")

        params = {
            "page": page,
            "page_size": page_size,
            "orderby": order_by,
            "desc": desc,
            "keywords": keywords,
            "id": document_id,
            "name": name,
            "create_time_from": create_time_from,
            "create_time_to": create_time_to,
            "suffix": suffix,
            "run": run,
            "metadata_condition": metadata_condition,
        }
        params = self._normalize_request(params)
        url = f"/datasets/{dataset_id}/documents"
        resp = await self._client.get(url, params=params)
        resp = self._handle_response(resp)

        raw_docs = resp.get("data", {}).get("docs", [])
        total = resp.get("data", {}).get("total", 0)

        documents = [Document.from_raw(d) for d in raw_docs]
        return documents, total

    async def get_document(
            self,
            dataset_id: str,
            *,
            document_id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> Document:
        """
        Get a single document by ID or name within a dataset.

        Exactly one of document_id or name must be provided.

        Args:
            dataset_id: Dataset ID.
            document_id: Document ID.
            name: Document name.

        Returns:
            Document instance if found, otherwise None.

        Raises:
            RAGFlowValidationError: If parameters are invalid.
            RAGFlowConflictError: If multiple documents match.
        """
        require_params(dataset_id=dataset_id)

        param_name, param_value = resolve_unique_field(document_id=document_id, name=name)

        documents, _ = await self.list_documents(
            dataset_id=dataset_id,
            page=1,
            page_size=2,
            document_id=document_id,
            name=name,
        )

        return get_single_or_raise(
            items=documents,
            key_name=param_name,
            key_value=param_value,
            entity_name="Document",
        )

    async def delete_documents(self, dataset_id: str, ids: Optional[list[str] | str] = None) -> None:
        """
        Delete documents by ID in a dataset.

        Args:
            dataset_id: Dataset ID.
            ids: List of document IDs to delete. If None, deletes all documents.
        """
        if not dataset_id:
            raise RAGFlowValidationError("dataset_id is required")

        payload = {"ids": normalize_ids(ids)}
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/documents"
        resp = await self._client.delete(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def parse_documents(self, dataset_id: str, document_ids: list[str]) -> None:
        """
        Start parsing specified documents in a dataset.

        Args:
            dataset_id: Dataset ID.
            document_ids: List of document IDs to parse.

        Raises:
            RAGFlowValidationError: If dataset_id or document_ids are invalid.
        """
        require_params(dataset_id=dataset_id)
        document_ids = normalize_ids(document_ids)

        if not document_ids:
            raise RAGFlowValidationError("document_ids must be a non-empty list")

        payload = {"document_ids": document_ids}
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/chunks"
        resp = await self._client.post(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def stop_parsing_documents(self, dataset_id: str, document_ids: list[str]) -> None:
        """
        Stop parsing specified documents in a dataset.

        Args:
            dataset_id: Dataset ID.
            document_ids: List of document IDs to stop parsing.

        Raises:
            RAGFlowValidationError: If dataset_id or document_ids are invalid.
        """
        require_params(dataset_id=dataset_id)
        document_ids = normalize_ids(document_ids)

        if not document_ids:
            raise RAGFlowValidationError("document_ids must be a non-empty list")

        payload = {"document_ids": document_ids}
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/chunks"
        resp = await self._client.delete(url, json=payload)
        self._handle_response(resp, require_data=False)