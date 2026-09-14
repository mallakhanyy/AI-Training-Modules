from pydantic import BaseModel


class ChatResponse(BaseModel):
    conversation_id: str
    message: str