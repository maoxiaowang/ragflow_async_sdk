# RAGFlow Async SDK

<a href="https://ragflow-async-sdk.readthedocs.io/en/latest/index.html" target="_blank"> 
    <img alt="Online Document" src="https://img.shields.io/badge/Online-Document-4e6b99?style=flat&logo=read-the-docs&logoColor=white"> 
</a>&nbsp;
<a href="https://github.com/maoxiaowang/ragflow_async_sdk/blob/main/LICENSE" target="_blank"> 
    <img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-3c9d6e?style=flat&logo=github&logoColor=white"> 
</a>&nbsp;
<a href="https://pypi.org/project/ragflow-async-sdk/" target="_blank"> 
    <img alt="PyPI" src="https://img.shields.io/badge/PyPI-v0.1.1-9b4ecc?style=flat&logo=python&logoColor=white"> 
</a>

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

## RAGFlow Version Support

This SDK version **0.1.x** supports the following RAGFlow versions:

| SDK Version | RAGFlow Version  | Support Level                                              | Notes                              |
|-------------|------------------|------------------------------------------------------------|------------------------------------|
| 0.1.x       | \>= 0.22         | ![✅](https://img.shields.io/badge/-Fully_Supported-4CAF50) | All SDK interfaces fully supported |
| 0.1.x       | 0.22 and earlier | ![❌](https://img.shields.io/badge/-Untested-B0BEC5)        | Not guaranteed                     |
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

[Online Document](https://ragflow-async-sdk.readthedocs.io/en/latest/index.html)

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
