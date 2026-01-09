# FastAPI Usage Examples

This document demonstrates how to integrate the **RAGFlow Async SDK** into a FastAPI project.
It covers common operations such as managing datasets, uploading/downloading documents, and interacting with chat sessions.

All examples use asynchronous endpoints (`async def`) since the SDK is async.

## 1️⃣ Initialize SDK Client

```python
from fastapi import FastAPI
from ragflow_async_sdk import AsyncRAGFlowClient

app = FastAPI()

client = AsyncRAGFlowClient(
    server_url="https://your-ragflow-server",
    api_key="your-api-key",
)
```

## 2️⃣ Operations Examples

```python
from fastapi import APIRouter, Query
from ragflow_async_sdk.models import Dataset

from app.main import app, client

datasets_router = APIRouter(prefix="/datasets", tags=["datasets"])
```

### List Datasets
```python
@app.get("/", response_model=list[Dataset])
async def list_datasets(
        page: int | None = Query(1, ge=1),
        page_size: int | None = Query(30, ge=1, le=100),
):
    """
    Retrieve a list of datasets with optional pagination.
    """
    datasets, total = await client.datasets.list_datasets(page=page, page_size=page_size)
    return datasets
```

### Create Datasets
```python
@app.post("/", response_model=Dataset)
async def create_dataset(name: str):
    """
    Create a new dataset with the given name.
    """
    dataset = await client.datasets.create_dataset(name=name)
    return dataset
```

### Update Datasets
```python
@app.put("/{dataset_id}")
async def update_dataset(dataset_id: str, new_name: str):
    """
    Update the name of an existing dataset.
    """
    await client.datasets.update_dataset(dataset_id, name=new_name)
    return {}
```

### Delete Datasets

```python
@app.delete("/{dataset_id}")
async def delete_dataset(dataset_id: str):
    """
    Delete a dataset by ID.
    """
    await client.datasets.delete_datasets([dataset_id])
    return {}
```

### Upload Documents

```python
from fastapi import UploadFile, File
from ragflow_async_sdk.models import Document
from ragflow_async_sdk.utils.files import file_from_bytes

@router.post("/{dataset_id}/documents", response_model=list[Document])
async def upload_documents(
        dataset_id: str,
        files: list[UploadFile] = File(...),
):
    """
    Upload one or more documents to a dataset.
    """
    files = [file_from_bytes(f.filename, await f.read(), f.content_type) for f in files]
    docs = await client.documents.upload_documents(dataset_id, files=files)
    return docs
```

### Download Document

```python
from fastapi.responses import StreamingResponse

@app.get("/{dataset_id}/documents/{document_id}/download")
async def download_document(dataset_id: str, document_id: str):
    """
    Download a document as a stream.
    """
    file = await client.documents.download_document(dataset_id, document_id)

    return StreamingResponse(
        file.stream,
        media_type=file.content_type,
        headers={"Content-Disposition": f'attachment; filename="{file.filename}"'}
    )
```

### Chat Interactions

```python
from pydantic import BaseModel
from ragflow_async_sdk.models import ChatCompletionResult

chats_router = APIRouter(prefix="/chats", tags=["chats"])

class ChatAskRequest(BaseModel):
    session_id: str | None = None
    question: str | None = None

@app.post("/{chat_id}/ask", response_model=ChatCompletionResult)
async def chat_ask(chat_id: str, body: ChatAskRequest):
    """
    Send a question to a chat session and receive an AI-generated response.
    """
    session = await client.chat.get_chat_session(chat_id, session_id=body.session_id)
    result = await client.chat.ask(chat_id, session.id, prompt=body.question)
    
    return result
```

## 3️⃣ Include Routers in Main App

```python
from app.routers import datasets_router, chats_router

app.include_router(datasets.router)
app.include_router(chats_router)
```

## ✅ Notes
1. **Async SDK**: All calls are asynchronous, use await inside async FastAPI endpoints.

2. **Streaming download**: download_document returns a DownloadedFile with stream, suitable for large files.

3. **Simple examples**: No authentication, validation, or advanced options are included here; for production, wrap with proper error handling and security.

4. **Chat usage**: Shows basic create_session + ask flow.