# import pytest
#
# from ragflow_async_sdk.models import ChatAssistant, ChatCompletionResult
#
#
# @pytest.mark.asyncio
# async def test_create_chat(client):
#     chat = await client.chats.create_chat("domo-chat")
#     assert isinstance(chat, ChatAssistant)
#     assert chat.name == "domo-chat"
#
# @pytest.mark.asyncio
# async def test_chat_ask(client):
#     chat = await client.chats.create_chat(name="demo-chat")
#     session = await client.chats.create_session(chat.id)
#     result = await client.chats.ask(chat.id, session.id, "Hello")
#     assert isinstance(result, ChatCompletionResult)
#     assert result.answer == "Hello from mock!"
#
#
# @pytest.mark.asyncio
# async def test_chat_ask_stream(client):
#     chat = await client.chats.create_chat(name="demo-chat")
#     session = await client.chats.create_session(chat.id)
#     result = client.chats.ask_stream(chat.id, session.id, "Hello")
#     async for chunk in result:
#         assert isinstance(chunk, ChatCompletionResult)
#         assert chunk.answer == "Hello from mock!"
#
