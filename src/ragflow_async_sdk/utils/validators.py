from ragflow_async_sdk.exceptions import RAGFlowValidationError


def require_params(**params) -> None:
    """
    Ensure required parameters are provided (not None or empty string).

    Example:
        require_params(dataset_id=dataset_id, document_id=document_id)
    """
    for name, value in params.items():
        if value is None or value == "":
            raise RAGFlowValidationError(f"{name} is required")



