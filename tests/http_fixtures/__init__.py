from .datasets import register_dataset_routes
from .documents import register_document_routes
from .agents import register_agent_routes
from .chunks import register_chunk_routes

__all__ = [
    "register_all_routes",
]


def register_all_routes(fake_httpx):
    register_dataset_routes(fake_httpx)
    register_document_routes(fake_httpx)
    register_agent_routes(fake_httpx)
    register_chunk_routes(fake_httpx)