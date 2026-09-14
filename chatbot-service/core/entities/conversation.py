from dataclasses import dataclass
from core.entities.message import Message

@dataclass
class Conversation:
    conversation_id: str
    messages:  list[Message]
    created_at: str