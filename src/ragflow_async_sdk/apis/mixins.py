# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from __future__ import annotations

from typing import (
    Optional, Any, Type,
    TypeVar, Generic, Callable, AsyncGenerator
)

from ..exceptions import RAGFlowValidationError, RAGFlowAPIError
from ..http import AsyncHTTPClient
from ..models import AgentCompletionResult, ChatCompletionResult
from ..models.session import BaseSession
from ..types.session import SessionType
from ..utils.entity_helpers import get_single_or_raise
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params, validate_enum, resolve_unique_field

T = TypeVar("T", bound=BaseSession)


class SessionMixin(Generic[T]):
    """
    CRUD operations for chat or agent sessions.

    Subclasses must define:
        - _parent_type: str, either "chats" or "agents"
        - _session_model: the session model class
    """

    _parent_type: str
    _session_model: Type[T]

    _client: AsyncHTTPClient
    _normalize_request: Callable[..., dict[str, Any]]
    _handle_response: Callable[..., dict[str, Any]]
    _parse_sse_line: Callable[[str], dict[str, Any]]

    async def create_session(self, parent_id: str, **kwargs) -> T:
        """
        Create a new session under a chat or agent.

        Args:
            parent_id: ID of the chat or agent parent.
            **kwargs: Additional session parameters (e.g., name, user_id).

        Returns:
            Instance of the session model (T).
        """
        require_params(parent_id=parent_id)
        url = f"/{self._parent_type}/{parent_id}/sessions"
        resp = await self._client.post(url, json=kwargs)
        resp = self._handle_response(resp)
        return self._session_model.from_raw(resp.get("data", {}))

    async def list_sessions(
        self,
        parent_id: str,
        *,
        page: int = 1,
        page_size: int = 30,
        orderby: str = "create_time",
        desc: bool = True,
        name: Optional[str] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> tuple[list[T], int]:
        """
        List sessions for a chat or agent.

        Args:
            parent_id: Chat or agent ID.
            page: Page number.
            page_size: Items per page.
            orderby: Field to sort by.
            desc: Whether to sort descending.
            name: Optional session name filter.
            session_id: Optional session ID filter.
            user_id: Optional user ID filter.

        Returns:
            Tuple of (sessions list, total count).
        """
        require_params(parent_id=parent_id)
        params = {
            "page": page,
            "page_size": page_size,
            "orderby": orderby,
            "desc": desc,
            "name": name,
            "id": session_id,
            "user_id": user_id,
        }
        params = self._normalize_request(params)
        url = f"/{self._parent_type}/{parent_id}/sessions"
        resp = await self._client.get(url, params=params)
        resp = self._handle_response(resp)
        data = resp.get("data", [])
        sessions = [self._session_model.from_raw(item) for item in data]
        return sessions, len(sessions)

    async def get_session(
        self,
        parent_id: str,
        *,
        session_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> T:
        """
        Get a single session by session_id or name.
        Exactly one of session_id or name must be provided.
        """
        param_name, param_value = resolve_unique_field(session_id=session_id, name=name)

        sessions, _ = await self.list_sessions(
            parent_id=parent_id,
            page=1,
            page_size=2,
            session_id=session_id,
            name=name,
        )

        return get_single_or_raise(
            items=sessions,
            key_name=param_name,
            key_value=param_value,
            entity_name="Session"
        )

    async def update_session(
        self,
        parent_id: str,
        session_id: str,
        *,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> None:
        """
        Update a chat or agent session.

        Args:
            parent_id: Chat or agent ID.
            session_id: Session ID.
            name: Optional new name.
            user_id: Optional new user ID.

        Raises:
            RAGFlowValidationError: If no fields are provided.
        """
        require_params(parent_id=parent_id, session_id=session_id)
        payload = self._normalize_request({"name": name, "user_id": user_id})
        if not payload:
            raise RAGFlowValidationError("No fields provided to update.")
        url = f"/{self._parent_type}/{parent_id}/sessions/{session_id}"
        resp = await self._client.put(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def delete_sessions(
        self,
        parent_id: str,
        session_ids: Optional[str | list[str]] = None,
    ) -> None:
        """
        Delete one or more chat or agent sessions.

        Args:
            parent_id: Chat or agent ID.
            session_ids: Session ID(s) to delete. If None, delete all sessions.

        Raises:
            RAGFlowAPIError: If deletion fails.
        """
        require_params(parent_id=parent_id)
        ids = normalize_ids(session_ids)
        payload = self._normalize_request({"ids": ids})
        url = f"/{self._parent_type}/{parent_id}/sessions"
        resp = await self._client.delete(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def ask(
        self,
        parent_id: str,
        session_id: str,
        prompt: str,
        *,
        session_type: Optional[SessionType | str] = None,
        stream: bool = False,
        **kwargs,
    ) -> (ChatCompletionResult |
          AgentCompletionResult |
          AsyncGenerator[ChatCompletionResult | AgentCompletionResult, None]
    ):
        """
        Ask a question in a session.

        Args:
            parent_id: Chat or agent ID.
            session_id: Session ID.
            prompt: User question.
            session_type: Optional session type, defaults to self._parent_type.
            stream: Whether to return streaming results.
            **kwargs: Extra parameters (temperature, top_p, etc.).

        Returns:
            Either a single completion result or an async generator if streaming.
        """
        require_params(parent_id=parent_id, session_id=session_id, prompt=prompt)
        stype = validate_enum(session_type, SessionType, "stype") or self._parent_type
        payload = {"question": prompt, "session_id": session_id, "stream": stream}
        payload.update(kwargs)
        url = f"/{stype}/{parent_id}/completions"

        if stream:
            async def generator() -> AsyncGenerator[
                ChatCompletionResult | AgentCompletionResult, None
            ]:
                async with self._client.stream("POST", url, json=payload) as stream_resp:
                    async for line in stream_resp.aiter_lines():
                        if not line:
                            continue
                        line = line.strip()
                        if line.startswith("data:"):
                            line = line[5:].strip()
                            if line == "[DONE]":
                                break
                        try:
                            line_resp = self._parse_sse_line(line)
                            line_data = line_resp.get("data", {})
                        except RAGFlowAPIError:
                            continue
                        if line_data is True:
                            break
                        yield self._structure_result(line_data, stype)
            return generator()
        else:
            resp = await self._client.post(url, json=payload)
            data = self._handle_response(resp)["data"]
            return self._structure_result(data, stype)

    @staticmethod
    def _structure_result(data: dict, session_type: str):
        """Convert raw API data to the appropriate session result model."""
        if session_type == SessionType.CHAT.value:
            return ChatCompletionResult.from_raw(data)
        elif session_type == SessionType.AGENT.value:
            return AgentCompletionResult.from_raw(data)
        else:
            raise ValueError(f"Unknown session_type: {session_type}")
