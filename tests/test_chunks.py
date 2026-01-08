import pytest

from ragflow_async_sdk.models import Chunk
from .fixtures.client import client


@pytest.mark.asyncio
async def test_add_chunk(client):
    dataset_id = "ds_id_1"
    document_id = "doc_id_1"
    content = "test_content"
    chunk = await client.chunks.add_chunk(
        dataset_id=dataset_id,
        document_id=document_id,
        content=content
    )
    assert isinstance(chunk, Chunk)
    assert chunk.dataset_id == dataset_id
    assert chunk.document_id == document_id
    assert chunk.content == content
    assert chunk.id is not None

# @pytest.mark.asyncio
# async def test_list_chunks(client):
#     chunks, total = await client.chunks.list_chunks(dataset_id="ds_id_1")
#     assert isinstance(chunks, list)
#     assert len(chunks) == total
#     for chunk in chunks:
#         assert isinstance(chunk, Chunk)
