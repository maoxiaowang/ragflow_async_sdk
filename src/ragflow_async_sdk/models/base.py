from enum import Enum
from typing import Any, TypeVar, Type
from dataclasses import fields, MISSING

T = TypeVar("T", bound="BaseEntity")


class BaseEntity:
    __export_fields__: tuple[str, ...] = ()
    _raw: dict[str, Any] = None

    def __init__(self, **kwargs):
        for field in self.__export_fields__:
            setattr(self, field, kwargs.get(field))
        self._raw: dict[str, Any] = kwargs.get("_raw", {})

    @classmethod
    def from_raw(cls: Type[T], raw: dict[str, Any]) -> T:
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

    def to_dict(self) -> dict[str, Any]:
        result = {}
        for field in self.__export_fields__:
            value = getattr(self, field, None)
            result[field] = self._serialize_value(value)
        return result

    def _serialize_value(self, value: Any) -> Any:
        if isinstance(value, Enum):
            return value.value
        if hasattr(value, "to_dict") and callable(value.to_dict):
            return value.to_dict()
        if isinstance(value, (list, tuple)):
            return [self._serialize_value(v) for v in value]
        if isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        return value
