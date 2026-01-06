from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseEntity


@dataclass
class BaseSession(BaseEntity):
    """
    Base session model, shared by chat and agent sessions.
    """
    id: str
    name: Optional[str] = None
    user_id: Optional[str] = None
    messages: list[dict[str, Any]] = field(default_factory=list)
    create_time: Optional[int] = None
    update_time: Optional[int] = None

    __export_fields__ = (
        "id",
        "name",
        "user_id",
        "create_time",
        "update_time",
    )


@dataclass
class ChatSession(BaseSession):
    """
    Chat session model.
    """
    chat_id: Optional[str] = None

    __export_fields__ = BaseSession.__export_fields__ + ("chat_id",)


@dataclass
class AgentSession(BaseSession):
    """
    Agent session model.
    """
    agent_id: Optional[str] = None

    __export_fields__ = BaseSession.__export_fields__ + ("agent_id",)
