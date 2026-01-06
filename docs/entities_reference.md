# Entities Reference

This section describes the main data models (Entities) used in the RAGFlow SDK.  
Entities represent resources like datasets, documents, chunks, files, chats, agents, and sessions.  
They provide convenient accessors, serialization methods, and encapsulate the raw API data.

---

## Common Entity Methods

All entities share several helper methods:

| Method | Description |
|--------|-------------|
| `.id` | Returns the unique identifier of the entity. |
| `.to_dict(export_fields=...)` | Convert entity to a dictionary. Optional `export_fields` to select specific keys. |
| `.to_json(pretty=False)` | Serialize entity to JSON string. `pretty=True` formats the output nicely. |
| `._raw` | Access the raw API response dictionary for advanced usage. |

---

## Examples

### Dataset
```python
dataset = await client.datasets.get_dataset(dataset_id="123")

# Access attributes
print(dataset.id, dataset.name)

# Convert to dictionary
dataset_dict = dataset.to_dict(export_fields=["id", "name"])
print(dataset_dict)

# Convert to JSON
dataset_json = dataset.to_json(pretty=True)
print(dataset_json)

# Access raw response
raw_data = dataset._raw
```

### Document
```python
documents, total = await client.documents.list_documents(dataset_id="123")
doc = documents[0]

print(doc.id, doc.name)
print(doc.to_dict())
print(doc.to_json(pretty=True))
```

### Chunk
```python
chunks, count = await client.chunks.list_chunks(dataset_id="123", document_id="doc_456")
chunk = chunks[0]

print(chunk.id, chunk.content)
print(chunk.to_dict(export_fields=["id", "content"]))
```

### ChatCompletionResult
```python
result = await client.chats.ask(chat_id="chat_123", session_id="sess_456", prompt="Hello!")

print(result.text)  # Generated text
print(result.to_dict())
print(result.to_json(pretty=True))
```

### AgentCompletionResult
```python
result = await client.agents.ask(agent_id="agent_123", session_id="sess_456", prompt="Run analysis")

print(result.text)
print(result.to_dict())
```

### Session
```python
sessions, total = await client.chats.list_sessions(chat_id="chat_123")
session = sessions[0]

print(session.id, session.name)
print(session.to_dict())
```

---

**Notes:**
- Not every entity class is shown, but the usage pattern is the same for all.
- `._raw` is useful for inspecting additional data returned by the server that may not have dedicated attributes.
