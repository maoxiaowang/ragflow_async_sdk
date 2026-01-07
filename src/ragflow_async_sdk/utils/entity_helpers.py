# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from typing import List, TypeVar, Any, Optional

from ragflow_async_sdk.exceptions.api import RAGFlowNotFoundError, RAGFlowConflictError

T = TypeVar("T")


def get_single_or_raise(
    items: List[T],
    *,
    key_name: str,
    key_value: Any,
    entity_name: Optional[str] = None
) -> T:
    """
    Return a single item from a list, or raise exceptions if not found / multiple.

    Args:
        items: List of entities returned by a list API.
        key_name: Name of the field used in query (e.g., "id", "name").
        key_value: Value of the field used in query.
        entity_name: Optional entity class name for error messages. If None, will try to
                     infer from items[0], defaults to "Entity" if list is empty.

    Returns:
        Single entity instance.

    Raises:
        RAGFlowNotFoundError: If items is empty.
        RAGFlowConflictError: If multiple items match.
    """
    if not entity_name:
        entity_name = type(items[0]).__name__ if items else "Entity"

    if not items:
        raise RAGFlowNotFoundError(f"{entity_name} not found for {key_name}={key_value}")
    if len(items) > 1:
        raise RAGFlowConflictError(f"Multiple {entity_name}s found for {key_name}={key_value}")

    return items[0]
