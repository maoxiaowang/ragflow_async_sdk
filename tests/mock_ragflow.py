import json
from pathlib import Path

import httpx
from ragflow_async_sdk.client import AsyncRAGFlowClient

class MockHandler:
    """Handle all requests from mock test"""

    def __init__(self, api_version: str="v1"):
        self.mock_dir = Path(__file__).parent / "mock"
        self._api_version = api_version
        # load JSON mock files
        self.list_datasets = json.loads((self.mock_dir / "mock_datasets.json").read_text())
        self.create_dataset = json.loads((self.mock_dir / "mock_dataset_create.json").read_text())
        # self.list_documents = json.loads((self.mock_dir / "mock_documents.json").read_text())
        # self.upload_document = json.loads((self.mock_dir / "mock_document_upload.json").read_text())

    def __call__(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        prefix = f"/api/{self._api_version}"
        if path.startswith(prefix):
            path = path[len(prefix):]
        method = request.method

        # mock API
        if path == "/datasets" and method == "GET":
            return httpx.Response(200, json=self.list_datasets)
        if path == "/datasets" and method == "POST":
            body = json.loads(request.content.decode()) if request.content else {}
            resp = self.create_dataset.copy()
            for key in ("name", "description"):
                if key in body:
                    resp["data"][key] = body[key]
            return httpx.Response(200, json=resp)

        return httpx.Response(404, json={"code": 404, "message": "Not Found"})


class MockRAGFlowClient:
    """AsyncRAGFlowClient wrapper"""

    def __init__(self, base_url="https://mock.ragflow.ai", api_key="test-key", api_version="v1"):
        self.client = AsyncRAGFlowClient(base_url, api_key, api_version=api_version)
        self._api_version = api_version
        self._setup_mock_transport()

        self.datasets = self.client.datasets

    def _setup_mock_transport(self):
        transport = httpx.MockTransport(MockHandler(api_version=self._api_version))
        self.client._http._client = httpx.AsyncClient(
            transport=transport,
            base_url="https://mock.ragflow.ai"
        )

    async def close(self):
        await self.client.close()
