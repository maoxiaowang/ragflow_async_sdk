from dataclasses import dataclass
from typing import Optional, Any, Self

from ..models.base import BaseEntity


@dataclass(slots=True)
class Folder(BaseEntity):
    id: str
    name: str
    type: str
    parent_id: Optional[str] = None


@dataclass(slots=True)
class File(BaseEntity):
    id: str
    name: str
    type: str
    size: Optional[int] = None
    parent_id: Optional[str] = None
    location: Optional[str] = None
    create_time: Optional[int] = None


@dataclass(slots=True)
class ListFilesResult(BaseEntity):
    files: Optional[list[File]]
    parent_folder: Optional[Folder] = None

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> Self:
        """
        Build ListFilesResult from RAGFlow list files response data.
        """
        files_raw = raw.get("files", [])
        files = [
            File.from_raw(item)
            for item in files_raw if isinstance(item, dict)
        ]

        parent_folder_raw = raw.get("parent_folder")
        parent_folder = (
            Folder.from_raw(parent_folder_raw)
            if isinstance(parent_folder_raw, dict) else None
        )

        obj = cls(files=files, parent_folder=parent_folder,)
        obj._raw = raw
        return obj