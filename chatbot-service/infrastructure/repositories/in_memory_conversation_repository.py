from core.entities.conversation import Conversation
from core.interfaces.conversation_repository import ConversationRepository


class InMemoryConversationRepository(ConversationRepository):

    def __init__(self):
        self._conversations: dict[str, Conversation] = {}

    def get(self, conversation_id: str) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def save(self, conversation: Conversation) -> None:
        self._conversations[conversation.conversation_id] = conversation