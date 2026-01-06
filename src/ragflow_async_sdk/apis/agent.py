from typing import Optional, Any, AsyncGenerator

from .mixins import SessionMixin
from ..apis.base import BaseAPI
from ..exceptions import RAGFlowValidationError
from ..exceptions.api import RAGFlowConflictError, RAGFlowAPIError, RAGFlowResponseError
from ..models.agent import Agent, AgentCompletionResult
from ..models.session import AgentSession
from ..types import OrderBy
from ..utils.validators import require_params


class AgentAPI(SessionMixin[AgentSession], BaseAPI):
    """API for managing agents and their sessions."""

    _parent_type = "agents"
    _session_model = AgentSession

    async def list_agents(
        self,
        *,
        page: int = 1,
        page_size: int = 30,
        orderby: OrderBy | str = OrderBy.CREATE_TIME,
        desc: bool = True,
        agent_id: Optional[str] = None,
        title: Optional[str] = None,
    ) -> tuple[list[Agent], int]:
        """
        List agents with optional filters.

        Args:
            page: Page number.
            page_size: Number of items per page.
            orderby: Field to sort by.
            desc: Sort descending if True.
            agent_id: Optional filter by agent ID.
            title: Optional filter by agent title.

        Returns:
            Tuple containing a list of Agent instances and total count.
        """
        params = {
            "page": page,
            "page_size": page_size,
            "orderby": orderby,
            "desc": desc,
            "id": agent_id,
            "title": title,
        }
        params = self._normalize_request(params)

        resp = await self._client.get("/agents", params=params)
        resp = self._handle_response(resp)

        data = resp.get("data", [])
        agents = [Agent.from_raw(item) for item in data]
        return agents, len(agents)

    async def get_agent(
        self,
        *,
        agent_id: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Optional[Agent]:
        """
        Retrieve a single agent by ID or title.

        Exactly one of `agent_id` or `title` must be provided.

        Args:
            agent_id: Optional agent ID.
            title: Optional agent title.

        Returns:
            Agent instance if found, else None.

        Raises:
            RAGFlowValidationError: If both or neither of `agent_id` and `title` are provided.
            RAGFlowConflictError: If multiple agents match the query.
        """
        if not agent_id and not title:
            raise RAGFlowValidationError("Either agent_id or title must be provided")
        if agent_id and title:
            raise RAGFlowValidationError("Only one of agent_id or title can be provided")

        agents, _ = await self.list_agents(
            page=1, page_size=2, agent_id=agent_id, title=title
        )

        if not agents:
            return None

        if len(agents) > 1:
            key = f"id={agent_id}" if agent_id else f"title={title}"
            raise RAGFlowConflictError(f"Multiple agents found for {key}")

        return agents[0]

    async def create_agent(
        self,
        title: str,
        dsl: dict,
        *,
        description: Optional[str] = None,
    ) -> Agent:
        """
        Create a new agent.

        Args:
            title: Agent title.
            dsl: Agent DSL configuration (graph, components, retrieval, etc.).
            description: Optional description of the agent.

        Returns:
            Agent instance.

        Raises:
            RAGFlowAPIError: If creation fails.
            RAGFlowResponseError: If agent cannot be retrieved after creation.
        """
        require_params(title=title, dsl=dsl)

        payload = {
            "title": title,
            "description": description,
            "dsl": dsl,
        }
        payload = self._normalize_request(payload)

        resp = await self._client.post("/agents", json=payload)
        resp = self._handle_response(resp)

        if not resp.get("data"):
            raise RAGFlowAPIError("Create agent failed")

        agent = await self.get_agent(title=title)
        if agent is None:
            raise RAGFlowResponseError("Agent created but cannot be retrieved")

        return agent

    async def update_agent(
            self,
            agent_id: str,
            *,
            title: Optional[str] = None,
            description: Optional[str] = None,
            dsl: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Update an existing agent.

        Args:
            agent_id: Agent ID (required).
            title: Optional new title for the agent.
            description: Optional new description.
            dsl: Optional updated canvas DSL object.

        Raises:
            ValueError: If no fields are provided for update.
        """
        require_params(agent_id=agent_id)

        payload = {
            "title": title,
            "description": description,
            "dsl": dsl,
        }

        payload = self._normalize_request(payload)

        if not payload:
            raise RAGFlowValidationError("No fields provided to update.")

        url = f"/agents/{agent_id}"
        resp = await self._client.put(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def delete_agent(self, agent_id: str) -> bool:
        """
        Delete an agent by ID.

        Args:
            agent_id: Agent ID.

        Returns:
            True if deletion succeeded, False otherwise.
        """
        require_params(agent_id=agent_id)
        resp = await self._client.delete(f"/agents/{agent_id}")
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

        Args:
            agent_id: Agent ID.
            name: Optional session name.
            user_id: Optional user ID.

        Returns:
            AgentSession instance.
        """
        return await super().create_session(parent_id=agent_id, name=name, user_id=user_id)

    async def list_sessions(
        self,
        agent_id: str,
        *,
        page: int = 1,
        page_size: int = 30,
        orderby: OrderBy | str = OrderBy.CREATE_TIME,
        desc: bool = True,
        name: Optional[str] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> tuple[list[AgentSession], int]:
        """
        List sessions for an agent.

        Args:
            agent_id: Agent ID.
            page: Page number.
            page_size: Number of items per page.
            orderby: Field to sort by.
            desc: Sort descending if True.
            name: Optional session name filter.
            session_id: Optional session ID filter.
            user_id: Optional user ID filter.

        Returns:
            Tuple containing a list of AgentSession instances and total count.
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

    async def get_agent_session(
            self,
            agent_id: str,
            *,
            session_id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> Optional[AgentSession]:
        return await self.get_session(
            parent_id=agent_id,
            session_id=session_id,
            name=name,
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

        Args:
            agent_id: Agent ID.
            session_id: Session ID.
            name: Optional new session name.
            user_id: Optional new user ID.
        """
        await super().update_session(parent_id=agent_id, session_id=session_id, name=name, user_id=user_id)

    async def delete_sessions(
        self,
        agent_id: str,
        session_ids: Optional[str | list[str]] = None,
    ) -> None:
        """
        Delete one or more agent sessions.

        Args:
            agent_id: Agent ID.
            session_ids: Single or list of session IDs. If None, delete all sessions.
        """
        await super().delete_sessions(parent_id=agent_id, session_ids=session_ids)

    async def ask(
            self,
            agent_id: str,
            session_id: str,
            prompt: str,
            *,
            stream: bool = False,
            **kwargs,
    ) -> AgentCompletionResult | AsyncGenerator[AgentCompletionResult, None]:
        """
        Ask a question in an agent session.

        Args:
            agent_id: Agent ID.
            session_id: Session ID.
            prompt: User question.
            stream: Whether to return streaming results (default False).
            **kwargs: Additional parameters such as temperature, top_p, etc.

        Returns:
            - If `stream=False`: a single `AgentCompletionResult`.
            - If `stream=True`: an async generator yielding `AgentCompletionResult` items.

        Raises:
            RAGFlowValidationError: If required parameters are missing.
            RAGFlowAPIError: If API request fails.

        Example:
        ```python
        # Non-streaming
        result = await client.agents.ask(agent_id="agent_123", session_id="sess_456", prompt="Hello AI")
        print(result.text)

        # Streaming
        async for chunk in client.agents.ask(agent_id="agent_123", session_id="sess_456", prompt="Hello AI", stream=True):
            print(chunk.text)
        ```
        """
        return await super().ask(
            parent_id=agent_id,
            session_id=session_id,
            prompt=prompt,
            session_type="agents",
            stream=stream,
            **kwargs,
        )