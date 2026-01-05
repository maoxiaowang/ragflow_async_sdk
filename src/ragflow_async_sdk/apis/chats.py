from typing import List, Optional, Dict, Any, Tuple, AsyncGenerator

from .base import BaseAPI
from .mixins import SessionMixin
from ..models.chat import ChatAssistant, ChatCompletionResult
from ..models.session import ChatSession
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params


class ChatsAPI(SessionMixin[ChatSession], BaseAPI):
    _parent_type = "chats"
    _session_model = ChatSession

    async def create_chat(
            self,
            name: str,
            *,
            dataset_ids: Optional[List[str]] = None,
            avatar: Optional[str] = None,
            llm: Optional[Dict[str, Any]] = None,
            prompt: Optional[Dict[str, Any]] = None,
    ) -> ChatAssistant:
        """
        Create a new chat assistant.
        """
        require_params(name=name)
        payload: Dict[str, Any] = {
            "name": name,
            "dataset_ids": normalize_ids(dataset_ids),
            "avatar": avatar,
            "llm": llm,
            "prompt": prompt,
        }
        payload = self._normalize_request(payload)
        resp = await self._client.post("/chats", json=payload)
        data = self._handle_response(resp).get("data", {})
        return ChatAssistant.from_raw(data)

    async def update_chat(
            self,
            chat_id: str,
            *,
            name: Optional[str] = None,
            dataset_ids: Optional[List[str]] = None,
            avatar: Optional[str] = None,
            llm: Optional[Dict[str, Any]] = None,
            prompt: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Update an existing chat assistant.
        """
        require_params(chat_id=chat_id)
        payload: Dict[str, Any] = {
            "name": name,
            "dataset_ids": dataset_ids,
            "avatar": avatar,
            "llm": llm,
            "prompt": prompt,
        }
        payload = self._normalize_request(payload)
        if not payload:
            raise ValueError("No fields provided to update.")

        url = f"/chats/{chat_id}"
        resp = await self._client.put(url, json=payload)
        self._handle_response(resp, require_data=False)

    async def delete_chats(
            self,
            ids: Optional[str | List[str]] = None,
    ) -> None:
        """
        Delete chat assistants by ID. If ids is None, all chats are deleted.
        """
        ids = normalize_ids(ids, "ids")
        payload: Dict[str, Any] = {"ids": ids}
        payload = self._normalize_request(payload)
        resp = await self._client.delete("/chats", json=payload)
        self._handle_response(resp, require_data=False)

    async def list_chats(
            self,
            *,
            page: int = 1,
            page_size: int = 30,
            orderby: str = "create_time",
            desc: bool = True,
            chat_id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> Tuple[List[ChatAssistant], int]:
        """
        List chat assistants with optional filters.
        Returns a tuple (list_of_chats, total_count)
        """
        params: Dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            "orderby": orderby,
            "desc": desc,
            "id": chat_id,
            "name": name,
        }
        params = self._normalize_request(params)
        resp = await self._client.get("/chats", params=params)
        data = self._handle_response(resp).get("data", [])
        chats = [ChatAssistant.from_raw(item) for item in data]
        total = len(chats)
        return chats, total

    async def create_session(
            self,
            chat_id: str,
            *,
            name: Optional[str] = None,
            user_id: Optional[str] = None,
    ) -> ChatSession:
        """
        Create a new session under a chat assistant.
        """
        return await super().create_session(
            parent_id=chat_id,
            name=name,
            user_id=user_id
        )

    async def list_sessions(
            self,
            chat_id: str,
            *,
            page: int = 1,
            page_size: int = 30,
            orderby: str = "create_time",
            desc: bool = True,
            name: Optional[str] = None,
            session_id: Optional[str] = None,
            user_id: Optional[str] = None,
    ) -> Tuple[List[ChatSession], int]:
        """
        List sessions for a chat assistant.
        """
        return await super().list_sessions(
            parent_id=chat_id,
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
            chat_id: str,
            session_id: str,
            *,
            name: Optional[str] = None,
            user_id: Optional[str] = None,
    ) -> None:
        """
        Update a chat session.
        """
        await super().update_session(
            parent_id=chat_id,
            session_id=session_id,
            name=name,
            user_id=user_id
        )

    async def delete_sessions(
            self,
            chat_id: str,
            session_ids: Optional[str | List[str]] = None,
    ) -> None:
        """
        Delete one or more chat sessions.
        """
        await super().delete_sessions(
            parent_id=chat_id,
            session_ids=session_ids
        )

    async def ask(
            self,
            chat_id: str,  # 替换 parent_id
            session_id: str,
            prompt: str,
            *,
            stream: bool = False,
            **kwargs,
    ) -> AsyncGenerator[ChatCompletionResult, None] | ChatCompletionResult:
        return await super().ask(
            parent_id=chat_id,
            session_id=session_id,
            prompt=prompt,
            session_type="chats",
            stream=stream,
            **kwargs
        )
