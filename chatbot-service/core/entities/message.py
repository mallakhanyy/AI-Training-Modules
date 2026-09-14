from dataclasses import dataclass
from core.enums.role import Role
from datetime import datetime


@dataclass
class Message:
    message_id: str
    conversation_id: str
    role: Role
    content: str
    created_at: datetime