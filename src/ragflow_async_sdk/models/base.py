from __future__ import annotations

import json
from dataclasses import fields, MISSING
from enum import Enum
from typing import Any, TypeVar, Type, Optional

T = TypeVar("T", bound="BaseEntity")


class BaseEntity:
    """
    Base class for all entities.

    Attributes:
        __export_fields__: Tuple of field names to export in `to_dict`.
        _raw: Original raw dictionary from API.
    """
    __export_fields__: tuple[str, ...] = ()
    _raw: dict[str, Any] = None

    def __init__(self, **kwargs):
        for field in self.__export_fields__:
            setattr(self, field, kwargs.get(field))
        self._raw = kwargs.get("_raw", {})

    @classmethod
    def from_raw(cls: Type[T], raw: dict[str, Any]) -> T:
        """
        Create an instance from raw dictionary, populating export fields.

        Args:
            raw: Original dictionary data from API.

        Returns:
            Instance of cls with fields set and _raw saved.
        """
        init_kwargs = {}
        for f in fields(cls):
            if f.name in ("_raw", "__export_fields__"):
                continue
            if f.name in raw:
                init_kwargs[f.name] = raw[f.name]
            else:
                init_kwargs[f.name] = f.default if f.default is not MISSING else None

        obj = cls(**init_kwargs)
        obj._raw = raw
        return obj

    def to_dict(self, full: bool = False, export_fields: Optional[list[str]] = None) -> dict[str, Any]:
        """
        Serialize entity to a dictionary.

        Args:
            full: If True, serialize all raw fields; otherwise only export fields.
            export_fields: Optional list of field names to export. Overrides `__export_fields__` if provided.
                       If None and full=False, defaults to `__export_fields__` or all dataclass fields.

        Returns:
            dict: Serialized representation.
        """
        result = {}
        if full:
            for k, v in self._raw.items():
                result[k] = self._serialize_value(v)
        else:
            fields_to_export = export_fields or getattr(self, "__export_fields__", None)
            for field_name in fields_to_export:
                value = getattr(self, field_name, None)
                result[field_name] = self._serialize_value(value)
        return result

    def to_json(
            self,
            full: bool = False,
            export_fields: Optional[list[str]] = None,
            pretty: bool = False, **kwargs
        ) -> str:
        """
        Serialize the entity to a JSON string.

        Args:
            full: Serialize all raw fields if True; else only export fields.
            export_fields: Optional list of field names to export.
            pretty: Pretty-print JSON if True.
            **kwargs: Additional args passed to `json.dumps`.

        Returns:
            str: JSON representation.
        """
        if pretty:
            kwargs.setdefault("indent", 2)
        return json.dumps(self.to_dict(full=full, export_fields=export_fields), **kwargs)

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        if isinstance(value, Enum):
            return value.value
        if hasattr(value, "to_dict") and callable(value.to_dict):
            return value.to_dict()
        if isinstance(value, (list, tuple)):
            return [BaseEntity._serialize_value(v) for v in value]
        if isinstance(value, dict):
            return {k: BaseEntity._serialize_value(v) for k, v in value.items()}
        return value
