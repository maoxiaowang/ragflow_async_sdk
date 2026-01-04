# ragflow-async-sdk

Python asynchronous SDK for managing RAGFlow APIs, including datasets, knowledge graphs, and RAPTOR tasks.

## Installation

```bash
pip install ragflow-async-sdk
```

## Initialization

```python
from ragflow_async_sdk.client import AsyncRAGFlowClient

# Initialize the client with your API Key
client = AsyncRAGFlowClient(api_key="YOUR_API_KEY", base_url="http://your-ragflow-address")
```

## Dataset Usage Examples

### List Datasets

```python
from ragflow_async_sdk.models.dataset import Dataset

datasets, total = await client.datasets.list_datasets(page=1, page_size=10)
for ds in datasets:
    print(ds.name, ds.permission)
print("Total datasets:", total)
```

### Create a Dataset

```python
from ragflow_async_sdk.types.ingestion import ChunkMethod
from ragflow_async_sdk.types.permission import Permission

ds = await client.datasets.create_dataset(
    name="my_dataset",
    chunk_method=ChunkMethod.NAIVE,
    permission=Permission.ME
)
print(ds.to_dict())
```

### Update a Dataset

```python
await client.datasets.update_dataset(
    dataset_id=ds.id,
    name="updated_dataset",
    description="Updated description"
)
```

### Delete Datasets

```python
# Delete a single dataset
await client.datasets.delete_datasets(ids=[ds.id])

# Delete multiple datasets
await client.datasets.delete_datasets(ids=["id1", "id2"])

# Delete all datasets
await client.datasets.delete_datasets(ids=None)
```

## Knowledge Graph (GraphRAG) Usage

### Get Knowledge Graph

```python
from ragflow_async_sdk.models.dataset import KnowledgeGraph

kg: KnowledgeGraph = await client.datasets.get_knowledge_graph(dataset_id=ds.id)
print("Nodes:", len(kg.nodes))
print("Edges:", len(kg.edges))
```

### Construct Knowledge Graph

```python
graphrag_task_id = await client.datasets.construct_knowledge_graph(dataset_id=ds.id)
print("GraphRAG task ID:", graphrag_task_id)
```

### Get GraphRAG Status

```python
from ragflow_async_sdk.models.task import TaskStatus

status: TaskStatus = await client.datasets.get_graphrag_status(dataset_id=ds.id)
print("Progress:", status.progress, "Message:", status.progress_msg)
```

### Delete Knowledge Graph

```python
success = await client.datasets.delete_knowledge_graph(dataset_id=ds.id)
print("Deletion success:", success)
```

## RAPTOR Usage

### Construct RAPTOR

```python
raptor_task_id = await client.datasets.construct_raptor(dataset_id=ds.id)
print("RAPTOR task ID:", raptor_task_id)
```

### Get RAPTOR Status

```python
status: TaskStatus = await client.datasets.get_raptor_status(dataset_id=ds.id)
print("Progress:", status.progress, "Message:", status.progress_msg)
```

## Exception Handling

```python
from ragflow_async_sdk.exceptions import RAGFlowAPIError, RAGFlowValidationError
from ragflow_async_sdk.http import HTTPTimeoutError

try:
    await client.datasets.list_datasets()
except RAGFlowValidationError as e:
    print("Validation error:", e.message)
except RAGFlowAPIError as e:
    print("API error:", e.message, e.details)
except HTTPTimeoutError:
    print("Request timed out")
```

## Type Notes

- `Dataset.to_dict()` converts a Dataset object into a dictionary.
- `KnowledgeGraph` contains `nodes`, `edges`, and optional `mind_map`.
- `TaskStatus` contains `progress`, `progress_msg`, timestamps, and task metadata.

