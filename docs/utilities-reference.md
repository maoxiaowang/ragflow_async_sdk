# Utilities Reference

This section documents the utility functions provided by the RAGFlow SDK.  

These helpers assist with input validation, ID normalization, file preparation for uploads, 
and data conversion tasks. They are intended for internal SDK operations as well as for developers
who need to prepare data or parameters before calling the SDK API methods.

## Validators
The SDK provides helper functions to validate input parameters before making API calls.

- `require_params(**params)`: Ensure required parameters are provided.
- `validate_enum(value, enum_class, param_name)`: Validate that a value is a member of an Enum.

### Example Usage
```python
from ragflow_async_sdk.utils.validators import require_params, validate_enum

# Simple parameter check
require_params(dataset_id=dataset_id, document_id=document_id)

# Validate enum value
order_by = validate_enum("TYPE_A", OrderBy, "order_by")
```

## Normalizers

Helper functions to normalize IDs or lists of IDs.

- `normalize_ids(ids, param_name)`: Converts a single ID or list of IDs into a normalized list of strings.

### Example Usage

```python
from ragflow_async_sdk.utils.normalizers import normalize_ids

# Single string ID
ids = normalize_ids("123", "dataset_ids")

# List of IDs
ids_list = normalize_ids(["123", "456"], "dataset_ids")
```

## Prepare Upload Files

The SDK provides helpers to create file tuples for multipart uploads.

- `file_from_path(path)`: From local file path.
- `file_from_bytes(filename, content)`: From bytes content.
- `file_from_url(url)`: Download from a URL.

Each returns a tuple (filename, bytes, content_type), which is compatible with multipart/form-data upload.

### 1. Prepare file tuple

- Using helper functions
```python
from ragflow_async_sdk.utils.files import file_from_path, file_from_bytes, file_from_url

upload_list = [
    await file_from_path("example.txt"),  # Local file
    file_from_bytes("hello.txt", b"Hello World"),  # Raw bytes
    await file_from_url("https://example.com/file.pdf")  # Remote URL
]
```

- Or manually
```python
upload_list = []

# Prepare manually
async with aiofiles.open("example.pdf", "rb") as f:
    upload_list.append(("example.pdf", await f.read(), "application/pdf"))
```

### 2. Upload
```python
# Upload as documents
docs, count = await client.datasets.upload_documents(
    dataset_id=dataset.id,
    files=upload_list,
)

# Upload as files
uploaded_files = await client.files.upload_files(
    files=upload_list,
    parent_id=root_folder.id
)
```

## Convertors

Functions to convert or parse data returned from the API.
- `parse_time_field(value)`: Convert RFC 2822 date strings to UTC datetime objects.

### Example Usage

```python
dt = parse_time_field("Tue, 30 Dec 2025 23:15:20 GMT")
```
