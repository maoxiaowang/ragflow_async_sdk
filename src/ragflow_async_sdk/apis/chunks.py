from typing import Any, Dict, List, Optional, Tuple, Union

from .base import BaseAPI
from ..exceptions import RAGFlowValidationError
from ..models.chunk import Chunk
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params

__all__ = ["ChunksAPI"]


class ChunksAPI(BaseAPI):
    """API for managing document chunks within datasets."""

    async def add_chunk(
        self,
        dataset_id: str,
        document_id: str,
        content: str,
        important_keywords: Optional[List[str]] = None,
        questions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Add a chunk to a specific document.
        """
        require_params(
            dataset_id=dataset_id,
            document_id=document_id,
            content=content,
        )

        payload: Dict[str, Any] = {
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
    ) -> Tuple[List[Chunk], int]:
        """
        List chunks in a document with optional filters.
        """
        require_params(dataset_id=dataset_id, document_id=document_id)

        params: Dict[str, Any] = {
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
        important_keywords: Optional[List[str]] = None,
        available: Optional[bool] = None,
    ) -> None:
        """
        Update content or settings for a specific chunk.
        """
        require_params(
            dataset_id=dataset_id,
            document_id=document_id,
            chunk_id=chunk_id,
        )

        payload: Dict[str, Any] = {
            "content": content,
            "important_keywords": important_keywords,
            "available": available,
        }
        payload = self._normalize_request(payload)

        if not payload:
            raise RAGFlowValidationError(
                "At least one field must be provided to update a chunk."
            )

        url = f"/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}"
        resp = await self._client.put(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def delete_chunks(
        self,
        dataset_id: str,
        document_id: str,
        *,
        chunk_ids: Optional[Union[str, List[str]]] = None,
    ) -> None:
        """
        Delete chunks by ID.

        If chunk_ids is None, all chunks in the document will be deleted.
        """
        require_params(dataset_id=dataset_id, document_id=document_id)

        chunk_ids = normalize_ids(chunk_ids, "chunk_ids")

        payload: Dict[str, Any] = {
            "chunk_ids": chunk_ids,
        }
        payload = self._normalize_request(payload)

        url = f"/datasets/{dataset_id}/documents/{document_id}/chunks"
        resp = await self._client.delete(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def get_metadata_summary(self, dataset_id: str) -> dict[str, Any]:
        """
        Retrieve a metadata summary for all documents in a dataset.

        Args:
            dataset_id: Target dataset ID.

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
            updates: Optional[List[dict]] = None,
            deletes: Optional[List[dict]] = None,
    ) -> dict[str, int]:
        """
        Batch update or delete document-level metadata within a dataset.

        Args:
            dataset_id: Target dataset ID.
            selector: Optional selector dict, e.g., {"document_ids": [...], "metadata_condition": {...}}
            updates: Optional list of metadata updates, each {"key": str, "match": str, "value": str}.
            deletes: Optional list of metadata deletions, each {"key": str, "value": Optional[str]}.

        Returns:
            dict: {"updated": int, "matched_docs": int}
        """
        require_params(dataset_id=dataset_id)

        payload: Dict[str, Any] = {
            "selector": selector,
            "updates": updates,
            "deletes": deletes,
        }
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
            dataset_ids: Optional[Union[str, List[str]]] = None,
            document_ids: Optional[Union[str, List[str]]] = None,
            page: int = 1,
            page_size: int = 30,
            similarity_threshold: float = 0.2,
            vector_similarity_weight: float = 0.3,
            top_k: int = 1024,
            rerank_id: Optional[str] = None,
            keyword: bool = False,
            highlight: bool = False,
            cross_languages: Optional[List[str]] = None,
            metadata_condition: Optional[dict] = None,
            use_kg: bool = False,
            toc_enhance: bool = False,
    ) -> dict[str, Any]:
        """
        Retrieve chunks from specified datasets or documents.

        Args:
            question: User query or keywords (required).
            dataset_ids: Dataset IDs to search.
            document_ids: Document IDs to search.
            page: Page number.
            page_size: Number of chunks per page.
            similarity_threshold: Minimum similarity score.
            vector_similarity_weight: Weight of vector similarity.
            top_k: Number of chunks for vector similarity computation.
            rerank_id: Rerank model ID.
            keyword: Enable keyword-based matching.
            highlight: Enable highlighting of matched terms.
            cross_languages: List of target languages for keyword translation.
            metadata_condition: Metadata filter conditions.
            use_kg: Enable knowledge graph multi-hop search.
            toc_enhance: Enable table of contents enhanced search.

        Returns:
            dict: Retrieved chunks, document aggregations, total count.
        """
        require_params(question=question)

        dataset_ids = normalize_ids(dataset_ids, "dataset_ids")
        document_ids = normalize_ids(document_ids, "document_ids")

        if not dataset_ids and not document_ids:
            raise RAGFlowValidationError("Either 'dataset_ids' or 'document_ids' must be provided.")

        payload: Dict[str, Any] = {
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
