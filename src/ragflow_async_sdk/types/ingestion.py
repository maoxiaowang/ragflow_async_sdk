from enum import Enum
from typing import TypedDict, List


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


class RaptorConfig(TypedDict, total=False):
    use_raptor: bool


class GraphRagConfig(TypedDict, total=False):
    use_graphrag: bool


class NaiveParserConfig(TypedDict, total=False):
    auto_keywords: int
    auto_questions: int
    chunk_token_num: int
    delimiter: str
    html4excel: bool
    layout_recognize: str
    tag_kb_ids: List[str]
    task_page_size: int
    raptor: RaptorConfig
    graphrag: GraphRagConfig


class SimpleParserConfig(TypedDict, total=False):
    raptor: RaptorConfig


class OrderBy(str, Enum):
    CREATE_TIME = "create_time"
    UPDATE_TIME = "update_time"
