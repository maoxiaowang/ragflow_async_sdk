from enum import Enum


class SessionType(str, Enum):
    CHAT = "chats"
    AGENT = "agents"