import pytest_asyncio

from ragflow_async_sdk import AsyncRAGFlowClient
from .http import FakeAsyncClient
from ..http_fixtures import register_all_routes


@pytest_asyncio.fixture
async def client():
    server_url = "http://test"
    fake_httpx = FakeAsyncClient(server_url)
    register_all_routes(fake_httpx)

    async with AsyncRAGFlowClient(
        server_url=server_url,
        api_key="test",
        _http_client=fake_httpx,  # type: ignore
    ) as client:
        yield client
