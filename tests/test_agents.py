import pytest
from tests.fixtures.client import client

from ragflow_async_sdk.models import Agent


# --------------------
# Agent Tests
# --------------------

# @pytest.mark.asyncio
# async def test_create_agent(client):
#     result = await client.agents.create_agent(
#         title="new_agent", dsl={}
#     )
#     assert result is None
#
#
# @pytest.mark.asyncio
# async def test_list_agents(client):
#     agents, total = await client.agents.list_agents()
#     assert isinstance(agents, list)
#     assert len(agents) == total
#     for agent in agents:
#         assert isinstance(agent, Agent)
#
#
# @pytest.mark.asyncio
# async def test_get_agent(client):
#     mock_title = "agent_tile_1"
#     agent = await client.agents.get_agent(title=mock_title)
#     assert agent.title == mock_title
