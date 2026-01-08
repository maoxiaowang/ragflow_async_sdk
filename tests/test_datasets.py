import pytest

from ragflow_async_sdk.models.dataset import Dataset
from .fixtures.client import client


@pytest.mark.asyncio
async def test_create_dataset(client):
    dataset_name = "ds_name_1"
    dataset = await client.datasets.create_dataset(name=dataset_name)
    assert isinstance(dataset, Dataset)
    assert dataset.name == dataset_name


@pytest.mark.asyncio
async def test_list_datasets(client):
    datasets, total = await client.datasets.list_datasets()
    assert isinstance(datasets, list)
    assert isinstance(total, int)
    assert len(datasets) == total
    for ds in datasets:
        assert isinstance(ds, Dataset)


@pytest.mark.asyncio
async def test_get_dataset(client):
    dataset_name = "ds_name_1"
    dataset = await client.datasets.get_dataset(name=dataset_name)
    assert isinstance(dataset, Dataset)
    assert dataset.name == dataset_name


@pytest.mark.asyncio
async def test_update_dataset(client):
    result = await client.datasets.update_dataset("ds_id_1", name="updated_ds")
    assert result is None


@pytest.mark.asyncio
async def test_delete_dataset(client):
    result = await client.datasets.delete_datasets(["ds_id_1"])
    assert result is None
