from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Any, Self

from ..models.base import BaseEntity

__all__ = [
    "Dataset",
    "KnowledgeGraph"
]


@dataclass(slots=True)
class Dataset(BaseEntity):
    """
    Dataset model for RAGFlow.
    """
    id: str
    name: str
    status: str
    permission: str
    document_count: Optional[int] = None
    chunk_count: Optional[int] = None
    token_num: Optional[int] = None

    create_time: Optional[int] = None
    create_date: Optional[str] = None
    update_time: Optional[int] = None
    update_date: Optional[str] = None

    avatar: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    embedding_model: Optional[str] = None
    chunk_method: Optional[str] = None

    __export_fields__ = (
        "id",
        "name",
        "status",
        "permission",
        "document_count",
        "chunk_count",
        "token_num",
        "create_time",
        "create_date",
        "update_time",
        "update_date",
        "avatar",
        "description",
        "language",
        "embedding_model",
        "chunk_method",
    )


@dataclass(slots=True)
class KGNode(BaseEntity):
    id: str
    entity_name: str
    entity_type: str

    description: Optional[str] = None
    pagerank: Optional[float] = None
    source_id: list[str] = field(default_factory=list)

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
    keywords: list[str] = field(default_factory=list)
    weight: Optional[float] = None
    source_id: list[str] = field(default_factory=list)

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
    nodes: list[KGNode]
    edges: list[KGEdge]

    directed: bool = False
    multigraph: bool = False
    graph_info: dict[str, Any] = field(default_factory=dict)
    mind_map: dict[str, Any] = field(default_factory=dict)

    __export_fields__ = (
        "nodes",
        "edges",
        "directed",
        "multigraph",
        "graph_info",
        "mind_map"
    )

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> Self:
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
