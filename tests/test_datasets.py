import pytest

from .conftest import mock_client


@pytest.mark.asyncio
async def test_list_datasets(mock_client):
    data, total = await mock_client.datasets.list()
    assert isinstance(data, list)
    assert isinstance(total, int)
    assert len(data) == total


@pytest.mark.asyncio
async def test_create_dataset(mock_client):
    dataset = await mock_client.datasets.create(name="new_ds")
    assert isinstance(dataset, dict)
    assert dataset["name"] == "new_ds"
