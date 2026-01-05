from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any, List, Dict, Self

from .base import BaseEntity
from .dataset import Dataset


@dataclass(slots=True)
class LLMConfig(BaseEntity):
    model_name: Optional[str] = None
    model_type: Optional[str] = "chat"
    temperature: Optional[float] = 0.1
    top_p: Optional[float] = 0.3
    presence_penalty: Optional[float] = 0.4
    frequency_penalty: Optional[float] = 0.7

    __export_fields__ = (
        "model_name",
        "model_type",
        "temperature",
        "top_p",
        "presence_penalty",
        "frequency_penalty",
    )


@dataclass(slots=True)
class PromptConfig(BaseEntity):
    similarity_threshold: Optional[float] = 0.2
    keywords_similarity_weight: Optional[float] = 0.7
    top_n: Optional[int] = 6
    variables: Optional[List[Dict[str, Any]]] = None
    rerank_model: Optional[str] = None
    empty_response: Optional[str] = None
    opener: Optional[str] = None
    show_quote: Optional[bool] = True
    prompt: Optional[str] = None

    __export_fields__ = (
        "similarity_threshold",
        "keywords_similarity_weight",
        "top_n",
        "variables",
        "rerank_model",
        "empty_response",
        "opener",
        "show_quote",
        "prompt",
    )


@dataclass(slots=True)
class ChatAssistant(BaseEntity):
    id: str
    name: str
    avatar: Optional[str] = None
    datasets: Optional[List[str]] = None
    llm: Optional[LLMConfig] = None
    prompt: Optional[PromptConfig] = None
    create_date: Optional[str] = None
    create_time: Optional[int] = None
    update_date: Optional[str] = None
    update_time: Optional[int] = None
    status: Optional[str] = None
    top_k: Optional[int] = 1024
    language: Optional[str] = "English"

    __export_fields__ = (
        "id",
        "name",
        "avatar",
        "dataset_ids",
        "llm",
        "prompt",
        "create_date",
        "create_time",
        "update_date",
        "update_time",
        "status",
        "top_k",
        "language",
    )

    @classmethod
    def from_raw(cls, raw: dict) -> Self:
        obj = super(ChatAssistant, cls).from_raw(raw)

        if isinstance(raw.get("llm"), dict):
            obj.llm = LLMConfig.from_raw(raw["llm"])
        if isinstance(raw.get("prompt"), dict):
            obj.prompt = PromptConfig.from_raw(raw["prompt"])
        if isinstance(raw.get("datasets"), dict):
            obj.datasets = [Dataset.from_raw(d) if isinstance(d, dict) else d for d in raw["datasets"]]
        return obj
