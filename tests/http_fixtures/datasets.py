from .utils import _json_response


def register_dataset_routes(fake_httpx):

    async def create_dataset(**kwargs):
        payload = kwargs["json"]
        return _json_response(
            data=payload
        )

    async def list_datasets(**kwargs):
        datasets = [
            {"id": "ds_id_1", "name": "ds_name_1"},
        ]

        return _json_response(data=datasets, total_datasets=len(datasets))

    async def get_dataset(**kwargs):
        return _json_response()

    async def update_dataset(**kwargs):
        return _json_response()

    async def delete_datasets(**kwargs):
        return _json_response()

    fake_httpx.route("POST", "/datasets", create_dataset)
    fake_httpx.route("GET", "/datasets", list_datasets)
    fake_httpx.route("GET", "/datasets/get", get_dataset)
    fake_httpx.route("PUT", "/datasets/{dataset_id}", update_dataset)
    fake_httpx.route("DELETE", "/datasets", delete_datasets)
