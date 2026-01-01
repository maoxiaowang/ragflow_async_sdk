import pytest
from .mock_ragflow import MockRAGFlowClient

@pytest.fixture
def mock_client():
    return MockRAGFlowClient()
