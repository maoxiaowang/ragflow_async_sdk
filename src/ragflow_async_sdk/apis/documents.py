from json import JSONDecodeError
from typing import List, Optional, Dict, Any, Tuple

from .base import BaseAPI
from ..exceptions import RAGFlowValidationError, RAGFlowAPIError
from ..models.document import Document
from ..types.ingestion import ChunkMethod
from ..utils.validators import require_params
from ..utils.normalizers import normalize_ids

__all__ = ["DocumentsAPI"]


class DocumentsAPI(BaseAPI):

    async def upload_documents(
            self,
            dataset_id: str,
            files: List[Tuple[str, bytes, str]],
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Upload multiple documents to a dataset using file bytes.

        Args:
            dataset_id: Target dataset ID.
            files: List of files to upload. Each file is a tuple:
                (filename: str, content: bytes, content_type: str)

        Returns:
            Tuple of (uploaded_docs, count)
        """
        require_params(dataset_id=dataset_id)

        if not files:
            raise RAGFlowValidationError("No files provided for upload")

        files_to_send = [("file", f) for f in files]

        resp = await self._client.post(
            f"/datasets/{dataset_id}/documents",
            files=files_to_send,
        )

        docs = resp.get("data", [])
        return docs, len(docs)

    async def update_document(
            self,
            dataset_id: str,
            document_id: str,
            *,
            name: Optional[str] = None,
            meta_fields: Optional[Dict[str, Any]] = None,
            chunk_method: Optional[str | ChunkMethod] = None,
            parser_config: Optional[Dict[str, Any]] = None,
            enabled: Optional[int] = None,
    ) -> Document:
        """
        Update document metadata or parser configuration.
        """
        require_params(dataset_id=dataset_id, document_id=document_id)

        if isinstance(chunk_method, str):
            try:
                chunk_method = ChunkMethod(chunk_method)
            except ValueError:
                raise RAGFlowValidationError(
                    f"Invalid chunk_method: {chunk_method}. "
                    f"Allowed: {[m.value for m in ChunkMethod]}"
                )

        payload: dict[str, Any] = {
            "name": name,
            "meta_fields": meta_fields,
            "chunk_method": chunk_method.value if chunk_method else None,
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
        Download a document from a dataset as bytes.

        Args:
            dataset_id: Target dataset ID.
            document_id: Document ID to download.

        Returns:
            bytes: Document content.
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
            order_by: str = "create_time",
            desc: bool = True,
            keywords: Optional[str] = None,
            document_id: Optional[str] = None,
            name: Optional[str] = None,
            create_time_from: int = 0,
            create_time_to: int = 0,
            suffix: Optional[List[str]] = None,
            run: Optional[List[str]] = None,
            metadata_condition: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Document], int]:
        """
        List documents in a dataset with filtering.
        """
        if not dataset_id:
            raise RAGFlowValidationError("dataset_id is required")

        params: Dict[str, Any] = {
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

        raw_docs: List[Dict[str, Any]] = resp.get("data", {}).get("docs", [])
        total = resp.get("data", {}).get("total", 0)

        documents = [Document.from_raw(d) for d in raw_docs]
        return documents, total

    async def delete_documents(
            self,
            dataset_id: str,
            ids: Optional[List[str] | str] = None,
    ) -> None:
        """
        Delete documents by IDs in a dataset. If ids=None, delete all.
        """
        if not dataset_id:
            raise RAGFlowValidationError("dataset_id is required")

        payload: Dict[str, Any] = {"ids": normalize_ids(ids)}
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/documents"
        resp = await self._client.delete(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def parse_documents(
            self,
            dataset_id: str,
            document_ids: List[str],
    ) -> None:
        """
        Parse specified documents in a dataset.

        Args:
            dataset_id: Target dataset ID.
            document_ids: List of document IDs to parse.

        Raises:
            RAGFlowValidationError: If dataset_id or document_ids is invalid.
        """
        require_params(dataset_id=dataset_id)
        document_ids = normalize_ids(document_ids)

        if not document_ids:
            raise RAGFlowValidationError("document_ids must be a non-empty list of strings")

        payload: Dict[str, Any] = {
            "document_ids": document_ids
        }
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/chunks"
        resp = await self._client.post(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def stop_parsing_documents(
            self,
            dataset_id: str,
            document_ids: List[str],
    ) -> None:
        """
        Stop parsing specified documents in a dataset.

        Args:
            dataset_id: Target dataset ID.
            document_ids: List of document IDs to stop parsing.

        Raises:
            RAGFlowValidationError: If dataset_id or document_ids is invalid.
        """
        require_params(dataset_id=dataset_id)
        document_ids = normalize_ids(document_ids)

        if not document_ids:
            raise RAGFlowValidationError("document_ids must be a non-empty list of strings")

        payload: Dict[str, Any] = {
            "document_ids": document_ids,
        }
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/chunks"
        resp = await self._client.delete(url, json=payload)
        self._handle_response(resp, require_data=False)