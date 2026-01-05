from __future__ import annotations

from typing import (
    Optional, Dict, Any, List, Tuple, Type, Union,
    TypeVar, Generic, Callable, AsyncGenerator
)

from ..exceptions import RAGFlowValidationError, RAGFlowAPIError
from ..http import AsyncHTTPClient
from ..models import AgentCompletionResult, ChatCompletionResult
from ..models.session import BaseSession
from ..types.session import SessionType
from ..utils.convertors import parse_enum
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params

T = TypeVar("T", bound=BaseSession)


class SessionMixin(Generic[T]):
    """
    CRUD operations for Chat or Agent sessions.
    Subclass must define _parent_type (str) and _session_model (class).
    """
    _parent_type: str
    _session_model: Type[T]

    _client: AsyncHTTPClient
    _normalize_request: Callable[..., Dict[str, Any]]
    _handle_response: Callable[..., Dict[str, Any]]
    _parse_sse_line: Callable[[str], Dict[str, Any]]

    async def create_session(self, parent_id: str, **kwargs) -> T:
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
    ) -> Tuple[List[T], int]:
        require_params(parent_id=parent_id)
        params: Dict[str, Any] = {
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

    async def update_session(
            self,
            parent_id: str,
            session_id: str,
            *,
            name: Optional[str] = None,
            user_id: Optional[str] = None,
    ) -> None:
        require_params(parent_id=parent_id, session_id=session_id)
        payload: Dict[str, Any] = {"name": name, "user_id": user_id}
        payload = self._normalize_request(payload)
        if not payload:
            raise RAGFlowValidationError("No fields provided to update.")

        url = f"/{self._parent_type}/{parent_id}/sessions/{session_id}"
        resp = await self._client.put(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def delete_sessions(
            self,
            parent_id: str,
            session_ids: Optional[Union[str, List[str]]] = None,
    ) -> None:
        """
        Delete one or more chat or agent sessions.
        :param parent_id:
        :param session_ids: The IDs of the sessions to delete. If it is not specified,
        all sessions associated with the specified chat assistant will be deleted.
        :return:
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
    ) -> Union[
        ChatCompletionResult,
        AgentCompletionResult,
        AsyncGenerator[Union[ChatCompletionResult, AgentCompletionResult], None],
    ]:
        """
        Ask a question in a session.
        :param parent_id: The chat/agent parent ID
        :param session_id: The session ID
        :param prompt: The user question
        :param session_type: Optional, "chats" or "agents"; defaults to self._parent_type
        :param stream: Whether to return streaming results
        :param kwargs: Extra parameters like temperature, top_p, etc.
        """
        require_params(parent_id=parent_id, session_id=session_id, prompt=prompt)

        stype = parse_enum(session_type) or self._parent_type
        payload = {"question": prompt, "session_id": session_id, "stream": stream}
        payload.update(kwargs)

        url = f"/{stype}/{parent_id}/completions"

        if stream:
            async def generator() -> AsyncGenerator[Union[ChatCompletionResult, AgentCompletionResult], None]:
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
        if session_type == SessionType.CHAT.value:
            return ChatCompletionResult.from_raw(data)
        elif session_type == SessionType.AGENT.value:
            return AgentCompletionResult.from_raw(data)
        else:
            raise ValueError(f"Unknown session_type: {session_type}")
