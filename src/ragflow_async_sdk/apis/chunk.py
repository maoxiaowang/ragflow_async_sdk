from typing import Any, Optional, Union

from .base import BaseAPI
from ..exceptions import RAGFlowValidationError
from ..models.chunk import Chunk
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params


class ChunkAPI(BaseAPI):
    """API for managing document chunks within datasets."""

    async def add_chunk(
        self,
        dataset_id: str,
        document_id: str,
        content: str,
        important_keywords: Optional[list[str]] = None,
        questions: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """
        Add a new chunk to a specific document.

        Args:
            dataset_id: Dataset containing the document.
            document_id: Target document ID.
            content: Text content of the chunk.
            important_keywords: Optional list of keywords for chunk importance.
            questions: Optional list of questions associated with the chunk.

        Returns:
            dict: Added chunk data.
        """
        require_params(dataset_id=dataset_id, document_id=document_id, content=content)

        payload = {
            "content": content,
            "important_keywords": important_keywords,
            "questions": questions,
        }
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/documents/{document_id}/chunks"
        resp = await self._client.post(url, json=payload)
        resp = self._handle_response(resp)
        return resp.get("data", {})

    async def list_chunks(
        self,
        dataset_id: str,
        document_id: str,
        *,
        keywords: Optional[str] = None,
        page: int = 1,
        page_size: int = 1024,
        chunk_id: Optional[str] = None,
    ) -> tuple[list[Chunk], int]:
        """
        List chunks in a document with optional filters.

        Args:
            dataset_id: Dataset containing the document.
            document_id: Target document ID.
            keywords: Optional search keywords.
            page: Page number.
            page_size: Number of chunks per page.
            chunk_id: Optional filter by specific chunk ID.

        Returns:
            Tuple of (list of Chunk objects, total count).
        """
        require_params(dataset_id=dataset_id, document_id=document_id)

        params = {
            "keywords": keywords,
            "page": page,
            "page_size": page_size,
            "id": chunk_id,
        }
        params = self._normalize_request(params)

        url = f"/datasets/{dataset_id}/documents/{document_id}/chunks"
        resp = await self._client.get(url, params=params)
        resp = self._handle_response(resp)

        data = resp.get("data", {})
        raw_chunks = data.get("chunks", [])
        total = data.get("total", 0)

        chunks = [Chunk.from_raw(item) for item in raw_chunks]
        return chunks, total

    async def update_chunk(
        self,
        dataset_id: str,
        document_id: str,
        chunk_id: str,
        *,
        content: Optional[str] = None,
        important_keywords: Optional[list[str]] = None,
        available: Optional[bool] = None,
    ) -> None:
        """
        Update content or settings for a specific chunk.

        Args:
            dataset_id: Dataset containing the document.
            document_id: Document ID.
            chunk_id: Chunk ID to update.
            content: New content for the chunk.
            important_keywords: Updated list of important keywords.
            available: Whether the chunk is available (True/False).

        Raises:
            RAGFlowValidationError: If no fields are provided to update.
        """
        require_params(dataset_id=dataset_id, document_id=document_id, chunk_id=chunk_id)

        payload = {
            "content": content,
            "important_keywords": important_keywords,
            "available": available,
        }
        payload = self._normalize_request(payload)

        if not payload:
            raise RAGFlowValidationError("At least one field must be provided to update a chunk.")

        url = f"/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}"
        resp = await self._client.put(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def delete_chunks(
        self,
        dataset_id: str,
        document_id: str,
        *,
        chunk_ids: Optional[str | list[str]] = None,
    ) -> None:
        """
        Delete chunks by ID.

        Args:
            dataset_id: Dataset containing the document.
            document_id: Document ID.
            chunk_ids: List of chunk IDs to delete. If None, deletes all chunks.

        """
        require_params(dataset_id=dataset_id, document_id=document_id)

        chunk_ids = normalize_ids(chunk_ids, "chunk_ids")
        payload = {"chunk_ids": chunk_ids}
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/documents/{document_id}/chunks"
        resp = await self._client.delete(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def get_metadata_summary(self, dataset_id: str) -> dict[str, Any]:
        """
        Retrieve a metadata summary for all documents in a dataset.

        Args:
            dataset_id: Dataset ID.

        Returns:
            dict: Metadata summary.
        """
        require_params(dataset_id=dataset_id)

        url = f"/datasets/{dataset_id}/metadata/summary"
        resp = await self._client.get(url)
        resp = self._handle_response(resp)
        return resp.get("data", {}).get("summary", {})

    async def update_metadata(
        self,
        dataset_id: str,
        *,
        selector: Optional[dict] = None,
        updates: Optional[list[dict]] = None,
        deletes: Optional[list[dict]] = None,
    ) -> dict[str, int]:
        """
        Batch update or delete document-level metadata.

        Args:
            dataset_id: Dataset ID.
            selector: Optional filter, e.g., {"document_ids": [...], "metadata_condition": {...}}.
            updates: List of metadata updates, each {"key": str, "match": str, "value": str}.
            deletes: List of metadata deletions, each {"key": str, "value": Optional[str]}.

        Returns:
            dict: {"updated": int, "matched_docs": int}

        Raises:
            RAGFlowValidationError: If no updates or deletes are provided.
        """
        require_params(dataset_id=dataset_id)

        payload = {"selector": selector, "updates": updates, "deletes": deletes}
        payload = self._normalize_request(payload)

        if not payload:
            raise RAGFlowValidationError("No updates or deletes provided.")

        url = f"/datasets/{dataset_id}/metadata/update"
        resp = await self._client.post(url, json=payload)
        resp = self._handle_response(resp)
        return resp.get("data", {})

    async def retrieve_chunks(
        self,
        question: str,
        *,
        dataset_ids: Optional[Union[str, list[str]]] = None,
        document_ids: Optional[Union[str, list[str]]] = None,
        page: int = 1,
        page_size: int = 30,
        similarity_threshold: float = 0.2,
        vector_similarity_weight: float = 0.3,
        top_k: int = 1024,
        rerank_id: Optional[str] = None,
        keyword: bool = False,
        highlight: bool = False,
        cross_languages: Optional[list[str]] = None,
        metadata_condition: Optional[dict] = None,
        use_kg: bool = False,
        toc_enhance: bool = False,
    ) -> dict[str, Any]:
        """
        Retrieve chunks from datasets or documents based on query.

        Args:
            question: Query string or keywords (required).
            dataset_ids: Dataset IDs to search.
            document_ids: Document IDs to search.
            page: Page number.
            page_size: Chunks per page.
            similarity_threshold: Minimum similarity score.
            vector_similarity_weight: Weight of vector similarity.
            top_k: Number of chunks considered for vector computation.
            rerank_id: Optional rerank model ID.
            keyword: Enable keyword-based matching.
            highlight: Highlight matched terms.
            cross_languages: Target languages for translation.
            metadata_condition: Metadata filter conditions.
            use_kg: Enable knowledge graph multi-hop search.
            toc_enhance: Enable table-of-contents enhanced search.

        Returns:
            dict: Retrieved chunks, document aggregations, and total count.

        Raises:
            RAGFlowValidationError: If question is empty or dataset/document IDs are missing.
        """
        require_params(question=question)

        dataset_ids = normalize_ids(dataset_ids, "dataset_ids")
        document_ids = normalize_ids(document_ids, "document_ids")

        if not dataset_ids and not document_ids:
            raise RAGFlowValidationError("Either 'dataset_ids' or 'document_ids' must be provided.")

        payload = {
            "question": question,
            "dataset_ids": dataset_ids,
            "document_ids": document_ids,
            "page": page,
            "page_size": page_size,
            "similarity_threshold": similarity_threshold,
            "vector_similarity_weight": vector_similarity_weight,
            "top_k": top_k,
            "rerank_id": rerank_id,
            "keyword": keyword,
            "highlight": highlight,
            "cross_languages": cross_languages,
            "metadata_condition": metadata_condition,
            "use_kg": use_kg,
            "toc_enhance": toc_enhance,
        }
        payload = self._normalize_request(payload)

        url = "/retrieval"
        resp = await self._client.post(url, json=payload)
        resp = self._handle_response(resp)
        return resp.get("data", {})
