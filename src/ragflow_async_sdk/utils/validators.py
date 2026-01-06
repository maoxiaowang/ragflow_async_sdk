from enum import Enum
from typing import Optional, TypeVar

from ..exceptions import RAGFlowValidationError

T = TypeVar("T", bound=Enum)


def require_params(**params) -> None:
    """
    Ensure required parameters are provided (not None or empty string).

    Example:
        require_params(dataset_id=dataset_id, document_id=document_id)
    """
    for name, value in params.items():
        if value is None or value == "":
            raise RAGFlowValidationError(f"{name} is required")


def validate_enum(
    value: Optional[str | Enum],
    enum_class: type[T],
    param_name: Optional[str] = "value"
) -> Optional[T]:
    """
    Validate a value against an Enum and return its string representation.

    Args:
        value: The input value (str, Enum, or None).
        enum_class: Enum class to validate against.
        param_name: Parameter name for error messages.

    Returns:
        str or None: Enum value as string if valid, or None if input is None.

    Raises:
        RAGFlowValidationError: if value is invalid.
    """
    if value is None:
        return None

    if isinstance(value, str):
        try:
            value = enum_class(value)
        except ValueError:
            allowed = ", ".join(e.value for e in enum_class)
            raise RAGFlowValidationError(
                f"Invalid {param_name!r}: {value!r}. Allowed values: {allowed}"
            )

    if not isinstance(value, enum_class):
        raise RAGFlowValidationError(
            f"{param_name!r} must be of type {enum_class.__name__}, str, or None, "
            f"got {type(value).__name__}"
        )

    return value


def validate_file_tuples(
    files: list[tuple[str, bytes, str]],
    param_name: str = "files"
) -> None:
    """
    Validate that the input is a list of tuples in the form (filename, content_bytes, content_type).

    Args:
        files: The list to validate.
        param_name: Name of the parameter for error messages.

    Raises:
        TypeError: If the structure is invalid.
        ValueError: If any tuple does not have exactly 3 elements.
    """
    if not isinstance(files, list):
        raise TypeError(f"{param_name} must be a list, got {type(files).__name__}")

    for i, f in enumerate(files):
        if not isinstance(f, tuple):
            raise TypeError(f"{param_name}[{i}] must be a tuple, got {type(f).__name__}")
        if len(f) != 3:
            raise ValueError(
                f"{param_name}[{i}] must have exactly 3 elements "
                f"(filename, bytes, content_type), got {len(f)}"
            )
        filename, content, content_type = f
        if not isinstance(filename, str):
            raise TypeError(f"{param_name}[{i}][0] must be str, got {type(filename).__name__}")
        if not isinstance(content, (bytes, bytearray)):
            raise TypeError(f"{param_name}[{i}][1] must be bytes or bytearray, got {type(content).__name__}")
        if not isinstance(content_type, str):
            raise TypeError(f"{param_name}[{i}][2] must be str, got {type(content_type).__name__}")
