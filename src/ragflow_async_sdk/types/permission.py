from enum import Enum


class Permission(str, Enum):
    ME = "me"
    TEAM = "team"
