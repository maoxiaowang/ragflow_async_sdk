import uuid
from typing import List, TypeVar

from ragflow_async_sdk.models import (
    Dataset, Document, ChatCompletionResult, Agent, AgentCompletionResult, Chunk,
    ChatAssistant
)
from ragflow_async_sdk.models.session import ChatSession, AgentSession
from ragflow_async_sdk.types import Permission, DocumentStatus
from ragflow_async_sdk.utils.validators import validate_file_tuples, resolve_unique_field

T = TypeVar('T')


class MockRAGFlowClient:
    """Fully mocked AsyncRAGFlowClient for testing SDK, returns Entity objects"""

    def __init__(self):
        # Datasets
        self.datasets = self.Datasets()
        # Documents
        self.documents = self.Documents()
        # Chunks
        self.chunks = self.Chunks()
        # Chats
        self.chats = self.Chats()
        # Agents
        self.agents = self.Agents()

    async def close(self):
        pass

    class BaseMixin:

        @staticmethod
        def _new_id():
            return uuid.uuid4().hex

        def _new_name(self):
            name = f"{self.__class__.__name__.lower()}_{self._new_id()[:4]}"
            return name

    class Datasets(BaseMixin):

        @staticmethod
        def _build_dataset(dataset_id, name, *, status=DocumentStatus.DONE.value, permission=Permission.ME.value,
                           **kwargs):
            return Dataset(dataset_id, name, status, permission, **kwargs)

        async def list_datasets(self) -> tuple[List[Dataset], int]:
            datasets = [
                self._build_dataset(self._new_id(), name=self._new_name()),
                self._build_dataset(self._new_id(), name=self._new_name()),
            ]
            return datasets, len(datasets)

        async def get_dataset(self, dataset_id=None, name=None) -> Dataset:
            resolve_unique_field(dataset_id=dataset_id, name=name)
            data = {"status": "1", "permission": Permission.ME.value}
            if dataset_id:
                data["id"] = dataset_id
                data["name"] = self._new_name()
            else:
                data["id"] = self._new_id()
                data["name"] = name
            return Dataset(**data)

        async def create_dataset(self, name: str, **kwargs) -> Dataset:
            return self._build_dataset(self._new_id(), name, **kwargs)

        @staticmethod
        async def update_dataset(dataset_id: str, **kwargs) -> None:
            return None

        @staticmethod
        async def delete_datasets(ids: list[str]) -> None:
            return None

    class Documents(BaseMixin):

        @staticmethod
        def _build_document(document_id, dataset_id, name, type_, location, **kwargs):
            return Document(
                id=document_id, dataset_id=dataset_id, name=name, type=type_, location=location, **kwargs
            )

        async def list_documents(self, dataset_id: str) -> tuple[List[Document], int]:
            docs = [
                self._build_document(self._new_id(), dataset_id, name="doc1.doc", type_="doc",
                                     location="doc1.doc"),
                self._build_document(self._new_id(), dataset_id, name="doc2.pdf", type_="pdf",
                                     location="doc2.pdf"),
            ]
            return docs, len(docs)

        async def upload_documents(self, dataset_id: str, files: list[tuple[str, bytes, str]]) -> tuple[
            List[Document], int]:
            validate_file_tuples(files)
            docs = [Document(id=self._new_id(), name=f[0], dataset_id=dataset_id, type="doc", location=f[0]) for f
                    in files]
            return docs, len(docs)

    class Chunks(BaseMixin):

        def _build_chunk(self, chunk_id=None, dataset_id=None, document_id=None, content="mock chunk"):
            if chunk_id is None:
                chunk_id = self._new_id()
            if dataset_id is None:
                dataset_id = self._new_id()
            if document_id is None:
                document_id = self._new_id()
            return Chunk(id=chunk_id, dataset_id=dataset_id, document_id=document_id, content=content)

        async def list_chunks(self, dataset_id: str) -> tuple[List[Chunk], int]:
            chunks = [self._build_chunk()]
            return chunks, len(chunks)

    class Chats(BaseMixin):
        def _build_chat(self, chat_id=None, name=None):
            if chat_id is None:
                chat_id = self._new_id()
            if name is None:
                name = self._new_name()
            return ChatAssistant(chat_id, name)

        def _build_chat_session(self, session_id=None, chat_id=None):
            if chat_id is None:
                chat_id = self._new_id()
            if session_id is None:
                session_id = self._new_id()
            return ChatSession(id=session_id, chat_id=chat_id)

        async def create_chat(self, name: str) -> ChatAssistant:
            return self._build_chat(name=name)

        async def create_session(self, chat_id: str) -> ChatSession:
            return self._build_chat_session(chat_id=chat_id)

        def ask_stream(self, chat_id: str, session_id: str, prompt: str):
            async def _gen():
                yield ChatCompletionResult(answer="Hello from mock!")
            return _gen()

        async def ask(self, chat_id: str, session_id: str, prompt: str):
            return ChatCompletionResult(answer="Hello from mock!", session_id=session_id)

    class Agents(BaseMixin):

        def _build_agent(self, agent_id=None, title=None, dsl=None):
            if title is None:
                title = self._new_name()
            if dsl is None:
                dsl = list()
            return Agent(id=agent_id, title=title, dsl=dsl)

        def _build_agent_session(self, agent_id=None, session_id=None, name=None):
            if agent_id is None:
                agent_id = self._new_id()
            if name is None:
                name = self._new_name()
            return AgentSession(id=session_id, agent_id=agent_id, name=name)

        async def list_agents(self) -> tuple[List[Agent], int]:
            agents = [self._build_agent()]
            return agents, len(agents)

        async def create_agent(self, title: str) -> Agent:
            return self._build_agent(title=title)

        async def create_session(self, agent_id: str) -> AgentSession:
            return self._build_agent_session(agent_id=agent_id)

        def ask_stream(self, agent_id: str, session_id: str, prompt: str):
            async def _gen():
                yield AgentCompletionResult(
                    id="assistant", answer="Hello from mock!"
                )
            return _gen()

        async def ask(self, chat_id, session_id, prompt):
            return AgentCompletionResult(id="assistant", answer="Hello from mock!")
