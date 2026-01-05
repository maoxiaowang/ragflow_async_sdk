from typing import Optional, Union, List

from ragflow_async_sdk.exceptions import RAGFlowValidationError


def normalize_ids(ids: Optional[Union[str, List[str]]], param_name: str = "ids") -> Optional[List[str]]:
    """
    Normalize an ID or a list of IDs into a list of strings.

    Args:
        ids: A string, a list of strings, or None.
        param_name: Parameter name for error messages.

    Returns:
        List of strings or None.

    Raises:
        RAGFlowValidationError: if the input type is invalid.
    """
    if ids is None:
        return None

    def validate_id(value: str) -> str:
        if not isinstance(value, str):
            raise RAGFlowValidationError(
                f"All elements in '{param_name}' must be strings"
            )
        if not value.strip():
            raise RAGFlowValidationError(
                f"'{param_name}' must contain at least one non-empty string"
            )
        return value

    if isinstance(ids, str):
        return [validate_id(ids)]

    if isinstance(ids, list):
        if not ids:
            raise RAGFlowValidationError(
                f"'{param_name}' must be a non-empty list of strings"
            )
        return [validate_id(i) for i in ids]

    raise RAGFlowValidationError(
        f"'{param_name}' must be a string, a list of strings, or None"
    )
