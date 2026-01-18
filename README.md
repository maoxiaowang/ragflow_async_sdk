# RAGFlow Async SDK

## Overview

An **async-first Python SDK** for interacting with the RAGFlow API.

Provides clean, typed, and production-ready access to RAGFlow features such as:

* Dataset & document management
* Document chunking & ingestion
* File & folder management
* Knowledge Graph (GraphRAG)
* Background tasks (parsing, knowledge construction)
* Chat & Agent sessions with **streaming (SSE) support**

---

## ⚡ Quick Start

### 💿 Installation

Requires **Python 3.10+**.

```bash
pip install ragflow-async-sdk
```

### 🚀 Getting Started

All operations in the RAGFlow SDK are asynchronous. To use the SDK, first initialize the client and then run async calls inside Python's `asyncio` event loop.

#### 🛠 Initialization

```python
from ragflow_async_sdk import AsyncRAGFlowClient

client = AsyncRAGFlowClient(
    server_url="http://your-ragflow-address",
    api_key="YOUR_API_KEY",
)
```

#### ⏩ Run with asyncio

```python
import asyncio

async def main():
    # Example: Health check
    system_health = await client.systems.healthz()
    print(system_health.status)

# Run the async main function
asyncio.run(main())
```

---

## 📚 Documentation

### 📝 User Guide
* [User Guide](docs/md/guides/user_guide.md)

### ⚡ FastAPI Integration
* [Usage Examples](docs/md/guides/fastapi_usage_examples.md) 

### 🧩 Core Modules

* [Datasets](docs/md/references/api_reference.md#-dataset-apis)
* [Documents](docs/md/references/api_reference.md#-document-apis)
* [Chunks](docs/md/references/api_reference.md#-chunk-apis)
* [Chat Assistants](docs/md/references/api_reference.md#-chat-apis)
* [Agents](docs/md/references/api_reference.md#-agent-apis)
* [Files](docs/md/references/api_reference.md#-file-apis)
* [System](docs/md/references/api_reference.md#-system-apis)

### 📖 Full API Reference

* [API Reference](docs/md/references/api_reference.md)

### 💡 Error Reference

* [Error Reference](docs/md/references/error_reference.md#error-reference)

### 🧬 Entities Reference

* [Entities Reference](docs/md/references/entities_reference.md#entities-reference)

### 🧪 Testing

* [Testing Guide](docs/md/guides/testing_guide.md)

---

## License

Apache License 2.0
