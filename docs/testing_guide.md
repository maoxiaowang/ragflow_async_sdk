# Testing

This document describes how to run and debug tests for the **RAGFlow Async SDK**.

## Requirements

- Python 3.10+
- pytest

## Running tests

```bash
pytest
```

## Logging

Tests use Python's standard `logging` module.

To enable debug logs during test execution:

```bash
pytest --log-level=DEBUG
```

## Notes

- Most tests rely on mocked HTTP responses.
- Integration tests are not yet available.
- Some integration tests may be added in the future and may require network access and valid credentials.
