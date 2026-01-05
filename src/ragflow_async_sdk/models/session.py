from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .base import BaseEntity


@dataclass
class Message:
    """
    A message in a session.
    """
    role: str
    content: str
    reference: Optional[Dict[str, Any]] = None
    prompt: Optional[str] = None
    id: Optional[str] = None


@dataclass
class BaseSession(BaseEntity):
    """
    Base session model, shared by chat and agent sessions.
    """
    id: str
    name: Optional[str] = None
    user_id: Optional[str] = None
    messages: List[Dict[str, Any]] = field(default_factory=list)
    create_time: Optional[int] = None
    update_time: Optional[int] = None


@dataclass
class ChatSession(BaseSession):
    """
    Chat session model.
    """
    chat_id: Optional[str] = None


@dataclass
class AgentSession(BaseSession):
    """
    Agent session model.
    """
    agent_id: Optional[str] = None
