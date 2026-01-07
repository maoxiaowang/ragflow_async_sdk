import pytest

from ragflow_async_sdk.models import Chunk
from ragflow_async_sdk.models.agent import Agent
from ragflow_async_sdk.models.chat import ChatCompletionResult, ChatAssistant
from ragflow_async_sdk.models.dataset import Dataset
from ragflow_async_sdk.models.document import Document
from tests.utils.mock_ragflow_client import MockRAGFlowClient


@pytest.fixture
def mock_client():
    client = MockRAGFlowClient()
    yield client
    import asyncio
    asyncio.run(client.close())


# --------------------
# Dataset Tests
# --------------------

@pytest.mark.asyncio
async def test_create_dataset(mock_client):
    dataset = await mock_client.datasets.create_dataset(name="new_ds")
    assert isinstance(dataset, Dataset)
    assert dataset.name == "new_ds"


@pytest.mark.asyncio
async def test_list_datasets(mock_client):
    datasets, total = await mock_client.datasets.list_datasets()
    assert isinstance(datasets, list)
    assert isinstance(total, int)
    assert len(datasets) == total
    for ds in datasets:
        assert isinstance(ds, Dataset)


@pytest.mark.asyncio
async def test_get_dataset(mock_client):
    dataset = await mock_client.datasets.get_dataset(name="new_ds")
    assert isinstance(dataset, Dataset)
    assert dataset.name == "new_ds"


@pytest.mark.asyncio
async def test_update_dataset(mock_client):
    result = await mock_client.datasets.update_dataset("mock_id", name="updated_ds")
    assert result is None


@pytest.mark.asyncio
async def test_delete_dataset(mock_client):
    result = await mock_client.datasets.delete_datasets(["mock_id"])
    assert result is None


# --------------------
# Document Tests
# --------------------
@pytest.mark.asyncio
async def test_list_documents(mock_client):
    docs, total = await mock_client.documents.list_documents(dataset_id="1")
    assert isinstance(docs, list)
    assert len(docs) == total
    for doc in docs:
        assert isinstance(doc, Document)


@pytest.mark.asyncio
async def test_upload_document(mock_client):
    files = [("test.txt", b"content", "text/plain")]
    uploaded_docs, total = await mock_client.documents.upload_documents(dataset_id="1", files=files)
    assert len(uploaded_docs) == total
    for doc in uploaded_docs:
        assert isinstance(doc, Document)


# --------------------
# Chunk Tests
# --------------------
@pytest.mark.asyncio
async def test_list_chunks(mock_client):
    chunks, total = await mock_client.chunks.list_chunks(dataset_id="1")
    assert isinstance(chunks, list)
    assert len(chunks) == total
    for chunk in chunks:
        assert isinstance(chunk, Chunk)


# --------------------
# Chat Tests
# --------------------
@pytest.mark.asyncio
async def test_create_chat(mock_client):
    chat = await mock_client.chats.create_chat("domo-chat")
    assert isinstance(chat, ChatAssistant)
    assert chat.name == "domo-chat"

@pytest.mark.asyncio
async def test_chat_ask(mock_client):
    chat = await mock_client.chats.create_chat(name="demo-chat")
    session = await mock_client.chats.create_session(chat.id)
    result = await mock_client.chats.ask(chat.id, session.id, "Hello")
    assert isinstance(result, ChatCompletionResult)
    assert result.answer == "Hello from mock!"


@pytest.mark.asyncio
async def test_chat_ask_stream(mock_client):
    chat = await mock_client.chats.create_chat(name="demo-chat")
    session = await mock_client.chats.create_session(chat.id)
    result = mock_client.chats.ask_stream(chat.id, session.id, "Hello")
    async for chunk in result:
        assert isinstance(chunk, ChatCompletionResult)
        assert chunk.answer == "Hello from mock!"


# --------------------
# Agent Tests
# --------------------
@pytest.mark.asyncio
async def test_agent_create(mock_client):
    agent = await mock_client.agents.create_agent(title="new_agent")
    assert isinstance(agent, Agent)
    assert agent.title == "new_agent"


@pytest.mark.asyncio
async def test_list_agents(mock_client):
    agents, total = await mock_client.agents.list_agents()
    assert isinstance(agents, list)
    assert len(agents) == total
    for agent in agents:
        assert isinstance(agent, Agent)
