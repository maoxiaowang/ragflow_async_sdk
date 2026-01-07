# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from datetime import datetime, timezone
from typing import Any

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
