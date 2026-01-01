from typing import TypedDict


class ListFilter(TypedDict):
    page: int
    page_size: int
    orderBy: str
    desc: bool


class DatasetFilter(ListFilter):
    id: int
    name: str



def make_filters(**kwargs)