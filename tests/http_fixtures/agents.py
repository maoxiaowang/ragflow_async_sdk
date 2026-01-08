from .utils import _json_response


def register_agent_routes(fake_httpx):

    async def create_agent(**kwargs):
        return _json_response(data=True)

    async def list_agents(**kwargs):
        agents = [
            {"id": "agent_id_1", "title": "agent_tile_1"},
        ]
        return _json_response(data=agents)

    async def get_agent(**kwargs):
        return _json_response()

    async def update_agent(**kwargs):
        return _json_response()

    async def delete_agents(**kwargs):
        return _json_response()

    fake_httpx.route("POST", "/agents", create_agent)
    fake_httpx.route("GET", "/agents", list_agents)
    fake_httpx.route("GET", "/agents/new_ds", get_agent)
    fake_httpx.route("PUT", "/agents/mock_id", update_agent)
    fake_httpx.route("DELETE", "/agents", delete_agents)
