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
  - [Exception Handling](#exception-handling)
  - [Using Entities](#using-entities)

- [Dataset API](#dataset-apis)
  - [1. Create Dataset](#1-create-dataset)
  - [2. List Datasets](#2-list-datasets)
  - [3. Get Dataset](#3-get-dataset)
  - [4. Update Dataset](#4-update-dataset)
  - [5. Delete Dataset](#5-delete-datasets)

- [Document API](#document-apis)
  - [Upload Documents](#1-upload-documents)
  - [List Documents](#2-list-documents)
  - [Get Document](#3-get-document)
  - [Update Document](#4-update-document)
  - [Delete Documents](#5-delete-documents)
  - [Download Document](#6-download-document)
  - [Parse Documents](#7-parse-documents)
  - [Stop Parsing Document](#8-stop-parsing-document)

- [Chunk API](#chunk-apis)
  - [Add Chunk](#1-add-chunk)
  - [List Chunks](#2-list-chunks)
  - [Get Chunk](#3-get-chunk)
  - [Update Chunk](#4-update-chunk)
  - [Delete Chunks](#5-delete-chunks)

- [Chat API](#chat-apis)
  - [Create Chat Assistant](#1-create-chat)
  - [List Chat Assistants](#2-list-chats)
  - [Get Chat Assistant](#3-get-chat)
  - [Update Chat Assistant](#4-update-chat)
  - [Delete Chat Assistants](#5-delete-chats)
  - [Create Chat Session](#6-create-chat-session)
  - [List Chat Session](#7-list-chat-sessions)
  - [Get Chat Session](#8-get-chat-session)
  - [Update Chat Session](#9-update-chat-session)
  - [Delete Chat Session](#10-delete-chat-sessions)
  - [Ask in Chat Session](#11-ask-in-chat-session)

- [Agent API](#agent-apis)
  - [Create Agent](#1-create-agent)
  - [List Agents](#2-list-agents)
  - [Get Agent](#3-get-agent)
  - [Update Agent](#4-update-agent)
  - [Delete Agent](#5-delete-agent)
  - [Create Agent Session](#6-create-agent-session)
  - [List Agent Sessions](#7-list-agent-sessions)
  - [Get Agent Session](#8-get-agent-session)
  - [Update Agent Session](#9-update-agent-session)
  - [Delete Agent Sessions](#10-delete-agent-sessions)
  - [Ask in Agent Session](#11-ask-in-agent-session)

- [File API](#file-apis)
  - [Upload Files](#1-upload-files)
  - [Download File](#2-download-file)
  - [List Files](#3-list-files)
  - [Delete Files](#4-delete-files)
  - [Create File or Folder](#5-create-file-or-folder)
  - [Get Root Folder](#6-get-root-folder)
  - [Get Parent Folder](#7-get-parent-folder)
  - [Get All Parent Folders](#8-get-all-parent-folders)
  - [Rename File](#9-rename-file)
  - [Remove Files](#10-move-files)
  - [Convert Files](#11-convert-files)

- [System API](#system-apis)
  - [Health Check](#1-health-check)


- Models & Entities
  - Dataset
  - Document
  - Chunk
  - File & Folder
  - ChatCompletionResult
  - AgentCompletionResult
  - Session Models


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

---

## Dataset APIs

### 1. Create Dataset

Returns a `Dataset` instance. Raises exception on failure.

```python
from ragflow_async_sdk.exceptions import RAGFlowAPIError

try:
    dataset = await client.datasets.create_dataset(name="my_dataset")
except RAGFlowAPIError as e:
    print("Failed to create dataset:", e)
```

### 2. List Datasets

```python
datasets, total = await client.datasets.list_datasets(page=1, page_size=30)

# Filtering by name
datasets, total = await client.datasets.list_datasets(name="my_dataset")
```

### 3. Get Dataset
Exactly one of dataset_id or name must be provided.

```python
dataset = await client.datasets.get_dataset(dataset_id="real-dataset-id")
assert dataset.id == "real-dataset-id"

dataset = await client.datasets.get_dataset(name="my_dataset")
assert dataset.name == "my_dataset"
```

### 4. Update Dataset

Returns None. Raises exception on failure.

```python
await client.datasets.update_dataset(dataset.id, name="new_name")
```

### 5. Delete Datasets

Returns None. Can delete a single, multiple, or all datasets.

```python
# Delete one
await client.datasets.delete_datasets(ids=[dataset.id])

# Delete multiple
await client.datasets.delete_datasets(ids=["id1", "id2"])

# Delete all
await client.datasets.delete_datasets(ids=None)
```

---

## Document APIs

### 1. Upload Documents

Returns a list of uploaded Documents and total count.

| Parameter     | Type                         | Description                                                |
| ------------- | ---------------------------- | ---------------------------------------------------------- |
| dataset_id    | str                          | Target dataset ID                                          |
| files         | List[Tuple[str, bytes, str]] | Each document as `(filename, content_bytes, content_type)` |
| parser_config | dict                         | Optional parser configuration                              |
| chunk_method  | ChunkMethod                  | Optional chunking method                                   |

Prepare the files using [Prepare Upload Files](#prepare-upload-files) or manually:

```python
from ragflow_async_sdk.types.ingestion import ChunkMethod

files = [
    ("hello.txt", b"hello world", "text/plain"),
]

uploaded_docs, total = await client.documents.upload_documents(
    dataset_id=dataset.id,
    files=files_to_send,
    chunk_method=ChunkMethod.NAIVE
)

print(f"Uploaded {total} documents")

```
> ⚠️ `file_from_path` requires `aiofiles`:
> > pip install aiofiles

### 2. List Documents

Returns a list of Documents and total count.

| Parameter  | Type    | Description                 |
| ---------- | ------- | --------------------------- |
| dataset_id | str     | Target dataset ID           |
| page       | int     | Page number (default 1)     |
| page_size  | int     | Items per page (default 30) |
| keywords   | str     | Optional search keywords    |
| orderby    | OrderBy | Optional sorting field      |
| desc       | bool    | Optional, descending order  |

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

### 3. Get Document

Get a single document by ID or name within a dataset.

#### Parameters

| Parameter   | Type          | Description           |
| ----------- | ------------- | --------------------- |
| dataset_id  | str           | Dataset ID (required) |
| document_id | Optional[str] | Document ID           |
| name        | Optional[str] | Document name         |

#### Returns
- `Document` instance if found
- `None` if no document matches

#### Raises
- `RAGFlowValidationError`: If parameters are invalid
- `RAGFlowConflictError`: If multiple documents match the query

#### Example
```python
document = await client.datasets.get_document(
    dataset_id=dataset.id,
    name="user_manual.pdf"
)

if document:
    print(document.id, document.name)
```

### 4. Update Document

Returns None, raises exception on failure.

| Parameter     | Type        | Description                   |
| ------------- | ----------- | ----------------------------- |
| dataset_id    | str         | Target dataset ID             |
| document_id   | str         | Document ID                   |
| name          | str         | New name                      |
| parser_config | dict        | Optional parser configuration |
| chunk_method  | ChunkMethod | Optional chunking method      |

```python
await client.documents.update_document(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    name="manual_updated.txt",
    parser_config={"chunk_token_num": 128}
)
```

### 5. Delete Documents


### 6. Download Document

Returns bytes of the file content.

| Parameter   | Type | Description       |
| ----------- | ---- | ----------------- |
| dataset_id  | str  | Target dataset ID |
| document_id | str  | Document ID       |

```python
import aiofiles

content = await client.documents.download_document(
    dataset_id=dataset.id,
    document_id=documents[0].id
)

async with aiofiles.open("downloaded_manual.txt", "wb") as f:
    await f.write(content)

```

### 7. Parse Documents

Trigger document parsing (chunking / ingestion).

| Parameter    | Type      | Description           |
| ------------ | --------- | --------------------- |
| dataset_id   | str       | Target dataset ID     |
| document_ids | List[str] | Document IDs to parse |

```python
# Parse all documents
await client.documents.parse_documents(dataset.id, [doc.id for doc in documents])

# Parse only failed documents
failed_ids = [d.id for d in documents if d.run == "FAIL"]
await client.documents.parse_documents(dataset.id, failed_ids)
```

### 8. Stop Parsing Document

Stop parsing a document.

| Parameter   | Type | Description       |
| ----------- | ---- | ----------------- |
| dataset_id  | str  | Target dataset ID |
| document_id | str  | Document ID       |

```python
await client.documents.stop_parsing_documents(dataset.id, documents[0].id)
```

---

## Chunk APIs

The Chunk API allows you to manage document chunks, including adding, 
listing, updating, deleting, retrieving, and handling document-level metadata.

> Note:
> Chunk-related APIs are divided into two categories:
> - **Browsing APIs** (`list_chunks`, `get_chunk`) for structured access
> - **Retrieval APIs** (`retrieve_chunks`) for semantic search
>
> Retrieval results are not guaranteed to be stable or unique entities.

### 1. Add Chunk

Add a new chunk to a document.

| Parameter          | Type                | Description                            |
| ------------------ | ------------------- | -------------------------------------- |
| dataset_id         | str                 | Dataset containing the document        |
| document_id        | str                 | Target document ID                     |
| content            | str                 | Text content of the chunk              |
| important_keywords | Optional[list[str]] | Keywords highlighting chunk importance |
| questions          | Optional[list[str]] | Questions associated with the chunk    |

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

### 2. List Chunks

List chunks in a document with optional filters.

| Parameter   | Type        | Description                             |
| ----------- | ----------- | --------------------------------------- |
| dataset_id  | str         | Dataset containing the document         |
| document_id | str         | Target document ID                      |
| keywords    | Optional[str] | Optional search keywords               |
| page        | int         | Page number                             |
| page_size   | int         | Number of chunks per page               |
| chunk_id    | Optional[str] | Optional specific chunk ID filter      |

```python
chunks, total = await client.chunks.list_chunks(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    page=1,
    page_size=20
)
print(chunks, total)
```

### 3. Get Chunk
Get a single chunk by ID within a document.
> This API is intended for structured access to chunks.
For semantic search, use retrieve_chunks instead.

#### Parameters
| Parameter   | Type | Description            |
| ----------- | ---- | ---------------------- |
| dataset_id  | str  | Dataset ID (required)  |
| document_id | str  | Document ID (required) |
| chunk_id    | str  | Chunk ID (required)    |

#### Returns
- `Chunk` instance if found
- `None` if the chunk does not exist

#### Raises
- `RAGFlowValidationError`: If required parameters are missing
- `RAGFlowConflictError`: If multiple chunks match the ID (unexpected)

#### Example
```python
chunk = await client.datasets.get_chunk(
    dataset_id=dataset.id,
    document_id=document.id,
    chunk_id="chunk_456"
)

if chunk:
    print(chunk.id, chunk.content)
```

### 4. Update Chunk

Update content or settings for a specific chunk.

| Parameter          | Type                | Description                           |
| ------------------ | ------------------- | ------------------------------------- |
| dataset_id         | str                 | Dataset containing the document       |
| document_id        | str                 | Document ID                            |
| chunk_id           | str                 | Chunk ID to update                     |
| content            | Optional[str]       | New content for the chunk             |
| important_keywords | Optional[list[str]] | Updated list of important keywords    |
| available          | Optional[bool]      | Whether the chunk is available        |

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

### 5. Delete Chunks

Delete chunks by ID or delete all if none provided.

| Parameter   | Type                  | Description                          |
| ----------- | -------------------   | ------------------------------------ |
| dataset_id  | str                   | Dataset containing the document      |
| document_id | str                   | Document ID                           |
| chunk_ids   | Optional[str|list[str]] | List of chunk IDs to delete or None to delete all |

```python
await client.chunks.delete_chunks(
    dataset_id=dataset.id,
    document_id=documents[0].id,
    chunk_ids=[chunk.id]
)
```

### 6. Get Metadata Summary

Retrieve a metadata summary for all documents in a dataset.

| Parameter   | Type | Description          |
| ----------- | ---- | ------------------- |
| dataset_id  | str  | Dataset ID           |

```python
summary = await client.chunks.get_metadata_summary(dataset.id)
print(summary)
```

### 7. Update Metadata

Batch update or delete document-level metadata.

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| dataset_id | str | Dataset ID |
| selector  | Optional[dict] | Filter documents, e.g., {"document_ids": [...]} |
| updates   | Optional[list[dict]] | Metadata updates [{"key": str, "match": str, "value": str}] |
| deletes   | Optional[list[dict]] | Metadata deletions [{"key": str, "value": Optional[str]}] |

```python
result = await client.chunks.update_metadata(
    dataset_id=dataset.id,
    updates=[{"key": "topic", "match": "old", "value": "new"}],
    deletes=[{"key": "obsolete"}]
)
print(result)
```

### 8. Retrieve Chunks

Retrieve chunks from datasets or documents based on a query. Supports filtering, reranking, keyword search, and knowledge-graph enhanced search.

| Parameter                   | Type                      | Description |
| --------------------------- | ------------------------- | ----------- |
| question                    | str                        | Query string or keywords (required) |
| dataset_ids                  | Optional[str \| list[str]] | Dataset IDs to search |
| document_ids                 | Optional[str \| list[str]] | Document IDs to search |
| page                         | int                        | Page number (default: 1) |
| page_size                    | int                        | Number of chunks per page (default: 30) |
| similarity_threshold         | float                      | Minimum similarity score (default: 0.2) |
| vector_similarity_weight     | float                      | Weight of vector similarity (default: 0.3) |
| top_k                        | int                        | Number of chunks considered for vector computation (default: 1024) |
| rerank_id                    | Optional[str]              | Optional rerank model ID |
| keyword                      | bool                       | Enable keyword-based matching (default: False) |
| highlight                    | bool                       | Highlight matched terms (default: False) |
| cross_languages              | Optional[list[str]]        | Target languages for translation |
| metadata_condition           | Optional[dict]             | Metadata filter conditions |
| use_kg                       | bool                       | Enable knowledge graph multi-hop search (default: False) |
| toc_enhance                  | bool                       | Enable table-of-contents enhanced search (default: False) |

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

# Access returned chunks and metadata
chunks = retrieved.get("chunks", [])
total = retrieved.get("total", 0)
aggregations = retrieved.get("document_aggregations", {})

print(f"Total chunks found: {total}")
for chunk in chunks:
    print(chunk["content"])
```

---

## Chat APIs

The Chat API allows you to manage chat assistants and their sessions, including creating, listing, updating, deleting, and sending messages with optional streaming.


### 1. Create Chat

Create a new chat assistant.

| Parameter    | Type                 | Description |
| ------------ | ------------------ | ----------- |
| name         | str                 | Chat assistant name (required) |
| dataset_ids  | Optional[list[str]] | Optional list of associated dataset IDs |
| avatar       | Optional[str]       | Optional avatar URL |
| llm          | Optional[dict]      | Optional LLM configuration |
| prompt       | Optional[dict]      | Optional prompt configuration |

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

### 2. List Chats

List chat assistants with optional filters.

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| page      | int  | Page number (default 1) |
| page_size | int  | Number of items per page (default 30) |
| orderby   | str  | Field to sort by (default CREATE_TIME) |
| desc      | bool | Sort descending if True (default True) |
| chat_id   | Optional[str] | Filter by chat ID |
| name      | Optional[str] | Filter by chat name |

```python
chats, total = await client.chats.list_chats(page=1, page_size=50)
for c in chats:
    print(c.id, c.name)
```

### 3. Get Chat
Get a single chat assistant by ID or name.

#### Parameters
Exactly one of `chat_id` or `name` must be provided.

| Parameter | Type          | Description         |
| --------- | ------------- | ------------------- |
| chat_id   | Optional[str] | Chat assistant ID   |
| name      | Optional[str] | Chat assistant name |

#### Returns
- `ChatAssistant` instance if found
- `None` if no chat matches

#### Raises
- `RAGFlowValidationError`: If parameters are invalid
- `RAGFlowConflictError`: If multiple chats match the query

#### Example
```python
chat = await client.chats.get_chat(name="support-bot")

if chat:
    print(chat.id, chat.name)
```

### 4. Update Chat

Update an existing chat assistant.

| Parameter    | Type                 | Description |
| ------------ | ------------------ | ----------- |
| chat_id      | str                 | Chat assistant ID (required) |
| name         | Optional[str]       | New chat name |
| dataset_ids  | Optional[list[str]] | Updated dataset IDs |
| avatar       | Optional[str]       | Updated avatar URL |
| llm          | Optional[dict]      | Updated LLM configuration |
| prompt       | Optional[dict]      | Updated prompt configuration |

```python
await client.chats.update_chat(
    chat_id=chat.id,
    name="updated-chat",
    avatar="http://example.com/new_avatar.png"
)
```

### 5. Delete Chats

Delete one or more chat assistants.

| Parameter | Type                | Description |
| --------- | ----------------- | ----------- |
| ids       | Optional[str|list] | Single or list of chat IDs. If None, deletes all chats. |

```python
await client.chats.delete_chats(ids=[chat.id])
```

### 6. Create Chat Session

Create a new session under a chat assistant.

| Parameter | Type          | Description               |
| ---------- | ------------ | ------------------------- |
| chat_id    | str           | Chat assistant ID         |
| name       | Optional[str] | Optional session name      |
| user_id    | Optional[str] | Optional user ID           |

```python
session = await client.chats.create_session(
    chat_id=chat.id,
    name="demo-session",
    user_id="user123"
)
print(session.id, session.name)
```

### 7. List Chat Sessions

List sessions for a specific chat assistant.

> Internally, this API uses the SessionMixin.list_sessions method, passing chat_id as the parent_id.

#### Parameters
| Parameter  | Type          | Description                              |
| ---------- | ------------- | ---------------------------------------- |
| chat_id    | str           | Chat assistant ID (required)             |
| page       | int           | Page number (default 1)                  |
| page_size  | int           | Number of items per page (default 30)    |
| orderby    | str           | Field to sort by (default `create_time`) |
| desc       | bool          | Sort descending if True (default True)   |
| name       | Optional[str] | Optional filter by session name          |
| session_id | Optional[str] | Optional filter by session ID            |
| user_id    | Optional[str] | Optional filter by user ID               |

#### Returns
- Tuple of `(list of ChatSession instances, total count)`

```python
sessions, total = await client.chats.list_sessions(chat_id="chat_123")
for s in sessions:
    print(s.id, s.name)
```

### 8. Get Chat Session
List all sessions for a specific chat assistant, with optional filtering and pagination.

#### Parameters
| Parameter  | Type          | Description                            |
| ---------- | ------------- | -------------------------------------- |
| chat_id    | str           | Chat assistant ID (required)           |
| page       | int           | Page number (default 1)                |
| page_size  | int           | Number of items per page (default 30)  |
| orderby    | OrderBy | str | Field to sort by (default CREATE_TIME) |
| desc       | bool          | Sort descending if True (default True) |
| name       | Optional[str] | Optional filter by session name        |
| session_id | Optional[str] | Optional filter by session ID          |
| user_id    | Optional[str] | Optional filter by user ID             |

#### Returns
- Tuple of (list of ChatSession instances, total count)

#### Raises
- RAGFlowValidationError: If parameters are invalid
- RAGFlowConflictError: If multiple chats match the query

#### Example
sessions, total = await client.chats.list_sessions(chat_id="chat_123")
for s in sessions:
    print(s.id, s.name, s.user_id)

### 9. Update Chat Session

Update a session under a chat assistant.

| Parameter  | Type          | Description           |
| ---------- | ------------ | -------------------- |
| chat_id    | str           | Chat assistant ID     |
| session_id | str           | Session ID            |
| name       | Optional[str] | Optional new name     |
| user_id    | Optional[str] | Optional new user ID  |

```python
await client.chats.update_session(
    chat_id=chat.id,
    session_id=session.id,
    name="updated-session"
)
```

### 10. Delete Chat Sessions

Delete one or more chat sessions.

| Parameter   | Type                 | Description                                   |
| ----------- | ------------------- | --------------------------------------------- |
| chat_id     | str                  | Chat assistant ID                             |
| session_ids | Optional[str/list]   | Single or list of session IDs; if None, delete all |

```python
await client.chats.delete_sessions(chat_id=chat.id, session_ids=[session.id])
```

### 11. Ask in Chat Session

Send a prompt to a chat session, optionally streaming the response.

| Parameter  | Type                         | Description                                   |
| ---------- | --------------------------- | --------------------------------------------- |
| chat_id    | str                           | Chat assistant ID                             |
| session_id | str                           | Session ID                                    |
| prompt     | str                           | User question                                |
| stream     | bool                          | Whether to return streaming results          |
| **kwargs   | Additional parameters         | Extra parameters (temperature, top_p, etc.)  |

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

## Agent APIs

The Agent API allows you to manage agents and their sessions, including creating, listing, updating, deleting, and managing sessions.

### 1. Create Agent

Create a new agent.

| Parameter     | Type          | Description |
| ------------- | ------------- | ----------- |
| title         | str           | Agent title (required) |
| dsl           | dict          | Agent DSL configuration, including graph, components, retrieval, etc. (required) |
| description   | Optional[str] | Optional description of the agent |

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

### 2. List Agents

List agents with optional filters.

| Parameter   | Type                 | Description |
| ----------- | ------------------ | ----------- |
| page        | int                  | Page number (default 1) |
| page_size   | int                  | Number of items per page (default 30) |
| orderby     | str                  | Field to sort by (default CREATE_TIME) |
| desc        | bool                 | Sort descending if True (default True) |
| agent_id    | Optional[str]        | Filter by agent ID |
| title       | Optional[str]        | Filter by agent title |

```python
agents, total = await client.agents.list_agents(page=1, page_size=50)
for a in agents:
    print(a.id, a.title)
```

### 3. Get Agent

Retrieve a single agent by ID or title. Only one of `agent_id` or `title` should be provided.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| agent_id    | Optional[str] | Agent ID |
| title       | Optional[str] | Agent title |

```python
agent = await client.agents.get_agent(agent_id="agent123")
# or
agent = await client.agents.get_agent(title="demo-agent")
```

### 4. Update Agent
Update an existing agent by its ID. Only specify the fields you want to change.

#### Parameters
| Parameter    | Type           | Description                                     |
| ------------ | -------------- | ----------------------------------------------- |
| agent_id     | str            | Agent ID (required)                             |
| title        | Optional[str]  | New title of the agent                           |
| description  | Optional[str]  | New description of the agent                     |
| dsl          | Optional[dict] | Canvas DSL object of the agent                  |

#### Returns
- `None` on success.

#### Raises
- `RAGFlowValidationError`: If no fields are provided to update.
- `RAGFlowAPIError`: If the update fails due to API or permission errors.

#### Example
```python
await client.agents.update_agent(
    agent_id="58af890a2a8911f0a71a11b922ed82d6",
    title="Test Agent",
    description="A test agent",
    dsl={"nodes": [], "edges": []},
)
```

### 5. Delete Agent

Delete an agent by ID.

| Parameter | Type   | Description |
| --------- | ------ | ----------- |
| agent_id  | str    | Agent ID (required) |

```python
success = await client.agents.delete_agent(agent_id=agent.id)
print(success)
```

### 6. Create Agent Session

Create a new session under an agent.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| agent_id    | str           | Agent ID (required) |
| name        | str           | Optional session name (default "New session") |
| user_id     | Optional[str] | Optional user ID |

```python
session = await client.agents.create_session(
    agent_id=agent.id,
    name="demo-session",
    user_id="user123"
)
print(session.id, session.name)
```

### 7. List Agent Sessions

List sessions for an agent.

| Parameter   | Type                 | Description |
| ----------- | ------------------ | ----------- |
| agent_id    | str                  | Agent ID (required) |
| page        | int                  | Page number (default 1) |
| page_size   | int                  | Number of items per page (default 30) |
| orderby     | str                  | Field to sort by (default CREATE_TIME) |
| desc        | bool                 | Sort descending if True (default True) |
| name        | Optional[str]        | Filter by session name |
| session_id  | Optional[str]        | Filter by session ID |
| user_id     | Optional[str]        | Filter by user ID |

```python
sessions, total = await client.agents.list_sessions(agent_id=agent.id)
for s in sessions:
    print(s.id, s.name)
```

### 8. Get Agent Session
Get a single session for a specific agent by session_id or name.

#### Parameters
| Parameter  | Type          | Description                                                    |
| ---------- | ------------- | -------------------------------------------------------------- |
| agent_id   | str           | Agent ID (required)                                            |
| session_id | Optional[str] | Session ID to fetch (exactly one required with `name`)         |
| name       | Optional[str] | Session name to fetch (exactly one required with `session_id`) |

#### Returns
- AgentSession instance if found, otherwise None

#### Raises
- `RAGFlowValidationError`: If both or neither parameter is provided
- `RAGFlowConflictError`: If multiple sessions match the query
- `RAGFlowAPIError`: If the API request fails

#### Example
```python
agent_session = await client.agents.get_agent_session(
    agent_id="agent_456",
    name="MySession"
)
print(agent_session.id, agent_session.name)
```

### 9. Update Agent Session

Update an agent session.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| agent_id    | str           | Agent ID (required) |
| session_id  | str           | Session ID (required) |
| name        | Optional[str] | Optional new session name |
| user_id     | Optional[str] | Optional new user ID |

```python
await client.agents.update_session(
    agent_id=agent.id,
    session_id=session.id,
    name="updated-session",
    user_id="user456"
)
```

### 10. Delete Agent Sessions

Delete one or more sessions under an agent.

| Parameter     | Type                | Description |
| ------------- | ----------------- | ----------- |
| agent_id      | str                 | Agent ID (required) |
| session_ids   | Optional[str|list] | Single or list of session IDs. If None, deletes all sessions |

```python
await client.agents.delete_sessions(agent_id=agent.id, session_ids=[session.id])
# or delete all sessions
await client.agents.delete_sessions(agent_id=agent.id)
```

### 11. Ask in Agent Session
Ask a question in a specific agent session and get a completion result.

#### Parameters
| Parameter   | Type          | Description                                                |
| ----------- | ------------- | ---------------------------------------------------------- |
| agent_id    | str           | Agent ID (required)                                        |
| session_id  | str           | Session ID (required)                                      |
| prompt      | str           | User question (required)                                   |
| stream      | bool          | Whether to return streaming results (default False)       |
| **kwargs    | dict          | Additional options like `temperature`, `top_p`, etc.      |

#### Returns
- If `stream=False`: an `AgentCompletionResult` object.
- If `stream=True`: an async generator yielding `AgentCompletionResult` objects.

#### Raises
- `RAGFlowValidationError`: If required parameters are missing.
- `RAGFlowAPIError`: If the API request fails.

#### Example
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

## File APIs

The File API allows you to manage files and folders, including uploading, creating, listing, renaming, moving, deleting, converting, and downloading files.

### 1. Upload Files

Upload multiple files to a folder.

| Parameter   | Type             | Description |
| ----------- | ---------------- | ----------- |
| files       | list[tuple]      | List of tuples (filename, content_bytes, content_type) (required) |
| parent_id   | Optional[str]    | Optional ID of the parent folder |

Prepare the files using [Prepare Upload Files](#prepare-upload-files) or manually:

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

### 2. Download File

Download the content of a file.

| Parameter   | Type  | Description |
| ----------- | ----- | ----------- |
| file_id     | str   | ID of the file (required) |

```python
content_bytes = await client.files.download_file(file_id=file.id)
with open("downloaded_file.txt", "wb") as f:
    f.write(content_bytes)
```

### 3. List Files

List files in a folder with optional filtering and pagination.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| parent_id   | Optional[str] | Parent folder ID |
| keywords    | Optional[str] | Search keywords |
| page        | int           | Page number (default 1) |
| page_size   | int           | Number of items per page (default 15) |
| orderby     | str           | Field to sort by (default CREATE_TIME) |
| desc        | bool          | Sort descending if True (default True) |

```python
result, total = await client.files.list_files(parent_id=folder.id, keywords="report")
for f in result.files:
    print(f.id, f.name)
```

### 4. Delete Files

Delete files by their IDs.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| file_ids    | list[str]     | List of file IDs to delete (required) |

```python
success = await client.files.delete_files(file_ids=[file.id])
print(success)
```

### 5. Create File or Folder

Create a new folder or virtual file.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| name        | str           | Name of the file or folder (required) |
| type_       | str           | Type: "FOLDER" or "FILE" (required) |
| parent_id   | Optional[str] | Optional parent folder ID |

```python
folder = await client.files.create_file_or_folder(name="New Folder", type_="FOLDER")
file = await client.files.create_file_or_folder(name="readme.txt", type_="FILE", parent_id=folder.id)
```

### 6. Get Root Folder

Get the root folder of the file system.

```python
root_folder = await client.files.get_root_folder()
print(root_folder.id, root_folder.name)
```

### 7. Get Parent Folder

Get the parent folder of a file.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| file_id     | str           | ID of the file (required) |

```python
parent = await client.files.get_parent_folder(file_id=file.id)
print(parent.id, parent.name)
```

### 8. Get All Parent Folders

Get all parent folders up to the root for a file.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| file_id     | str           | ID of the file (required) |

```python
parents = await client.files.get_all_parent_folders(file_id=file.id)
for p in parents:
    print(p.id, p.name)
```

### 9. Rename File

Rename a file.

| Parameter   | Type      | Description |
| ----------- | -------- | ----------- |
| file_id     | str       | ID of the file (required) |
| name        | str       | New name (required) |

```python
success = await client.files.rename_file(file_id=file.id, name="new_name.txt")
print(success)
```

### 10. Move Files

Move files to a new folder.

| Parameter       | Type         | Description |
| --------------- | ------------ | ----------- |
| src_file_ids    | list[str]    | Source file IDs (required) |
| dest_file_id    | str          | Destination folder ID (required) |

```python
success = await client.files.move_files(src_file_ids=[file.id], dest_file_id=folder.id)
print(success)
```

### 11. Convert Files

Convert files into knowledge base entries.

| Parameter   | Type          | Description |
| ----------- | ------------- | ----------- |
| file_ids    | list[str]     | File IDs to convert (required) |
| kb_ids      | list[str]     | Target knowledge base IDs (required) |

```python
conversion_results = await client.files.convert_files(file_ids=[file.id], kb_ids=[kb.id])
print(conversion_results)
```

---

## System APIs

The System API provides system-related endpoints, including health checks.

### 1. Health Check

Check the health status of the system.

```python
# Perform a health check
system_health = await client.system.healthz()
print(system_health.status, system_health.details)
```

