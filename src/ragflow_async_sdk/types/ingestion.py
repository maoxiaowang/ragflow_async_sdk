from enum import Enum


class ChunkMethod(str, Enum):
    NAIVE = "naive"
    BOOK = "book"
    EMAIL = "email"
    LAWS = "laws"
    MANUAL = "manual"
    ONE = "one"
    PAPER = "paper"
    PICTURE = "picture"
    PRESENTATION = "presentation"
    QA = "qa"
    TABLE = "table"
    TAG = "tag"


class OrderBy(str, Enum):
    CREATE_TIME = "create_time"
    UPDATE_TIME = "update_time"
