# RAGFlow Async SDK

An **async-first Python SDK** for interacting with the RAGFlow API.

This SDK is designed for **Python async applications** and provides
clean, typed, and production-ready access to RAGFlow features such as:

-   Dataset & document management
-   Document chunking & ingestion (chunk strategies, parsing, reprocessing)
-   Knowledge Graph (GraphRAG)
-   Background tasks (document parsing, knowledge construction) with a unified TaskStatus model
-   Chat & Agent sessions with **streaming (SSE) support**
-   System health check

------------------------------------------------------------------------

## Installation

``` bash
pip install ragflow-async-sdk
```

------------------------------------------------------------------------

## Quick Start

``` python
from ragflow_async_sdk.client import AsyncRAGFlowClient

client = AsyncRAGFlowClient(
    api_key="YOUR_API_KEY",
    base_url="http://your-ragflow-address"
)
```

------------------------------------------------------------------------

## Chat Example

### Non-streaming

``` python
chat = await client.chats.create(name="demo-chat")
session = await client.chats.create_session(chat.id)

result = await client.chats.ask(
    chat.id,
    session.id,
    "你好"
)

print(result.answer)
```

### Streaming (SSE)

``` python
async for chunk in await client.chats.ask(
    chat.id,
    session.id,
    "你好",
    stream=True,
):
    print(chunk.answer, end="", flush=True)
```

------------------------------------------------------------------------

## Dataset Example

``` python
from ragflow_async_sdk.types.ingestion import ChunkMethod

dataset = await client.datasets.create_dataset(
    name="my_dataset",
    chunk_method=ChunkMethod.NAIVE,
)

datasets, total = await client.datasets.list_datasets()
```

------------------------------------------------------------------------

## Error Handling

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
except RAGFlowAPIError as e:
    print("API error:", e.message)
except RAGFlowTimeoutError:
    print("Request timed out")
```

------------------------------------------------------------------------

## Design Principles

-   Async-first (`async` / `await` everywhere)
-   No httpx leakage in public APIs
-   Streaming support via async generators
-   Clear separation of models / APIs / types
-   Typed return values

------------------------------------------------------------------------

## Documentation

📘 **Full documentation:**\
See the complete usage guide here:

👉 **[User Guide](docs/user-guide.md)**

The User Guide goes beyond basic examples and covers advanced usage, including:

- Detailed API usage with real-world examples
- Streaming response handling patterns
- Background task lifecycle and status polling
- Error handling and retry strategies

------------------------------------------------------------------------

## License

Apache License 2.0
