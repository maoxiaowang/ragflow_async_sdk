# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from typing import TypedDict, Optional


class Filter(TypedDict):
    page: Optional[int]
    page_size: Optional[int]
    orderby: Optional[str]
    desc: Optional[bool]


class DatasetFilter(Filter):
    id: Optional[int]
    name: Optional[str]


class DocumentFilter(Filter):
    id: Optional[int]
    keywords: Optional[str]
    create_time_from: Optional[int]
    create_time_to: Optional[int]
