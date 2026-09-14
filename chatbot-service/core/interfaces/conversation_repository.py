from abc import ABC, abstractmethod
from core.entities.conversation import Conversation

class ConversationRepository(ABC):

    @abstractmethod
    def get(self, conversation_id: str) -> Conversation | None:
        pass

    def save(self, conversation: Conversation) -> None:
        pass
