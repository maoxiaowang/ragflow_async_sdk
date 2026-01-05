# User Guide

ragflow-async-sdk is a Python **asynchronous** SDK for interacting with **RAGFlow** services,
including datasets, documents, knowledge graphs (GraphRAG), RAPTOR
tasks, and chat/agent conversations.

This SDK is designed for: - asyncio-first usage - clear type models -
streaming (SSE) support for chat / agent completions - thin abstraction
over HTTP, without leaking httpx details to API users.

------------------------------------------------------------------------

## Installation

``` bash
pip install ragflow-async-sdk
```

------------------------------------------------------------------------

## Initialization

``` python
from ragflow_async_sdk.client import AsyncRAGFlowClient

client = AsyncRAGFlowClient(
    api_key="YOUR_API_KEY",
    base_url="http://your-ragflow-address"
)
```

The client internally manages: - authentication headers -
request/response validation - exception translation - streaming support

------------------------------------------------------------------------

## Dataset APIs

### List Datasets

``` python
datasets, total = await client.datasets.list_datasets(page=1, page_size=10)

for ds in datasets:
    print(ds.id, ds.name, ds.permission)

print("Total:", total)
```

------------------------------------------------------------------------

### Create Dataset

``` python
from ragflow_async_sdk.types.ingestion import ChunkMethod
from ragflow_async_sdk.types.permission import Permission

dataset = await client.datasets.create_dataset(
    name="my_dataset",
    chunk_method=ChunkMethod.NAIVE,
    permission=Permission.ME,
)
```

------------------------------------------------------------------------

### Update Dataset

``` python
await client.datasets.update_dataset(
    dataset_id=dataset.id,
    name="updated_name",
    description="Updated description",
)
```

------------------------------------------------------------------------

### Delete Datasets

``` python
# delete one
await client.datasets.delete_datasets(ids=[dataset.id])

# delete multiple
await client.datasets.delete_datasets(ids=["id1", "id2"])

# delete all
await client.datasets.delete_datasets(ids=None)
```

------------------------------------------------------------------------

## Document APIs

### Upload Documents

``` python
import aiofiles

files = [
    ("hello.txt", b"hello world", "text/plain"),
]

async with aiofiles.open("example.pdf", "rb") as f:
    files.append(("example.pdf", await f.read(), "application/pdf"))

docs, count = await client.datasets.upload_documents(
    dataset_id=dataset.id,
    files=files,
)

print("Uploaded:", count)
```

------------------------------------------------------------------------

### List Documents

``` python
documents, total = await client.datasets.list_documents(
    dataset_id=dataset.id,
    page=1,
    page_size=10,
)

for doc in documents:
    print(doc.id, doc.name, doc.run)
```

------------------------------------------------------------------------

### Update Document

``` python
doc = await client.datasets.update_document(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    name="manual.txt",
    parser_config={"chunk_token_num": 128},
)
```

------------------------------------------------------------------------

### Download Document

``` python
content = await client.datasets.download_document(
    dataset_id=dataset.id,
    document_id=doc.id,
)

with open("manual.txt", "wb") as f:
    f.write(content)
```

------------------------------------------------------------------------

### Parse Documents

``` python
# parse specific documents
await client.documents.parse_documents(dataset.id, [doc.id])

# parse failed documents only
failed_ids = [d.id for d in documents if d.run == "FAIL"]
await client.documents.parse_documents(dataset.id, failed_ids)
```

------------------------------------------------------------------------

### Stop Parsing

``` python
await client.documents.stop_parsing_documents(dataset.id, doc.id)
```

------------------------------------------------------------------------

## Knowledge Graph (GraphRAG)

### Get Knowledge Graph

``` python
kg = await client.datasets.get_knowledge_graph(dataset.id)

print("Nodes:", len(kg.nodes))
print("Edges:", len(kg.edges))
```

------------------------------------------------------------------------

### Construct Knowledge Graph

``` python
task_id = await client.datasets.construct_knowledge_graph(dataset.id)
print("Task ID:", task_id)
```

------------------------------------------------------------------------

### GraphRAG Status

``` python
status = await client.datasets.get_graphrag_status(dataset.id)

print(status.progress, status.progress_msg)
```

------------------------------------------------------------------------

### Delete Knowledge Graph

``` python
await client.datasets.delete_knowledge_graph(dataset.id)
```

------------------------------------------------------------------------

## RAPTOR

### Construct RAPTOR

``` python
task_id = await client.datasets.construct_raptor(dataset.id)
```

------------------------------------------------------------------------

### RAPTOR Status

``` python
status = await client.datasets.get_raptor_status(dataset.id)
print(status.progress, status.progress_msg)
```

------------------------------------------------------------------------

## Chat & Agent APIs

Both **chat** and **agent** share the same `ask()` interface and support
**streaming (SSE)**.

### Non-streaming Ask

``` python
answer = await client.chats.ask(
    parent_id=chat.id,
    session_id=session.id,
    prompt="你好",
)

print(answer.answer)
```

------------------------------------------------------------------------

### Streaming Ask (SSE)

``` python
async for chunk in await client.chats.ask(
    parent_id=chat.id,
    session_id=session.id,
    prompt="你好",
    stream=True,
):
    print(chunk.answer)
```

Notes: - The returned object is an `AsyncGenerator` - Each yielded item
is a `ChatCompletionResult` or `AgentCompletionResult` - Stream ends
automatically when server sends `data: true` or `[DONE]`

------------------------------------------------------------------------

## Exception Handling

All low-level httpx exceptions are translated into SDK-level exceptions.

``` python
from ragflow_async_sdk.exceptions import (
    RAGFlowAPIError,
    RAGFlowValidationError,
    RAGFlowTimeoutError,
)

try:
    await client.datasets.list_datasets()
except RAGFlowValidationError as e:
    print("Validation error:", e.message)
except RAGFlowTimeoutError:
    print("Timeout")
except RAGFlowAPIError as e:
    print("API error:", e.message, e.details)
```

------------------------------------------------------------------------

## Design Notes

-   Async-first (`async/await` everywhere)
-   Clear separation between:
    -   API layer
    -   HTTP transport
    -   models / types
-   Streaming implemented via SSE using `httpx.AsyncClient.stream`
-   No httpx objects are exposed to SDK users

------------------------------------------------------------------------

## License

Apache License 2.0
