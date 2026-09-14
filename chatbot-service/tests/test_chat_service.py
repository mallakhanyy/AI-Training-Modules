from application.services.chat_service import ChatService
from core.interfaces.llm_service import LLMService
from infrastructure.repositories.in_memory_conversation_repository import (
    InMemoryConversationRepository,
)


class FakeLLMService(LLMService):

    def __init__(self):
        self.messages = None

    def generate(self, messages: list[dict[str, str]]) -> str:
        self.messages = messages
        return "مرحبًا! كيف يمكنني مساعدتك؟"


def test_chat_creates_conversation_and_returns_response():

    repository = InMemoryConversationRepository()

    chat_service = ChatService(
        llm_service=FakeLLMService(),
        conversation_repository=repository,
    )

    response = chat_service.chat(
        conversation_id="conversation-1",
        message="مرحبًا",
    )

    assert response.conversation_id == "conversation-1"
    assert response.message == "مرحبًا! كيف يمكنني مساعدتك؟"


def test_chat_saves_conversation_history():

    repository = InMemoryConversationRepository()

    chat_service = ChatService(
        llm_service=FakeLLMService(),
        conversation_repository=repository,
    )

    chat_service.chat(
        conversation_id="conversation-1",
        message="مرحبًا",
    )

    conversation = repository.get("conversation-1")

    assert conversation is not None
    assert len(conversation.messages) == 2
    assert conversation.messages[0].content == "مرحبًا"
    assert conversation.messages[1].content == "مرحبًا! كيف يمكنني مساعدتك؟"


def test_chat_includes_conversation_history():

    repository = InMemoryConversationRepository()
    llm_service = FakeLLMService()

    chat_service = ChatService(
        llm_service=llm_service,
        conversation_repository=repository,
    )

    chat_service.chat(
        conversation_id="conversation-3",
        message="المحاصيل عندي جافة.",
    )

    chat_service.chat(
        conversation_id="conversation-3",
        message="ماذا لو استخدمت الري بالتنقيط؟",
    )

    assert llm_service.messages is not None

    contents = [
        message["content"]
        for message in llm_service.messages
    ]

    assert "المحاصيل عندي جافة." in contents
    assert "ماذا لو استخدمت الري بالتنقيط؟" in contents


def test_chat_uses_context():

    repository = InMemoryConversationRepository()
    llm_service = FakeLLMService()

    chat_service = ChatService(
        llm_service=llm_service,
        conversation_repository=repository,
    )

    context = (
        "المشكلة: المحاصيل لا تحصل على كمية كافية من المياه.\n"
        "التوصية: زيادة معدل تكرار الري.\n"
        "السبب: قد تعاني المحاصيل من نقص المياه."
    )

    chat_service.chat(
        conversation_id="conversation-4",
        message="لماذا هذه التوصية؟",
        context=context,
    )

    assert llm_service.messages is not None

    contents = [
        message["content"]
        for message in llm_service.messages
    ]

    assert any(context in content for content in contents)