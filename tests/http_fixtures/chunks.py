from tests.http_fixtures.utils import _json_response


def register_chunk_routes(fake_httpx):

    async def add_chunk(**kwargs):
        dataset_id = kwargs["dataset_id"]
        document_id = kwargs["document_id"]
        payload = kwargs["json"]
        return _json_response(
            data={
                "chunk": {
                    "id": "chunk_id_1",
                    "dataset_id": dataset_id,
                    "document_id": document_id,
                    **payload,
                }
            }
        )

    fake_httpx.route("POST", "/datasets/{dataset_id}/documents/{document_id}/chunks", add_chunk)