from datetime import datetime

from core.entities.conversation import Conversation
from infrastructure.repositories.in_memory_conversation_repository import (
    InMemoryConversationRepository,
)


def test_save_and_get_conversation():
    repository = InMemoryConversationRepository()

    conversation = Conversation(
        conversation_id="conversation-1",
        messages=[],
        created_at=datetime.now(),
    )

    repository.save(conversation)

    result = repository.get("conversation-1")

    assert result is conversation
    assert result.conversation_id == "conversation-1"


def test_get_non_existing_conversation():
    repository = InMemoryConversationRepository()

    result = repository.get("does-not-exist")

    assert result is None