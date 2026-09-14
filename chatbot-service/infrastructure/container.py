from application.services.chat_service import ChatService
from infrastructure.llm.ollama_llm_service import OllamaLLMService
from infrastructure.repositories.in_memory_conversation_repository import (
    InMemoryConversationRepository,
)


def create_chat_service() -> ChatService:
    llm_service = OllamaLLMService()
    conversation_repository = InMemoryConversationRepository()

    return ChatService(
        llm_service=llm_service,
        conversation_repository=conversation_repository,
    )