import pytest
from tests.fixtures.client import client

from ragflow_async_sdk.models import Document


@pytest.mark.asyncio
async def test_list_documents(client):
    docs, total = await client.documents.list_documents("ds_1")
    assert isinstance(docs, list)
    assert len(docs) == total
    for doc in docs:
        assert isinstance(doc, Document)


@pytest.mark.asyncio
async def test_get_document(client):
    mock_doc_id = "doc_id_1"
    document = await client.documents.get_document("ds_id_1", document_id=mock_doc_id)
    assert isinstance(document, Document)
    assert document.id == mock_doc_id
    assert document.type == "doc"


@pytest.mark.asyncio
async def test_upload_document(client):
    files = [("test.txt", b"content", "text/plain")]
    uploaded_docs = await client.documents.upload_documents(dataset_id="ds_id_1", files=files)
    for doc in uploaded_docs:
        assert isinstance(doc, Document)
    assert len(files) == len(uploaded_docs)


@pytest.mark.asyncio
async def test_download_document(client):
    document = await client.documents.download_document("ds_id_1", "doc_id_1")
    assert document.filename == "doc_id_1"
    chunks = []
    async for chunk in document.stream:
        chunks.append(chunk)

    data = b"".join(chunks)
    assert data == b"file content"


@pytest.mark.asyncio
async def test_delete_documents(client):
    result = await client.documents.delete_documents("ds_id_1", ["doc_id_1"])
    assert result is None


@pytest.mark.asyncio
async def test_parse_documents(client):
    result = await client.documents.parse_documents("ds_id_1", ["doc_id_1"])
    assert result is None


@pytest.mark.asyncio
async def test_stop_parsing_documents(client):
    result = await client.documents.stop_parsing_documents("ds_id_1", ["doc_id_1"])
    assert result is None
