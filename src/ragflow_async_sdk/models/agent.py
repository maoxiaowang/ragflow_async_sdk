# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Self

from .base import BaseEntity


@dataclass(slots=True)
class Agent(BaseEntity):
    """
    Agent model.
    """

    __export_fields__ = (
        "id",
        "title",
        "description",
        "avatar",
        "dsl",
        "canvas_category",
        "canvas_type",
        "create_date",
        "create_time",
        "update_date",
        "update_time",
        "user_id",
    )

    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[str] = None

    dsl: Optional[dict[str, Any]] = None
    canvas_category: Optional[str] = None
    canvas_type: Optional[str] = None

    create_date: Optional[str] = None
    create_time: Optional[int] = None
    update_date: Optional[str] = None
    update_time: Optional[int] = None

    user_id: Optional[str] = None


@dataclass
class AgentStep(BaseEntity):
    """
    One reasoning or execution step of an agent.
    """
    role: Optional[str] = None  # system / agent / tool
    content: Optional[str] = None
    tool_name: Optional[str] = None
    tool_input: Optional[dict[str, Any]] = None
    tool_output: Optional[Any] = None


@dataclass
class AgentCompletionResult(BaseEntity):
    """
    Result returned by agent completion API.
    """
    id: Optional[str] = None
    answer: Optional[str] = None

    steps: Optional[list[AgentStep]] = None
    usage: Optional[dict[str, Any]] = None

    create_time: Optional[int] = None

    __export_fields__ = (
        "id",
        "answer",
        "steps",
        "create_time",
    )

    @classmethod
    def from_raw(cls, raw: dict) -> Self:
        obj = super().from_raw(raw)

        if obj.steps:
            obj.steps = [AgentStep.from_raw(step) for step in obj.steps]

        return obj
