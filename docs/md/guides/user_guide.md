# 📝 User Guide

This guide provides step-by-step tutorials and detailed examples for using the **RAGFlow Async SDK**.
It is intended for Python developers who want to integrate with RAGFlow asynchronously.

---

## ⚡ Setup & Initialization

### 💿 Installation

Requires **Python 3.10+**.

```bash
pip install ragflow-async-sdk
```

Optional (for async local file uploads):

```bash
pip install aiofiles
```

### 🛠 Initialize Client

```python
from ragflow_async_sdk import AsyncRAGFlowClient

client = AsyncRAGFlowClient(
    server_url="http://your-ragflow-address",
    api_key="YOUR_API_KEY"
)
```

### ⏩ Run Async Calls

```python
import asyncio

async def main():
    # Perform a simple health check
    system_health = await client.systems.healthz()
    print(system_health.status, system_health.details)

asyncio.run(main())
```

> You can also use the SDK in async frameworks like FastAPI or any asyncio-based environment. See: [FastAPI Usage Examples](fastapi_usage_examples.md)

---

## 🧩 Core Concepts

| Concept      | Description                               |
| ------------ | ----------------------------------------- |
| Dataset      | Container for documents                   |
| Document     | Individual file with metadata             |
| Chunk        | Segment of document content for retrieval |
| Chat / Agent | Assistants for QA or workflow             |
| Session      | Conversation context for Chat/Agent       |

---

## 🚀 Usage Examples

### Datasets

```python
dataset = await client.datasets.create_dataset(name="my_dataset")
datasets, total = await client.datasets.list_datasets()
dataset = await client.datasets.get_dataset(dataset.id)
await client.datasets.update_dataset(dataset.id, name="new_name")
await client.datasets.delete_dataset(dataset.id)
```

### Documents

```python
from ragflow_async_sdk.utils.files import file_from_path

files_to_send = [await file_from_path("test.txt"), await file_from_path("test.pdf")]
uploaded_docs, total = await client.documents.upload_documents(dataset.id, files=files_to_send)

import aiofiles, os
file_path = "./downloads/test.pdf"
os.makedirs(os.path.dirname(file_path), exist_ok=True)
content = await client.files.download_file(dataset.id, uploaded_docs[1].id)
async with aiofiles.open(file_path, "wb") as f:
    await f.write(content)

await client.documents.parse_document(document_id)
await client.documents.stop_parsing(document_id)
```

### Chunks

```python
chunks, total = await client.chunks.list_chunks(dataset_id=dataset.id)
```

### Chat Assistants

```python
chat = await client.chats.create(name="demo-chat")
session = await client.chats.create_session(chat.id)
result = await client.chats.ask(chat.id, session.id, "Hello")
async for chunk in await client.chats.ask(chat.id, session.id, "Hello", stream=True):
    print(chunk.answer, end="")
```

### Agents

```python
agent = await client.agents.create(title="Demo Agent")
agents, total = await client.agents.list_agents()
agent = await client.agents.get_agent(agent.id)
await client.agents.update_agent(agent.id, title="Updated")
await client.agents.delete_agent(agent.id)

session = await client.agents.create_session(agent.id)
result = await client.agents.ask(agent.id, session.id, "Hello")
async for chunk in await client.agents.ask(agent.id, session.id, "Hello", stream=True):
    print(chunk.answer, end="")
```

### File & Folder Management

```python
files_to_upload = [await file_from_path("example.txt")]
uploaded_files = await client.files.upload_files(files=files_to_upload, parent_id=root_folder.id)
content = await client.files.download_file(root_folder.id, uploaded_files[0].id)

folder = await client.files.create_file_or_folder(name="New Folder", parent_id=root_folder.id, is_folder=True)
parent = await client.files.get_parent_folder(file_id)
await client.files.rename_file(file_id, "new_name.txt")
await client.files.remove_files([file_id], destination_folder_id=other_folder.id)
```

---

## 🛠 Utilities

* Validators: `require_params`, `validate_enum`
* Normalizers: `normalize_ids`
* File helpers: `file_from_path`, `file_from_bytes`, `file_from_url`

> See the API Reference for full usage of validators and file helpers.

---

## ⚠️ Error Handling

```python
from ragflow_async_sdk.exceptions import (
    RAGFlowAPIError,
    RAGFlowValidationError,
    RAGFlowTimeoutError
)

try:
    await client.datasets.list_datasets()
except RAGFlowValidationError as e:
    print("Validation error:", e.message)
except RAGFlowAPIError as e:
    print("API error:", e.message)
except RAGFlowTimeoutError:
    print("Request timed out")
```

---

## 💡 Tips & Tricks

* Handling large files efficiently (use streaming or chunked uploads)
* Streaming large chat sessions with `stream=True`
* Retry and rate-limit handling using `asyncio.sleep` + `try/except`
* Use normalizers & validators consistently for parameter safety

---

## 🎯 Design Principles

The RAGFlow SDK is designed with the following principles:

* **Async-first:** All API calls are awaitable; supports streaming via async generators.
* **Separation of concerns:** Models, APIs, and utility functions are clearly separated.
* **Typed and predictable:** Return values are typed, ensuring IDE support and fewer runtime errors.
* **No httpx leakage:** Internal HTTP client is encapsulated.
* **Extensible:** Easily extendable for new APIs, entities, or utilities.
* **Error-safe by design:** Operations are considered successful if no errors are raised.

---

## 🔗 References

* [API Reference](../references/api_reference.md)
* [Error Reference](../references/error_reference.md)
* [Entities Reference](../references/entities_reference.md)
