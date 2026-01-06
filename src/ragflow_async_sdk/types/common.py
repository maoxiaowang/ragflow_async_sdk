from enum import Enum


class OrderBy(str, Enum):
    CREATE_TIME = "create_time"
    UPDATE_TIME = "update_time"
