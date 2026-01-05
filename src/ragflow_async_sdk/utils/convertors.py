from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

RFC_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"


def parse_time_field(value: Any) -> datetime | str | None:
    """
    Parse a datetime string like 'Tue, 30 Dec 2025 23:15:20 GMT' into a timezone-aware UTC datetime.
    Returns original value if parsing fails or value is not a string.
    """
    if isinstance(value, str):
        try:
            dt = datetime.strptime(value, RFC_DATE_FORMAT)
            return dt.replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            return value
    return value


def parse_enum(session_type: Optional[Enum | str]) -> Optional[str]:
    """
    Convert Enum object to string.
    - None -> None
    - Enum -> Enum's value
    - str -> str
    - other -> raise TypeError
    """
    if session_type is None:
        return None
    if isinstance(session_type, Enum):
        return session_type.value
    if isinstance(session_type, str):
        return session_type
    raise TypeError(
        f"session_type must be Enum, str, or None, "
        f"got {type(session_type).__name__}"
    )
