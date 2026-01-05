from __future__ import annotations

from typing import Optional, Dict, Any, Tuple, List

from .mixins import SessionMixin
from ..apis.base import BaseAPI
from ..exceptions import RAGFlowValidationError
from ..models.agent import Agent
from ..models.session import AgentSession
from ..utils.validators import require_params


class AgentsAPI(SessionMixin[AgentSession], BaseAPI):
    """
    API for interacting with agents.
    """
    _parent_type = "agents"
    _session_model = AgentSession

    async def list_agents(
            self,
            *,
            page: int = 1,
            page_size: int = 30,
            orderby: str = "create_time",
            desc: bool = True,
            agent_id: Optional[str] = None,
            title: Optional[str] = None,
    ) -> Tuple[List[Agent], int]:
        """
        List agents with optional filters.
        """
        params: Dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            "orderby": orderby,
            "desc": desc,
            "id": agent_id,
            "title": title,
        }
        params = self._normalize_request(params)

        url = "/agents"
        resp = await self._client.get(url, params=params)
        resp = self._handle_response(resp)

        data = resp.get("data", [])
        agents = [Agent.from_raw(item) for item in data]
        total = len(agents)

        return agents, total

    async def create_agent(
            self,
            title: str,
            dsl: dict,
            *,
            description: Optional[str] = None,
    ) -> bool:
        """
        Create a new agent.
        """
        require_params(title=title, dsl=dsl)

        payload: Dict[str, Any] = {
            "title": title,
            "description": description,
            "dsl": dsl,
        }
        payload = self._normalize_request(payload)

        url = "/agents"
        resp = await self._client.post(url, json=payload)
        resp = self._handle_response(resp)

        return bool(resp.get("data", False))

    async def update_agent(
            self,
            agent_id: str,
            *,
            title: Optional[str] = None,
            description: Optional[str] = None,
            dsl: Optional[dict] = None,
    ) -> bool:
        """
        Update an existing agent.
        """
        require_params(agent_id=agent_id)

        payload: Dict[str, Any] = {
            "title": title,
            "description": description,
            "dsl": dsl,
        }
        payload = self._normalize_request(payload)

        if not payload:
            raise RAGFlowValidationError("No fields provided to update.")

        url = f"/agents/{agent_id}"
        resp = await self._client.put(url, json=payload)
        resp = self._handle_response(resp)

        return bool(resp.get("data", False))

    async def delete_agent(
            self,
            agent_id: str,
    ) -> bool:
        """
        Delete an agent by ID.
        """
        require_params(agent_id=agent_id)

        url = f"/agents/{agent_id}"
        resp = await self._client.delete(url)
        resp = self._handle_response(resp)

        return bool(resp.get("data", False))

    async def create_session(
            self,
            agent_id: str,
            *,
            name: str = "New session",
            user_id: Optional[str] = None,
    ) -> AgentSession:
        """
        Create a new session under an agent.
        """
        return await super().create_session(
            parent_id=agent_id,
            name=name,
            user_id=user_id
        )

    async def list_sessions(
            self,
            agent_id: str,
            *,
            page: int = 1,
            page_size: int = 30,
            orderby: str = "create_time",
            desc: bool = True,
            name: Optional[str] = None,
            session_id: Optional[str] = None,
            user_id: Optional[str] = None,
    ) -> Tuple[List[AgentSession], int]:
        """
        List sessions for an agent.
        """
        return await super().list_sessions(
            parent_id=agent_id,
            page=page,
            page_size=page_size,
            orderby=orderby,
            desc=desc,
            name=name,
            session_id=session_id,
            user_id=user_id,
        )

    async def update_session(
            self,
            agent_id: str,
            session_id: str,
            *,
            name: Optional[str] = None,
            user_id: Optional[str] = None,
    ) -> None:
        """
        Update an agent session.
        """
        await super().update_session(
            parent_id=agent_id,
            session_id=session_id,
            name=name,
            user_id=user_id
        )

    async def delete_sessions(
            self,
            agent_id: str,
            session_ids: Optional[str | List[str]] = None,
    ) -> None:
        """
        Delete one or more agent sessions.
        """
        await super().delete_sessions(
            parent_id=agent_id,
            session_ids=session_ids
        )
