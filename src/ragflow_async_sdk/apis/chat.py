from typing import Optional, Any, AsyncGenerator

from .base import BaseAPI
from .mixins import SessionMixin
from ..models.chat import ChatAssistant, ChatCompletionResult
from ..models.session import ChatSession
from ..types import OrderBy
from ..utils.normalizers import normalize_ids
from ..utils.validators import require_params


class ChatAPI(SessionMixin[ChatSession], BaseAPI):
    """API for managing chat assistants and their sessions."""

    _parent_type = "chats"
    _session_model = ChatSession

    async def create_chat(
        self,
        name: str,
        *,
        dataset_ids: Optional[list[str]] = None,
        avatar: Optional[str] = None,
        llm: Optional[dict[str, Any]] = None,
        prompt: Optional[dict[str, Any]] = None,
    ) -> ChatAssistant:
        """
        Create a new chat assistant.

        Args:
            name: Chat assistant name.
            dataset_ids: Optional list of dataset IDs to associate.
            avatar: Optional avatar URL.
            llm: Optional LLM configuration.
            prompt: Optional prompt configuration.

        Returns:
            ChatAssistant instance.
        """
        require_params(name=name)
        payload = {
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
        dataset_ids: Optional[list[str]] = None,
        avatar: Optional[str] = None,
        llm: Optional[dict[str, Any]] = None,
        prompt: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Update an existing chat assistant.

        Args:
            chat_id: Chat assistant ID.
            name: Optional new name.
            dataset_ids: Optional updated dataset IDs.
            avatar: Optional updated avatar URL.
            llm: Optional updated LLM configuration.
            prompt: Optional updated prompt configuration.

        Raises:
            ValueError: If no fields are provided for update.
        """
        require_params(chat_id=chat_id)
        payload = {
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

    async def delete_chats(self, ids: Optional[str | list[str]] = None) -> None:
        """
        Delete chat assistants by ID.

        Args:
            ids: Single or list of chat IDs to delete. If None, deletes all chats.
        """
        ids = normalize_ids(ids, "ids")
        payload = {"ids": ids}
        payload = self._normalize_request(payload)
        resp = await self._client.delete("/chats", json=payload)
        self._handle_response(resp, require_data=False)

    async def list_chats(
        self,
        *,
        page: int = 1,
        page_size: int = 30,
        orderby: OrderBy | str = OrderBy.CREATE_TIME,
        desc: bool = True,
        chat_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> tuple[list[ChatAssistant], int]:
        """
        List chat assistants with optional filters.

        Args:
            page: Page number.
            page_size: Number of items per page.
            orderby: Field to sort by.
            desc: Sort descending if True.
            chat_id: Optional filter by chat ID.
            name: Optional filter by chat name.

        Returns:
            Tuple containing a list of ChatAssistant instances and the total count.
        """
        params = {
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
        return chats, len(chats)

    async def create_session(
        self,
        chat_id: str,
        *,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> ChatSession:
        """
        Create a new session under a chat assistant.

        Args:
            chat_id: Chat assistant ID.
            name: Optional session name.
            user_id: Optional user ID.

        Returns:
            ChatSession instance.
        """
        return await super().create_session(parent_id=chat_id, name=name, user_id=user_id)

    async def list_sessions(
        self,
        chat_id: str,
        *,
        page: int = 1,
        page_size: int = 30,
        orderby: OrderBy | str = OrderBy.CREATE_TIME,
        desc: bool = True,
        name: Optional[str] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> tuple[list[ChatSession], int]:
        """
        List sessions for a chat assistant.

        Args:
            chat_id: Chat assistant ID.
            page: Page number.
            page_size: Number of items per page.
            orderby: Field to sort by.
            desc: Sort descending if True.
            name: Optional session name filter.
            session_id: Optional session ID filter.
            user_id: Optional user ID filter.

        Returns:
            Tuple containing a list of ChatSession instances and total count.
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

        Args:
            chat_id: Chat assistant ID.
            session_id: Session ID.
            name: Optional new session name.
            user_id: Optional new user ID.
        """
        await super().update_session(
            parent_id=chat_id, session_id=session_id, name=name, user_id=user_id
        )

    async def delete_sessions(
        self,
        chat_id: str,
        session_ids: Optional[str | list[str]] = None,
    ) -> None:
        """
        Delete one or more chat sessions.

        Args:
            chat_id: Chat assistant ID.
            session_ids: Single or list of session IDs to delete. If None, delete all.
        """
        await super().delete_sessions(parent_id=chat_id, session_ids=session_ids)

    async def ask(
        self,
        chat_id: str,
        session_id: str,
        prompt: str,
        *,
        stream: bool = False,
        **kwargs,
    ) -> AsyncGenerator[ChatCompletionResult, None] | ChatCompletionResult:
        """
        Ask a question in a chat session.

        Args:
            chat_id: Chat assistant ID.
            session_id: Session ID.
            prompt: User question.
            stream: Whether to return streaming results.
            **kwargs: Additional parameters (temperature, top_p, etc.).

        Returns:
            Either a single ChatCompletionResult or an async generator if streaming.
        """
        return await super().ask(
            parent_id=chat_id,
            session_id=session_id,
            prompt=prompt,
            session_type="chats",
            stream=stream,
            **kwargs,
        )