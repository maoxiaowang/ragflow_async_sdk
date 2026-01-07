# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from typing import Optional

from ..apis.base import BaseAPI
from ..exceptions import RAGFlowValidationError
from ..models.file import Folder, File, ListFilesResult, ConversionResult
from ..types import OrderBy
from ..types.file import FileType
from ..utils.validators import require_params, validate_file_tuples


class FileAPI(BaseAPI):
    """API for managing files and folders."""

    async def upload_files(
        self,
        files: list[tuple[str, bytes, str]],
        parent_id: str | None = None
    ) -> list[File]:
        """
        Upload multiple files to a folder.

        Args:
            files: List of tuples (filename, content_bytes, content_type).
            parent_id: Optional ID of the parent folder.

        Returns:
            List of uploaded File objects.

        Raises:
            RAGFlowValidationError: If files list is empty or invalid.
            RAGFlowAPIError: If upload fails.
        """
        if not files:
            raise RAGFlowValidationError("No files provided for upload")
        validate_file_tuples(files)
        files_to_send = [("file", f) for f in files]
        data = {"parent_id": parent_id} if parent_id else None

        resp = await self._client.post("/file/upload", data=data, files=files_to_send)
        return [File.from_raw(item) for item in self._handle_response(resp)["data"]]

    async def create_file_or_folder(
        self,
        name: str,
        type_: FileType | str,
        parent_id: str | None = None
    ) -> Folder | File:
        """
        Create a new folder or virtual file.

        Args:
            name: Name of the file or folder.
            type_: Type of the object ("FOLDER" or "FILE").
            parent_id: Optional parent folder ID.

        Returns:
            Folder instance if type is "FOLDER", else File instance.

        Raises:
            RAGFlowValidationError: If required parameters are missing.
            RAGFlowAPIError: If creation fails.
        """
        require_params(name=name, type_=type_)

        payload = {"name": name, "type": type_}
        if parent_id:
            payload["parent_id"] = parent_id
        payload = self._normalize_request(payload)

        resp = await self._client.post("/file/create", json=payload)
        data = self._handle_response(resp)["data"]
        return Folder.from_raw(data) if data.get("type") == "FOLDER" else File.from_raw(data)

    async def list_files(
        self,
        parent_id: Optional[str] = None,
        keywords: Optional[str] = None,
        page: int = 1,
        page_size: int = 15,
        orderby: OrderBy | str = OrderBy.CREATE_TIME,
        desc: bool = True
    ) -> tuple[ListFilesResult, int]:
        """
        List files in a folder with optional filtering and pagination.

        Args:
            parent_id: Optional ID of the parent folder to list files from.
            keywords: Optional search keywords for file names.
            page: Page number for pagination.
            page_size: Number of items per page.
            orderby: Field to order results by.
            desc: Whether to sort in descending order.

        Returns:
            Tuple of ListFilesResult instance and total file count.

        Raises:
            RAGFlowAPIError: If listing fails.
        """
        params = {
            "parent_id": parent_id,
            "keywords": keywords,
            "page": page,
            "page_size": page_size,
            "orderby": orderby,
            "desc": desc,
        }
        params = self._normalize_request(params)

        resp = await self._client.get("/file/list", params=params)
        resp = self._handle_response(resp)
        data = resp.get("data")

        result = ListFilesResult.from_raw({
            "files": data.get("files", []),
            "parent_folder": data.get("parent_folder"),
        })
        return result, data.get("total", 0)

    async def get_root_folder(self) -> Folder:
        """
        Get the root folder of the file system.

        Returns:
            Folder instance representing the root folder.

        Raises:
            RAGFlowAPIError: If request fails.
        """
        resp = await self._client.get("/file/root_folder")
        resp = self._handle_response(resp)
        data = resp.get("data", {})
        return Folder.from_raw(data.get("root_folder", {}))

    async def get_parent_folder(self, file_id: str) -> Folder:
        """
        Get the parent folder of a file.

        Args:
            file_id: ID of the file.

        Returns:
            Folder instance representing the parent folder.

        Raises:
            RAGFlowValidationError: If file_id is missing.
            RAGFlowAPIError: If request fails.
        """
        require_params(file_id=file_id)
        resp = await self._client.get("/file/parent_folder", params={"file_id": file_id})
        resp = self._handle_response(resp)
        data = resp.get("data", {})
        return Folder.from_raw(data.get("parent_folder", {}))

    async def get_all_parent_folders(self, file_id: str) -> list[Folder]:
        """
        Get all parent folders of a file up to the root.

        Args:
            file_id: ID of the file.

        Returns:
            List of Folder instances from immediate parent up to root.

        Raises:
            RAGFlowValidationError: If file_id is missing.
            RAGFlowAPIError: If request fails.
        """
        require_params(file_id=file_id)
        resp = await self._client.get("/file/all_parent_folder", params={"file_id": file_id})
        resp = self._handle_response(resp)
        data = resp.get("data", {})
        parent_folders = data.get("parent_folders", [])
        return [Folder.from_raw(f) for f in parent_folders]

    async def delete_files(self, file_ids: list[str]) -> bool:
        """
        Delete files by their IDs.

        Args:
            file_ids: List of file IDs to delete.

        Returns:
            True if deletion succeeded, False otherwise.

        Raises:
            RAGFlowValidationError: If file_ids is empty.
            RAGFlowAPIError: If deletion fails.
        """
        require_params(file_ids=file_ids)
        resp = await self._client.post("/file/rm", json={"file_ids": file_ids})
        resp = self._handle_response(resp)
        return bool(resp.get("data", False))

    async def rename_file(self, file_id: str, name: str) -> bool:
        """
        Rename a file.

        Args:
            file_id: ID of the file to rename.
            name: New name for the file.

        Returns:
            True if rename succeeded, False otherwise.

        Raises:
            RAGFlowValidationError: If file_id or name is missing.
            RAGFlowAPIError: If renaming fails.
        """
        require_params(file_id=file_id, name=name)
        resp = await self._client.post("/file/rename", json={"file_id": file_id, "name": name})
        resp = self._handle_response(resp)
        return bool(resp.get("data", False))

    async def move_files(self, src_file_ids: list[str], dest_file_id: str) -> bool:
        """
        Move files to a new folder.

        Args:
            src_file_ids: List of source file IDs to move.
            dest_file_id: Destination folder ID.

        Returns:
            True if move succeeded, False otherwise.

        Raises:
            RAGFlowValidationError: If parameters are missing.
            RAGFlowAPIError: If move operation fails.
        """
        require_params(src_file_ids=src_file_ids, dest_file_id=dest_file_id)
        resp = await self._client.post(
            "/file/mv",
            json={
                "src_file_ids": src_file_ids,
                "dest_file_id": dest_file_id
            }
        )
        resp = self._handle_response(resp)
        return bool(resp.get("data", False))

    async def convert_files(self, file_ids: list[str], kb_ids: list[str]) -> list[ConversionResult]:
        """
        Convert files into knowledge base entries.

        Args:
            file_ids: List of file IDs to convert.
            kb_ids: List of target knowledge base IDs.

        Returns:
            List of conversion results (dicts).

        Raises:
            RAGFlowValidationError: If parameters are missing.
            RAGFlowAPIError: If conversion fails.
        """
        require_params(file_ids=file_ids, kb_ids=kb_ids)
        resp = await self._client.post(
            "/file/convert",
            json={
                "file_ids": file_ids,
                "kb_ids": kb_ids
            }
        )
        data = self._handle_response(resp)["data"]
        return [ConversionResult(**item) for item in data]

    async def download_file(self, file_id: str) -> bytes:
        """
        Download the content of a file.

        Args:
            file_id: ID of the file to download.

        Returns:
            File content as bytes.

        Raises:
            RAGFlowValidationError: If file_id is missing.
            RAGFlowAPIError: If download fails.
        """
        require_params(file_id=file_id)
        resp = await self._client.get(f"/file/get/{file_id}", expect_json=False)
        if resp.status_code != 200:
            self._handle_response(resp)
        return resp.content
