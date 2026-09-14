from pydantic import BaseModel


class ChatRequest(BaseModel):

    conversation_id: str

    message: str

    context: str | None = None