# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from enum import Enum


class SessionType(str, Enum):
    CHAT = "chats"
    AGENT = "agents"