# API Reference

This document provides the complete API reference for ragflow-async-sdk, a Python asynchronous SDK
for interacting with RAGFlow services.

All APIs are **fully asynchronous** and designed to work with Python’s asyncio event loop.
API calls return structured **Entity objects** instead of raw JSON, offering:

- Typed attribute access (e.g. dataset.id)
- Serialization helpers (to_dict(), to_json())
- Access to original response data when needed

This reference focuses on **practical usage and API behavior**, including request parameters,
return values, and code examples.

> For installation instructions and high-level concepts, please refer to the project README.

## Table of Contents

- [Getting Started](#getting-started)
    - [Initialization](#initialization)
    - [Running with asyncio](#running-with-asyncio)
    - [Exceptions](#exceptions)
    - [Exception Handling](#exception-handling)
    - [Using Entities](#using-entities)

- [Dataset API](#-dataset-apis)
    - [Create Dataset](#-create-dataset)
    - [List Datasets](#-list-datasets)
    - [Get Dataset](#-get-dataset)
    - [Update Dataset](#-update-dataset)
    - [Delete Dataset](#-delete-datasets)

- [Document API](#-document-apis)
    - [Upload Documents](#-upload-documents)
    - [List Documents](#-list-documents)
    - [Get Document](#-get-document)
    - [Update Document](#-update-document)
    - [Delete Documents](#-delete-documents)
    - [Download Document](#-download-document)
    - [Parse Documents](#-parse-documents)
    - [Stop Parsing Document](#-stop-parsing-document)

- [Chunk API](#-chunk-apis)
    - [Add Chunk](#-add-chunk)
    - [List Chunks](#-list-chunks)
    - [Get Chunk](#-get-chunk)
    - [Update Chunk](#-update-chunk)
    - [Delete Chunks](#-delete-chunks)

- [Chat API](#-chat-apis)
    - [Create Chat Assistant](#-create-chat)
    - [List Chat Assistants](#-list-chats)
    - [Get Chat Assistant](#-get-chat)
    - [Update Chat Assistant](#-update-chat)
    - [Delete Chat Assistants](#-delete-chats)
    - [Create Chat Session](#-create-chat-session)
    - [List Chat Session](#-list-chat-sessions)
    - [Get Chat Session](#-get-chat-session)
    - [Update Chat Session](#-update-chat-session)
    - [Delete Chat Session](#-delete-chat-sessions)
    - [Ask in Chat Session](#-ask-in-chat-session)

- [Agent API](#-agent-apis)
    - [Create Agent](#-create-agent)
    - [List Agents](#-list-agents)
    - [Get Agent](#-get-agent)
    - [Update Agent](#-update-agent)
    - [Delete Agent](#-delete-agent)
    - [Create Agent Session](#-create-agent-session)
    - [List Agent Sessions](#-list-agent-sessions)
    - [Get Agent Session](#-get-agent-session)
    - [Update Agent Session](#-update-agent-session)
    - [Delete Agent Sessions](#-delete-agent-sessions)
    - [Ask in Agent Session](#-ask-in-agent-session)

- [File API](#-file-apis)
    - [Upload Files](#-upload-files)
    - [Download File](#-download-file)
    - [List Files](#-list-files)
    - [Delete Files](#-delete-files)
    - [Create File or Folder](#-create-file-or-folder)
    - [Get Root Folder](#-get-root-folder)
    - [Get Parent Folder](#-get-parent-folder)
    - [Get All Parent Folders](#-get-all-parent-folders)
    - [Rename File](#-rename-file)
    - [Remove Files](#-move-files)
    - [Convert Files](#-convert-files)

- [System API](#-system-apis)
    - [Health Check](#-health-check)

## Getting Started

This section provides a quick introduction for beginners on how to initialize the client,
run asynchronous operations, handle exceptions, and use SDK entities.

### Initialization

```python
from ragflow_async_sdk import AsyncRAGFlowClient

client = AsyncRAGFlowClient(
    server_url="http://your-ragflow-address",
    api_key="YOUR_API_KEY"
)
```

### Running With asyncio

This SDK uses asynchronous APIs. To run examples, use Python's asyncio event loop.

```python
import asyncio
from ragflow_async_sdk import AsyncRAGFlowClient


async def main():
    client = AsyncRAGFlowClient(
        server_url="http://your-ragflow-address",
        api_key="YOUR_API_KEY"
    )
    # Example: Health check
    system_health = await client.systems.healthz()
    print(system_health.status, system_health.details)


# Run the async main function
asyncio.run(main()) 
```

### Using Entities

SDK entities such as Dataset, File, or Agent provide convenient methods and attributes.

```python
dataset = await client.datasets.get_dataset(dataset_id="123")

# Access attributes
print(dataset.id, dataset.name)

# Convert to dictionary with selected fields
dataset_dict = dataset.to_dict(export_fields=["id", "name"])
print(dataset_dict)

# Convert to pretty JSON string
dataset_json = dataset.to_json(pretty=True)
print(dataset_json)

# Access raw response data if needed
raw_data = dataset._raw
```

### Exceptions

All SDK APIs may raise the following exceptions:

- `RAGFlowAPIError`: Generic API failure (non-validation, non-timeout, etc.)
- `RAGFlowConfigError`: Invalid SDK configurations
- `RAGFlowValidationError`: Invalid or missing parameters
- `RAGFlowTimeoutError`: Request timed out
- `RAGFlowConnectionError`: Connection failure
- `RAGFlowTransportError`: Network/transport error
- `RAGFlowHTTPResponseError`: Invalid or non-JSON HTTP response

> 💡 All module methods may raise these exceptions.
> Module-specific exceptions (like `RAGFlowNotFoundError`) are documented in the corresponding API section.

### Exception Handling

The SDK may raise exceptions like `RAGFlowAPIError` or `RAGFlowValidationError`.
Catch them using `try/except` blocks:

```python
from ragflow_async_sdk.exceptions import RAGFlowAPIError, RAGFlowValidationError

try:
    system_health = await client.systems.healthz()
    print(system_health.status, system_health.details)
except RAGFlowValidationError as ve:
    print("Validation error:", ve)
except RAGFlowAPIError as ae:
    print("API error:", ae)
```

### Common List Parameters

💡 The following parameters are supported by all list APIs unless otherwise noted.

| Parameter | Type    | Description                          |
|-----------|---------|--------------------------------------|
| page      | int     | Page number (default=1)              |
| page_size | int     | Items per page (default=30)          |
| order_by  | OrderBy | Sort field (defaults to create_time) |
| desc      | bool    | Sort descending (default=True)       |

> `OrderBy` is an enum defining sortable fields for each resource (e.g., create_time, update_time).

---

## 🧩 Dataset APIs

### ⚡ Create Dataset

Create a new dataset.

**Parameters:**

| Parameter | Type | Description         |
|-----------|------|---------------------|
| name      | str  | Name of the dataset |

**Returns:**

- `Dataset` instance

**Raises:**

- `RAGFlowValidationError`: If `name` is missing or invalid
- `RAGFlowAPIError`: If creation fails

**Example:**

```python
from ragflow_async_sdk.exceptions import RAGFlowAPIError

try:
    dataset = await client.datasets.create_dataset(name="my_dataset")
    print(dataset.id, dataset.name)
except RAGFlowAPIError as e:
    print("Failed to create dataset:", e)
```

---

### ⚡ List Datasets

Retrieve a paginated list of datasets, optionally filtered by name.

**Parameters**

| Parameter  | Type | Description                      |
|------------|------|----------------------------------|
| dataset_id | str  | Optional: filter by dataset ID   |
| name       | str  | Optional: filter by dataset name |

> 💡 This API supports common list parameters: `page`, `page_size`, `order_by`, `desc`.

**Returns**

- Tuple `(datasets, total)`
    - `datasets`: List of `Dataset` instances
    - `total`: Total number of datasets matching the filter

**Example**

```python
datasets, total = await client.datasets.list_datasets(page=1, page_size=30)
datasets, total = await client.datasets.list_datasets(name="my_dataset")
```

### ⚡ Get Dataset

Get a single dataset by ID or name.

**Parameters**

| Parameter  | Type | Description                                         |
|------------|------|-----------------------------------------------------|
| dataset_id | str  | Dataset ID (optional if `name` is provided)         |
| name       | str  | Dataset name (optional if `dataset_id` is provided) |

> 💡 Exactly one of `dataset_id` or `name` must be provided.

**Returns**

- `Dataset` instance

**Raises**

- `RAGFlowNotFoundError`: If no dataset matches the given identifier
- `RAGFlowConflictError`: If multiple datasets match the query

**Example**

```python
dataset = await client.datasets.get_dataset(dataset_id="dataset_123")
assert dataset.id == "dataset_123"

dataset = await client.datasets.get_dataset(name="my_dataset")
assert dataset.name == "my_dataset"
```

---

### ⚡ Update Dataset

Update properties of an existing dataset.

**Parameters**

| Parameter  | Type | Description                         |
|------------|------|-------------------------------------|
| dataset_id | str  | Dataset ID                          |
| name       | str  | New name for the dataset (optional) |

**Returns**

- `None`

**Raises**

- `RAGFlowAPIError`: If update fails
- `RAGFlowValidationError`: If required parameters are missing

**Example**

```python
await client.datasets.update_dataset(dataset.id, name="new_name")
```

---

### ⚡ Delete Datasets

Delete one, multiple, or all datasets.

**Parameters**

| Parameter | Type              | Description                                                    |
|-----------|-------------------|----------------------------------------------------------------|
| ids       | List[str] or None | List of dataset IDs to delete. If `None`, deletes all datasets |

> ⚠️ If `ids` is None, all datasets will be permanently deleted.

**Returns**

- `None`

**Raises**

- `RAGFlowAPIError`: If deletion fails

**Example**

```python
# Delete one
await client.datasets.delete_datasets(ids=[dataset.id])

# Delete multiple
await client.datasets.delete_datasets(ids=["id1", "id2"])

# Delete all
await client.datasets.delete_datasets(ids=None)
```

---

## 🧩 Document APIs

### ⚡ Upload Documents

Upload multiple documents to a dataset. Returns a list of uploaded `Document` instances and total count.

**Parameters**

| Parameter  | Type                         | Description                                                |
|------------|------------------------------|------------------------------------------------------------|
| dataset_id | str                          | Target dataset ID                                          |
| files      | List[Tuple[str, bytes, str]] | Each document as `(filename, content_bytes, content_type)` |

**Returns**

- List of uploaded `Document` instances

**Example**

Prepare the files using [Prepare Upload Files](utilities-reference.md#prepare-upload-files) or manually:

```python
from ragflow_async_sdk.types.ingestion import ChunkMethod

files_to_send = [
    ("hello.txt", b"hello world", "text/plain"),
]

uploaded_docs, total = await client.documents.upload_documents(
    dataset_id=dataset.id,
    files=files_to_send,
    chunk_method=ChunkMethod.NAIVE
)

print(f"Uploaded {total} documents")
```

> 💡 Each file should be provided as a tuple: (filename: str, content_bytes: bytes, content_type: str).
>
> ⚠️ Using `file_from_path` requires aiofiles: `pip install aiofiles`

### ⚡ List Documents

Retrieve a paginated list of documents in a dataset.

**Parameters**

| Parameter  | Type | Description              |
|------------|------|--------------------------|
| dataset_id | str  | Target dataset ID        |
| keywords   | str  | Optional search keywords |

> 💡 This API supports common list parameters: `page`, `page_size`, `order_by`, `desc`.

**Returns**

- Tuple `(documents, total)`
    - `documents`: List of `Document` instances
    - `total`: Total number of documents matching the query

**Example**

```python
documents, total = await client.documents.list_documents(
    dataset_id=dataset.id,
    page=1,
    page_size=20,
    keywords="report"
)

for doc in documents:
    print(doc.id, doc.name)
print("Total:", total)
```

### ⚡ Get Document

Get a single document by ID or name within a dataset.

**Parameters**

| Parameter   | Type          | Description           |
|-------------|---------------|-----------------------|
| dataset_id  | str           | Dataset ID (required) |
| document_id | Optional[str] | Document ID           |
| name        | Optional[str] | Document name         |

> 💡 Exactly one of `document_id` or `name` must be provided.

**Returns**

- `Document` instance

**Raises**

- `RAGFlowNotFoundError`: If no document matches

**Example**

```python
document = await client.datasets.get_document(
    dataset_id=dataset.id,
    name="user_manual.pdf"
)

if document:
    print(document.id, document.name)
```

### ⚡ Update Document

Update a document's properties.

**Parameters**

| Parameter     | Type        | Description                                |
|---------------|-------------|--------------------------------------------|
| dataset_id    | str         | Target dataset ID (required)               |
| document_id   | str         | Document ID (required)                     |
| name          | str         | New document name (optional)               |
| meta_fields   | dict        | Metadata fields (optional)                 |
| chunk_method  | ChunkMethod | Chunking method (optional)                 |
| parser_config | dict        | Parser configuration (optional)            |
| enabled       | bool        | Whether the document is enabled (optional) |

**Returns**

- `None`

**Example**

```python
await client.documents.update_document(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    name="manual_updated.txt",
    parser_config={"chunk_token_num": 128}
)
```

---

### ⚡ Delete Documents

Delete a document from a dataset.

**Parameters**

| Parameter  | Type      | Description       |
|------------|-----------|-------------------|
| dataset_id | str       | Target dataset ID |
| ids        | list[str] | Document ID       |

> ⚠️ If `ids` is None, all datasets will be permanently deleted.

**Returns**

- `True` on success

**Raises**

- `RAGFlowAPIError`: If deletion fails

**Example**

```python
success = await client.documents.delete_document(
    dataset_id=dataset.id,
    ids=[documents[0].id]
)
if success:
    print("Document deleted successfully")
```

---

### ⚡ Download Document

Download a document's content as bytes.

**Parameters**

| Parameter   | Type | Description       |
|-------------|------|-------------------|
| dataset_id  | str  | Target dataset ID |
| document_id | str  | Document ID       |

**Returns**

- `bytes`: Raw file content as bytes. Can be used to save the file locally or process in memory.

**Example**

```python
import aiofiles

content = await client.documents.download_document(
    dataset_id=dataset.id,
    document_id=documents[0].id
)

async with aiofiles.open("downloaded_manual.txt", "wb") as f:
    await f.write(content)
```

---

### ⚡ Parse Documents

Trigger parsing/chunking for one or more documents.

> 💡 This operation runs asynchronously in the background.
> The API call returns immediately; parsing may take some time to complete.


**Parameters**

| Parameter    | Type      | Description           |
|--------------|-----------|-----------------------|
| dataset_id   | str       | Target dataset ID     |
| document_ids | list[str] | Document IDs to parse |

**Returns**

- `None`

**Example**

```python
# Parse all documents
await client.documents.parse_documents(dataset.id, [doc.id for doc in documents])

# Parse only failed documents
failed_ids = [d.id for d in documents if d.run == "FAIL"]
await client.documents.parse_documents(dataset.id, failed_ids)
```

### ⚡ Stop Parsing Document

Stop parsing a document.

> ⚠️ Stopping parsing will mark the document as `FAIL`. Any ongoing parsing is immediately halted.

**Parameters**

| Parameter   | Type | Description       |
|-------------|------|-------------------|
| dataset_id  | str  | Target dataset ID |
| document_id | str  | Document ID       |

**Returns**

- `None`

**Example**

```python
await client.documents.stop_parsing_documents(dataset.id, documents[0].id)
```

---

## 🧩 Chunk APIs

The Chunk API allows managing document chunks, including adding, listing, updating, deleting, retrieving, and handling
document-level metadata.

> 💡 **Note:**  
> Chunk-related APIs are divided into two categories:
> - **Browsing APIs** (`list_chunks`, `get_chunk`) for structured access
> - **Retrieval APIs** (`retrieve_chunks`) for semantic search
>
> Retrieval results are **not guaranteed** to be stable or unique entities.

### ⚡ Add Chunk

Add a new chunk to a document.

**Parameters**

| Parameter          | Type                | Description                            |
|--------------------|---------------------|----------------------------------------|
| dataset_id         | str                 | Dataset containing the document        |
| document_id        | str                 | Target document ID                     |
| content            | str                 | Text content of the chunk              |
| important_keywords | Optional[list[str]] | Keywords highlighting chunk importance |
| questions          | Optional[list[str]] | Questions associated with the chunk    |

**Returns**

- `Chunk` instance

**Example**

```python
chunk_data = await client.chunks.add_chunk(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    content="This is a chunk",
    important_keywords=["important", "key"],
    questions=["What is this chunk about?"]
)
print(chunk_data)
```

### ⚡ List Chunks

List chunks in a document with optional filters.

**Parameters**

| Parameter   | Type          | Description                       |
|-------------|---------------|-----------------------------------|
| dataset_id  | str           | Dataset containing the document   |
| document_id | str           | Target document ID                |
| keywords    | Optional[str] | Optional search keywords          |
| chunk_id    | Optional[str] | Optional specific chunk ID filter |

> 💡 This API supports common list parameters: `page`, `page_size`, `order_by`, `desc`.

**Returns**

- Tuple `(chunks, total)`
    - `chunks`: List of `Chunk` instances
    - `total`: Total number of chunks matching the query

**Example**

```python
chunks, total = await client.chunks.list_chunks(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    page=1,
    page_size=20
)
print(chunks, total)
```

---

### ⚡ Get Chunk

Get a single chunk by ID within a document.

> 💡 For structured access only. For semantic search, use `retrieve_chunks`.

**Parameters**

| Parameter   | Type | Description            |
|-------------|------|------------------------|
| dataset_id  | str  | Dataset ID (required)  |
| document_id | str  | Document ID (required) |
| chunk_id    | str  | Chunk ID (required)    |

**Returns**

- `Chunk` instance

**Raises**

- `RAGFlowNotFoundError`: If chunk not found
- `RAGFlowConflictError`: If multiple chunks match the ID (unexpected)

**Example**

```python
chunk = await client.chunks.get_chunk(
    dataset_id=dataset.id,
    document_id=document.id,
    chunk_id="chunk_456"
)
print(chunk.id, chunk.content)
```

### ⚡ Update Chunk

Update content or settings for a specific chunk.

**Parameters**

| Parameter          | Type                | Description                        |
|--------------------|---------------------|------------------------------------|
| dataset_id         | str                 | Dataset containing the document    |
| document_id        | str                 | Document ID                        |
| chunk_id           | str                 | Chunk ID to update                 |
| content            | Optional[str]       | New content for the chunk          |
| important_keywords | Optional[list[str]] | Updated list of important keywords |
| available          | Optional[bool]      | Whether the chunk is available     |

**Returns**

- `None`

**Example**

```python
await client.chunks.update_chunk(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    chunk_id=chunk.id,
    content="Updated content",
    important_keywords=["updated", "key"],
    available=True
)
```

### ⚡ Delete Chunks

Delete chunks by ID or delete all if none provided.

**Parameters**

| Parameter   | Type                    | Description                                          |
|-------------|-------------------------|------------------------------------------------------|
| dataset_id  | str                     | Dataset containing the document                      |
| document_id | str                     | Document ID                                          |
| chunk_ids   | Optional[str/list[str]] | List of chunk IDs to delete, or `None` to delete all |

**Returns**

- `None`

**Example**

```python
await client.chunks.delete_chunks(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    chunk_ids=[chunk.id]
)
```

### ⚡ Get Metadata Summary

Retrieve a metadata summary for all documents in a dataset.

**Parameters**

| Parameter  | Type | Description |
|------------|------|-------------|
| dataset_id | str  | Dataset ID  |

**Returns**

- `dict`: Metadata summary

**Example**

```python
summary = await client.chunks.get_metadata_summary(dataset.id)
print(summary)
```

### ⚡ Update Metadata

Batch update or delete document-level metadata.

**Parameters**

| Parameter  | Type                 | Description                                                 |
|------------|----------------------|-------------------------------------------------------------|
| dataset_id | str                  | Dataset ID                                                  |
| selector   | Optional[dict]       | Filter documents, e.g., {"document_ids": [...]}             |
| updates    | Optional[list[dict]] | Metadata updates [{"key": str, "match": str, "value": str}] |
| deletes    | Optional[list[dict]] | Metadata deletions [{"key": str, "value": Optional[str]}]   |

**Returns**

- `dict`: Result summary of updates/deletions

**Example**

```python
result = await client.chunks.update_metadata(
    dataset_id=dataset.id,
    updates=[{"key": "topic", "match": "old", "value": "new"}],
    deletes=[{"key": "obsolete"}]
)
print(result)
```

### ⚡ Retrieve Chunks

Retrieve chunks from datasets or documents based on a query. Supports filtering, reranking, keyword search, and
knowledge-graph enhanced search.

**Parameters**

| Parameter                | Type                    | Description                                                        |
|--------------------------|-------------------------|--------------------------------------------------------------------|
| question                 | str                     | Query string or keywords (required)                                |
| dataset_ids              | Optional[str/list[str]] | Dataset IDs to search                                              |
| document_ids             | Optional[str/list[str]] | Document IDs to search                                             |
| page                     | int                     | Page number (default: 1)                                           |
| page_size                | int                     | Number of chunks per page (default: 30)                            |
| similarity_threshold     | float                   | Minimum similarity score (default: 0.2)                            |
| vector_similarity_weight | float                   | Weight of vector similarity (default: 0.3)                         |
| top_k                    | int                     | Number of chunks considered for vector computation (default: 1024) |
| rerank_id                | Optional[str]           | Optional rerank model ID                                           |
| keyword                  | bool                    | Enable keyword-based matching (default: False)                     |
| highlight                | bool                    | Highlight matched terms (default: False)                           |
| cross_languages          | Optional[list[str]]     | Target languages for translation                                   |
| metadata_condition       | Optional[dict]          | Metadata filter conditions                                         |
| use_kg                   | bool                    | Enable knowledge graph multi-hop search (default: False)           |
| toc_enhance              | bool                    | Enable table-of-contents enhanced search (default: False)          |

**Returns**

- `dict` containing:
    - `chunks`: List of retrieved chunk dicts
    - `total`: Total number of matching chunks
    - `document_aggregations`: Aggregated metadata per document

**Example**

```python
retrieved = await client.chunks.retrieve_chunks(
    question="What are the key features of async Python?",
    dataset_ids=[dataset.id],
    page=1,
    page_size=10,
    similarity_threshold=0.25,
    keyword=True,
    highlight=True
)

chunks = retrieved.get("chunks", [])
total = retrieved.get("total", 0)
aggregations = retrieved.get("document_aggregations", {})

print(f"Total chunks found: {total}")
for chunk in chunks:
    print(chunk["content"])
```

---

## 🧩 Chat APIs

The Chat API allows you to manage chat assistants and their sessions, including creating, listing, updating, deleting,
and sending messages with optional streaming.

### ⚡ Create Chat

Create a new chat assistant.

**Parameters**

| Parameter   | Type                | Description                             |
|-------------|---------------------|-----------------------------------------|
| name        | str                 | Chat assistant name (required)          |
| dataset_ids | Optional[list[str]] | Optional list of associated dataset IDs |
| avatar      | Optional[str]       | Optional avatar URL                     |
| llm         | Optional[dict]      | Optional LLM configuration              |
| prompt      | Optional[dict]      | Optional prompt configuration           |

**Returns**

- `ChatAssistant` instance

**Example**

```python
chat = await client.chats.create_chat(
    name="demo-chat",
    dataset_ids=[dataset.id],
    avatar="http://example.com/avatar.png",
    llm={"model": "gpt-4"},
    prompt={"system": "You are a helpful assistant"}
)
print(chat.id, chat.name)
```

### ⚡ List Chats

List chat assistants with optional filters.

**Parameters**

| Parameter | Type          | Description                              |
|-----------|---------------|------------------------------------------|
| page      | int           | Page number (default 1)                  |
| page_size | int           | Number of items per page (default 30)    |
| orderby   | str           | Field to sort by (default `create_time`) |
| desc      | bool          | Sort descending if True (default True)   |
| chat_id   | Optional[str] | Filter by chat ID                        |
| name      | Optional[str] | Filter by chat name                      |

> 💡 This API supports common list parameters: `page`, `page_size`, `order_by`, `desc`.

**Returns**

- Tuple `(chats, total)`
    - `chats`: List of `ChatAssistant` instances
    - `total`: Total number of chats matching the query

**Example**

```python
chats, total = await client.chats.list_chats(page=1, page_size=50)
for c in chats:
    print(c.id, c.name)
```

### ⚡ Get Chat

Get a single chat assistant by ID or name.

**Parameters**

| Parameter | Type          | Description         |
|-----------|---------------|---------------------|
| chat_id   | Optional[str] | Chat assistant ID   |
| name      | Optional[str] | Chat assistant name |

> Exactly one of `chat_id` or `name` must be provided.

**Returns**

- `ChatAssistant` instance

**Raises**

- `RAGFlowNotFoundError`: If match not found
- `RAGFlowConflictError`: If multiple chats match the ID or name (unexpected)

**Example**

```python
chat = await client.chats.get_chat(name="support-bot")
print(chat.id, chat.name)
```

### ⚡ Update Chat

Update an existing chat assistant.

**Parameters**

| Parameter   | Type                | Description                  |
|-------------|---------------------|------------------------------|
| chat_id     | str                 | Chat assistant ID (required) |
| name        | Optional[str]       | New chat name                |
| dataset_ids | Optional[list[str]] | Updated dataset IDs          |
| avatar      | Optional[str]       | Updated avatar URL           |
| llm         | Optional[dict]      | Updated LLM configuration    |
| prompt      | Optional[dict]      | Updated prompt configuration |

**Returns**

- `None`

**Example**

```python
await client.chats.update_chat(
    chat_id=chat.id,
    name="updated-chat",
    avatar="http://example.com/new_avatar.png"
)
```

### ⚡ Delete Chats

Delete one or more chat assistants.

**Parameters**

| Parameter | Type               | Description                                             |
|-----------|--------------------|---------------------------------------------------------|
| ids       | Optional[str/list] | Single or list of chat IDs. If None, deletes all chats. |

**Returns**

- `None`

**Example**

```python
await client.chats.delete_chats(ids=[chat.id])
```

### ⚡ Create Chat Session

Create a new session under a chat assistant.

**Parameters**

| Parameter | Type          | Description           |
|-----------|---------------|-----------------------|
| chat_id   | str           | Chat assistant ID     |
| name      | Optional[str] | Optional session name |
| user_id   | Optional[str] | Optional user ID      |

**Returns**

- `ChatSession` instance

**Example**

```python
session = await client.chats.create_session(
    chat_id=chat.id,
    name="demo-session",
    user_id="user123"
)
print(session.id, session.chat_id)
```

### ⚡ List Chat Sessions

List sessions for a specific chat assistant.

> Uses `SessionMixin.list_sessions` internally.

**Parameters**

| Parameter  | Type          | Description                     |
|------------|---------------|---------------------------------|
| chat_id    | str           | Chat assistant ID (required)    |
| name       | Optional[str] | Optional filter by session name |
| session_id | Optional[str] | Optional filter by session ID   |
| user_id    | Optional[str] | Optional filter by user ID      |

**Returns**

- Tuple (list of `ChatSession` instances, total count)

**Example**

```python
sessions, total = await client.chats.list_sessions(chat_id="chat_123")
for s in sessions:
    print(s.id, s.name)
```

### ⚡ Get Chat Session

Get a specific chat session.

**Parameters**

| Parameter  | Type          | Description                     |
|------------|---------------|---------------------------------|
| chat_id    | str           | Chat assistant ID (required)    |
| name       | Optional[str] | Optional filter by session name |
| session_id | Optional[str] | Optional filter by session ID   |

**Returns**

- `ChatSession` instance

**Raises**

- `RAGFlowNotFoundError`: If chat session not found
- `RAGFlowConflictError`: If multiple sessions match the ID (unexpected)

**Example**

```python
sessions, total = await client.chats.get_session(session_id="session_123")
for s in sessions:
    print(s.id, s.chat_id, s.name)
```

### ⚡ Update Chat Session

Update a session under a chat assistant.

**Parameters**

| Parameter  | Type          | Description          |
|------------|---------------|----------------------|
| chat_id    | str           | Chat assistant ID    |
| session_id | str           | Session ID           |
| name       | Optional[str] | Optional new name    |
| user_id    | Optional[str] | Optional new user ID |

**Returns**

- `None`

**Example**

```python
await client.chats.update_session(
    chat_id=chat.id,
    session_id=session.id,
    name="updated-session"
)
```

### ⚡ Delete Chat Sessions

Delete one or more chat sessions.

**Parameters**

| Parameter   | Type               | Description                                        |
|-------------|--------------------|----------------------------------------------------|
| chat_id     | str                | Chat assistant ID                                  |
| session_ids | Optional[str/list] | Single or list of session IDs; if None, delete all |

**Returns**

- `None`

**Example**

```python
await client.chats.delete_sessions(chat_id=chat.id, session_ids=[session.id])
```

### ⚡ Ask in Chat Session

Send a prompt to a chat session, optionally streaming the response.

**Parameters**

| Parameter  | Type                  | Description                                 |
|------------|-----------------------|---------------------------------------------|
| chat_id    | str                   | Chat assistant ID                           |
| session_id | str                   | Session ID                                  |
| prompt     | str                   | User question                               |
| stream     | bool                  | Whether to return streaming results         |
| **kwargs   | Additional parameters | Extra parameters (temperature, top_p, etc.) |

**Returns**

- `ChatCompletionResult` instance if `stream=False`.
- async generator `ChatCompletionResult` if `stream=True`.

**Example**

- Non-streaming:

```python
answer = await client.chats.ask(
    chat_id=chat.id,
    session_id=session.id,
    prompt="Hello, how are you?"
)
print(answer.answer)
```

- Streaming:

```python
async for chunk in await client.chats.ask(
        chat_id=chat.id,
        session_id=session.id,
        prompt="Hello, how are you?",
        stream=True
):
    print(chunk.answer, end='', flush=True)
```

---

## 🧩 Agent APIs

The Agent API allows you to manage agents and their sessions, including creating, listing, updating, deleting, and
managing sessions.

### ⚡ Create Agent

Create a new agent.

**Parameters**

| Parameter   | Type          | Description                                                                      |
|-------------|---------------|----------------------------------------------------------------------------------|
| title       | str           | Agent title (required)                                                           |
| dsl         | dict          | Agent DSL configuration, including graph, components, retrieval, etc. (required) |
| description | Optional[str] | Optional description of the agent                                                |

#**Returns**

- `Agent` instance

**Example**

```python
agent = await client.agents.create_agent(
    title="demo-agent",
    dsl={
        "graph": {...},
        "components": {...},
        "retrieval": {...}
    },
    description="A test agent"
)
print(agent.id, agent.title)
```

### ⚡ List Agents

List agents with optional filters.

**Parameters**

| Parameter | Type          | Description           |
|-----------|---------------|-----------------------|
| agent_id  | Optional[str] | Filter by agent ID    |
| title     | Optional[str] | Filter by agent title |

> 💡 **Note:** Supports common list parameters for pagination and sorting: `page`, `page_size`, `order_by`, `desc`.

**Returns**

- Tuple (list of `ChatSession` instances, total count)

**Example**

```python
agents, total = await client.agents.list_agents(page=1, page_size=50)
for a in agents:
    print(a.id, a.title)
```

### ⚡ Get Agent

Retrieve a single agent by ID or title. Only one of `agent_id` or `title` should be provided.

**Parameters**

| Parameter | Type          | Description |
|-----------|---------------|-------------|
| agent_id  | Optional[str] | Agent ID    |
| title     | Optional[str] | Agent title |

**Raises**

- `RAGFlowNotFoundError`: If chat session not found
- `RAGFlowConflictError`: If multiple sessions match the ID (unexpected)

**Example**

```python
agent = await client.agents.get_agent(agent_id="agent123")
# or
agent = await client.agents.get_agent(title="demo-agent")
```

### ⚡ Update Agent

Update an existing agent by its ID. Only specify the fields you want to change.

**Parameters**

| Parameter   | Type           | Description                    |
|-------------|----------------|--------------------------------|
| agent_id    | str            | Agent ID (required)            |
| title       | Optional[str]  | New title of the agent         |
| description | Optional[str]  | New description of the agent   |
| dsl         | Optional[dict] | Canvas DSL object of the agent |

**Returns**: 

- `None`

**Example**

```python
await client.agents.update_agent(
    agent_id="58af890a2a8911f0a71a11b922ed82d6",
    title="Test Agent",
    description="A test agent",
    dsl={"nodes": [], "edges": []},
)
```

### ⚡ Delete Agent

Delete an agent by ID.

**Parameters**

| Parameter | Type | Description         |
|-----------|------|---------------------|
| agent_id  | str  | Agent ID (required) |

**Returns**: 

- `None`

**Example**

```python
success = await client.agents.delete_agent(agent_id=agent.id)
print(success)
```

### ⚡ Create Agent Session

Create a new session under an agent.

**Parameters**

| Parameter | Type          | Description                                   |
|-----------|---------------|-----------------------------------------------|
| agent_id  | str           | Agent ID (required)                           |
| name      | str           | Optional session name (default "New session") |
| user_id   | Optional[str] | Optional user ID                              |

**Returns**: 

- `AgentSession` instance

**Example**

```python
session = await client.agents.create_session(
    agent_id=agent.id,
    name="demo-session",
    user_id="user123"
)
print(session.id, session.name)
```

### ⚡ List Agent Sessions

List sessions for an agent.

**Parameters**

| Parameter  | Type          | Description            |
|------------|---------------|------------------------|
| agent_id   | str           | Agent ID (required)    |
| name       | Optional[str] | Filter by session name |
| session_id | Optional[str] | Filter by session ID   |
| user_id    | Optional[str] | Filter by user ID      |

> 💡 **Note:** Supports common list parameters for pagination and sorting: `page`, `page_size`, `order_by`, `desc`.

**Returns**: 

- Tuple (list of `AgentSession` instance, total count)

**Example**

```python
sessions, total = await client.agents.list_sessions(agent_id=agent.id)
for s in sessions:
    print(s.id, s.name)
```

### ⚡ Get Agent Session

Get a single session for a specific agent by session_id or name.

**Parameters**

| Parameter  | Type          | Description                                                    |
|------------|---------------|----------------------------------------------------------------|
| agent_id   | str           | Agent ID (required)                                            |
| session_id | Optional[str] | Session ID to fetch (exactly one required with `name`)         |
| name       | Optional[str] | Session name to fetch (exactly one required with `session_id`) |

**Returns**

- `AgentSession` instance

**Raises**

- `RAGFlowConflictError`: If multiple sessions match the query
- `RAGFlowAPIError`: If the API request fails

**Example**

```python
agent_session = await client.agents.get_agent_session(
    agent_id="agent_456",
    name="MySession"
)
print(agent_session.id, agent_session.name)
```

### ⚡ Update Agent Session

Update an agent session.

**Parameters**

| Parameter  | Type          | Description               |
|------------|---------------|---------------------------|
| agent_id   | str           | Agent ID (required)       |
| session_id | str           | Session ID (required)     |
| name       | Optional[str] | Optional new session name |
| user_id    | Optional[str] | Optional new user ID      |

**Returns**

- `None`

**Example**

```python
await client.agents.update_session(
    agent_id=agent.id,
    session_id=session.id,
    name="updated-session",
    user_id="user456"
)
```

### ⚡ Delete Agent Sessions

Delete one or more sessions under an agent.

**Parameters**

| Parameter   | Type                 | Description                                                  |
|-------------|----------------------|--------------------------------------------------------------|
| agent_id    | str                  | Agent ID (required)                                          |
| session_ids | Optional[str / list] | Single or list of session IDs. If None, deletes all sessions |

**Returns**

- `None`

**Example**

```python
await client.agents.delete_sessions(agent_id=agent.id, session_ids=[session.id])
# or delete all sessions
await client.agents.delete_sessions(agent_id=agent.id)
```

### ⚡ Ask in Agent Session

Ask a question in a specific agent session and get a completion result.

**Parameters**

| Parameter  | Type | Description                                          |
|------------|------|------------------------------------------------------|
| agent_id   | str  | Agent ID (required)                                  |
| session_id | str  | Session ID (required)                                |
| prompt     | str  | User question (required)                             |
| stream     | bool | Whether to return streaming results (default False)  |
| **kwargs   | dict | Additional options like `temperature`, `top_p`, etc. |

**Returns**

- `AgentCompletionResult` instance if `stream=False`.
- async generator `AgentCompletionResult` if `stream=True`.

**Example**

- Non-streaming

```python
result = await client.agents.ask(agent_id="agent_123", session_id="sess_456", prompt="Hello AI")
print(result.text)
```

- Streaming

```python
async for chunk in client.agents.ask(agent_id="agent_123", session_id="sess_456", prompt="Hello AI", stream=True):
    print(chunk.text)
```

---

## 🧩 File APIs

The File API allows you to manage files and folders, including uploading, creating, listing, renaming, moving, deleting,
converting, and downloading files.

### ⚡ Upload Files

Upload multiple files to a folder.

**Parameters**

| Parameter | Type          | Description                                                       |
|-----------|---------------|-------------------------------------------------------------------|
| files     | list[tuple]   | List of tuples (filename, content_bytes, content_type) (required) |
| parent_id | Optional[str] | Optional ID of the parent folder                                  |

**Returns**

- List of uploaded `File` instances

**Example**

Prepare the files using [Prepare Upload Files](utilities-reference.md#prepare-upload-files) or manually:

```python
uploaded_files = await client.files.upload_files(
    files=[
        ("test1.txt", b"content", "text/plain"),
        ("test2.pdf", b"%PDF-1.4...", "application/pdf")
    ],
    parent_id=root_folder.id
)
for f in uploaded_files:
    print(f.id, f.name)
```

### ⚡ Download File

Download the content of a file.

**Parameters**

| Parameter | Type | Description               |
|-----------|------|---------------------------|
| file_id   | str  | ID of the file (required) |

**Returns**

- `bytes`: Raw file content as bytes. Can be used to save the file locally or process in memory.

**Example**

```python
content_bytes = await client.files.download_file(file_id=file.id)
with open("downloaded_file.txt", "wb") as f:
    f.write(content_bytes)
```

### ⚡ List Files

List files in a folder with optional filtering and pagination.

**Parameters**

| Parameter | Type          | Description                            |
|-----------|---------------|----------------------------------------|
| parent_id | Optional[str] | Parent folder ID                       |
| keywords  | Optional[str] | Search keywords                        |
| page      | int           | Page number (default 1)                |
| page_size | int           | Number of items per page (default 15)  |
| orderby   | str           | Field to sort by (default CREATE_TIME) |
| desc      | bool          | Sort descending if True (default True) |

**Returns**

- List of `File` instances

**Example**

```python
result, total = await client.files.list_files(parent_id=folder.id, keywords="report")
for f in result.files:
    print(f.id, f.name)
```

### ⚡ Delete Files

Delete files by their IDs.

**Parameters**

| Parameter | Type      | Description                           |
|-----------|-----------|---------------------------------------|
| file_ids  | list[str] | List of file IDs to delete (required) |

**Returns**

- `None`

**Example**

```python
await client.files.delete_files(file_ids=[file.id])
```

### ⚡ Create File or Folder

Create a new folder or virtual file.

**Parameters**

| Parameter | Type          | Description                           |
|-----------|---------------|---------------------------------------|
| name      | str           | Name of the file or folder (required) |
| type_     | str           | Type: "FOLDER" or "FILE" (required)   |
| parent_id | Optional[str] | Optional parent folder ID             |

**Returns**

- `File` or `Folder` instance

**Example**

```python
from ragflow_async_sdk.types import FileType

folder = await client.files.create_file_or_folder(name="New Folder", type_=FileType.FOLDER)
file = await client.files.create_file_or_folder(name="readme.txt", type_=FileType.FILE, parent_id=folder.id)
```

### ⚡ Get Root Folder

Get the root folder of the file system.

**Parameters**

- `None`

**Returns**

- `Folder` instance

**Example**

```python
root_folder = await client.files.get_root_folder()
print(root_folder.id, root_folder.name)
```

### ⚡ Get Parent Folder

Get the parent folder of a file.

**Parameters**

| Parameter | Type | Description               |
|-----------|------|---------------------------|
| file_id   | str  | ID of the file (required) |

**Returns**

- `Folder` instance

**Example**

```python
parent = await client.files.get_parent_folder(file_id=file.id)
print(parent.id, parent.name)
```

### ⚡ Get All Parent Folders

Get all parent folders up to the root for a file.

**Parameters**

| Parameter | Type | Description               |
|-----------|------|---------------------------|
| file_id   | str  | ID of the file (required) |

**Returns**

- List of `Folder` instances

**Example**

```python
parents = await client.files.get_all_parent_folders(file_id=file.id)
for p in parents:
    print(p.id, p.name)
```

### ⚡ Rename File

Rename a file.

**Parameters**

| Parameter | Type | Description               |
|-----------|------|---------------------------|
| file_id   | str  | ID of the file (required) |
| name      | str  | New name (required)       |

**Returns**

- `None`

**Example**

```python
await client.files.rename_file(file_id=file.id, name="new_name.txt")
```

### ⚡ Move Files

Move files to a new folder.

**Parameters**

| Parameter    | Type      | Description                      |
|--------------|-----------|----------------------------------|
| src_file_ids | list[str] | Source file IDs (required)       |
| dest_file_id | str       | Destination folder ID (required) |

**Returns**

- `None`

**Example**

```python
await client.files.move_files(src_file_ids=[file.id], dest_file_id=folder.id)
```

### ⚡ Convert Files

Convert files into knowledge base entries.

**Parameters**

| Parameter | Type      | Description                          |
|-----------|-----------|--------------------------------------|
| file_ids  | list[str] | File IDs to convert (required)       |
| kb_ids    | list[str] | Target knowledge base IDs (required) |

**Returns**

- `ConversionResult` instance

**Example**

```python
conversion_results = await client.files.convert_files(file_ids=[file.id], kb_ids=[kb.id])
print(conversion_results)
```

---

## 🧩 System APIs

The System API provides system-related endpoints, including health checks.

### ⚡ Health Check

Check the health status of the system.

**Parameters**

- `None`

**Returns**

- `SystemHealth` instance

**Example**

```python
# Perform a health check
system_health = await client.system.healthz()
print(system_health.status, system_health.details)
```

