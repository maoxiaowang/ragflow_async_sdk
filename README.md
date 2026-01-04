# ragflow-async-sdk

Python asynchronous SDK for managing RAGFlow related APIs.

## Installation

```bash
pip install ragflow-async-sdk
```

## Initialization

```python
from ragflow_async_sdk.client import RAGFlowClient

# Initialize the client with your API Key
client = RAGFlowClient(api_key="YOUR_API_KEY", base_url="http://your-ragflow-address")
```

## Dataset Usage Examples

### List Datasets

```python
from ragflow_async_sdk.models.dataset import Dataset
datasets, total = await client.datasets.list(page=1, page_size=10)
for ds in datasets:
    print(ds.name, ds.permission)
```

### Create a Dataset

```python
from ragflow_async_sdk.models.dataset import ChunkMethod, Permission

ds = await client.datasets.create(
    name="my_dataset",
    chunk_method=ChunkMethod.NAIVE,
    permission=Permission.ME
)
print(ds.to_dict())
```

### Update a Dataset

```python
await client.datasets.update(
    dataset_id=ds.id,
    name="updated_dataset",
    description="Updated description"
)
```

### Delete Datasets

```python
# Delete a single dataset
await client.datasets.delete(ids=[ds.id])

# Delete multiple datasets
await client.datasets.delete(ids=["id1", "id2"])

# Delete all datasets
await client.datasets.delete(ids=None)
```

## Exception Handling

```python
from ragflow_async_sdk.exceptions import RAGFlowAPIError, HTTPTimeoutError

try:
    await client.datasets.list()
except RAGFlowAPIError as e:
    print("API error:", e.message, e.details)
except HTTPTimeoutError:
    print("Request timed out")
```

## Type Notes

- `Dataset.to_dict()` converts a Dataset object into a dictionary

