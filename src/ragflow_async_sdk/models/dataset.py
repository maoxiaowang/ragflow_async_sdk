from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict

from ..models.base import BaseEntity

__all__ = [
    "Dataset",
    "KnowledgeGraph"
]


@dataclass(slots=True)
class Dataset(BaseEntity):
    id: str
    name: str
    permission: str
    status: str

    description: Optional[str] = None
    avatar: Optional[str] = None
    language: Optional[str] = None

    document_count: Optional[int] = None
    chunk_count: Optional[int] = None
    token_num: Optional[int] = None

    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    __export_fields__ = (
        "id",
        "name",
        "permission",
        "status",
        "description",
        "avatar",
        "language",
        "document_count",
        "chunk_count",
        "token_num",
        "created_at",
        "updated_at",
    )


@dataclass(slots=True)
class KGNode(BaseEntity):
    id: str
    entity_name: str
    entity_type: str

    description: Optional[str] = None
    pagerank: Optional[float] = None
    source_id: List[str] = field(default_factory=list)

    __export_fields__ = (
        "id",
        "entity_name",
        "entity_type",
        "description",
        "pagerank",
        "source_id"
    )


@dataclass(slots=True)
class KGEdge(BaseEntity):
    src_id: str
    tgt_id: str
    source: str
    target: str

    description: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    weight: Optional[float] = None
    source_id: List[str] = field(default_factory=list)

    __export_fields__ = (
        "src_id",
        "tgt_id",
        "source",
        "target",
        "description",
        "keywords",
        "weight",
        "source_id"
    )


@dataclass(slots=True)
class KnowledgeGraph(BaseEntity):
    nodes: List[KGNode]
    edges: List[KGEdge]

    directed: bool = False
    multigraph: bool = False
    graph_info: Dict[str, Any] = field(default_factory=dict)
    mind_map: Dict[str, Any] = field(default_factory=dict)

    __export_fields__ = (
        "nodes",
        "edges",
        "directed",
        "multigraph",
        "graph_info",
        "mind_map"
    )

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> "KnowledgeGraph":
        data = raw.get("graph", {})
        nodes = [KGNode.from_raw(n) for n in data.get("nodes", [])]
        edges = [KGEdge.from_raw(e) for e in data.get("edges", [])]
        kg = cls(
            nodes=nodes,
            edges=edges,
            directed=data.get("directed", False),
            multigraph=data.get("multigraph", False),
            graph_info=data.get("graph", {}),
            mind_map=raw.get("mind_map", {}),
        )
        kg._raw = raw
        return kg
