from .utils import _json_response, _stream_response


def register_document_routes(fake_httpx):
    async def list_documents(**kwargs):
        dataset_id = kwargs["dataset_id"]
        params = kwargs.get("params") or {}
        name_filter = params.get("name")
        document_id_filter = params.get("id")
        all_docs = [
            {
                "id": "doc_id_1",
                "name": "doc_name_1.doc",
                "dataset_id": dataset_id,
                "type": "doc",
                "location": "doc_id_1.doc"
            },
            {
                "id": "doc_id_2",
                "name": "doc_name_2.doc",
                "dataset_id": dataset_id,
                "type": "doc",
                "location": "doc_name_2.doc"
            }
        ]
        filtered = all_docs
        if name_filter is not None:
            filtered = [doc for doc in filtered if doc["name"] == name_filter]
        if document_id_filter is not None:
            filtered = [doc for doc in filtered if doc["id"] == document_id_filter]
        return _json_response(
            data={
                "docs": filtered,
                "total": len(filtered)
            },
        )

    async def get_document(**kwargs):
        return _json_response()

    async def upload_documents(**kwargs):
        data = list()
        files = kwargs["files"]
        for i, (_, file_tuple) in enumerate(files):
            data.append({
                "id": f"doc_{i}",
                "name": file_tuple[0],
                "location": file_tuple[0],
                "dataset_id": kwargs["dataset_id"],
                "type": file_tuple[2].split(".")[0] or "unknown",
            })
        return _json_response(data=data)

    async def download_document(**kwargs):
        return _stream_response(b"file content")

    async def delete_document(**kwargs):
        return _json_response()

    async def parse_documents(**kwargs):
        return _json_response()

    async def stop_parsing_documents(**kwargs):
        return _json_response()

    fake_httpx.route("GET", "/datasets/{dataset_id}/documents", list_documents)
    fake_httpx.route("GET", "/datasets/{dataset_id}/documents/{document_id}/get", get_document)
    fake_httpx.route("POST", "/datasets/{dataset_id}/documents", upload_documents)
    fake_httpx.route("GET", "/datasets/{dataset_id}/documents/{document_id}", download_document)
    fake_httpx.route("DELETE", "/datasets/{dataset_id}/documents", delete_document)
    fake_httpx.route("POST", "/datasets/{dataset_id}/chunks", parse_documents)
    fake_httpx.route("DELETE", "/datasets/{dataset_id}/chunks", stop_parsing_documents)
