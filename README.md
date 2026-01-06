# RAGFlow Async SDK

An **async-first Python SDK** for interacting with the RAGFlow API.

Provides clean, typed, and production-ready access to RAGFlow features such as:

- Dataset & document management  
- Document chunking & ingestion  
- File & folder management  
- Knowledge Graph (GraphRAG)  
- Background tasks (parsing, knowledge construction)  
- Chat & Agent sessions with **streaming (SSE) support**  

---

## Installation
Requires **Python 3.10+**.

```bash
pip install ragflow-async-sdk
```

For async file uploads with `file_from_path`, also install:

```bash
pip install aiofiles
```

---

## Quick Start

```python
from ragflow_async_sdk import AsyncRAGFlowClient

client = AsyncRAGFlowClient(
    api_key="YOUR_API_KEY",
    base_url="http://your-ragflow-address"
)
```

---

## Examples

### Chat

- **Non-streaming**

```python
chat = await client.chats.create(name="demo-chat")
session = await client.chats.create_session(chat.id)

result = await client.chats.ask(chat.id, session.id, "Hello")
print(result.answer)
```

- **Streaming (SSE)**

```python
async for chunk in await client.chats.ask(chat.id, session.id, "Hello", stream=True):
    print(chunk.answer, end="", flush=True)
```

### Dataset

- **Create**
```python
dataset = await client.datasets.create_dataset(name="my_dataset")
print(dataset.id, dataset.to_dict())
```

- **List**
```python
datasets, total = await client.datasets.list_datasets()
dataset_ids = [item.id for item in datasets]
```

### Document

- **Upload**
```python
from ragflow_async_sdk.utils.files import file_from_path

file_paths = ["test.txt", "test.pdf"]
files_to_send = [await file_from_path(p) for p in file_paths]

uploaded_docs, total = await client.documents.upload_documents(dataset.id, files=files_to_send)
```

- **Download**
```python
import aiofiles, os

file_path = "./downloads/test.pdf"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

content = await client.files.download_file(dataset.id, document.id)

async with aiofiles.open(file_path, "wb") as f:
    await f.write(content)
```

---

## Error Handling

```python
from ragflow_async_sdk.exceptions import (
    RAGFlowAPIError,
    RAGFlowValidationError,
    RAGFlowTimeoutError,
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

## Design Principles

- Async-first (`async` / `await` everywhere)
- No httpx leakage in public APIs
- Streaming support via async generators
- Clear separation of models / APIs / types
- Typed return values

---

## Documentation

📘 **Full documentation:**  
See the complete usage guide here:  

👉 **[User Guide](docs/user-guide.md)**

---

## License

Apache License 2.0
