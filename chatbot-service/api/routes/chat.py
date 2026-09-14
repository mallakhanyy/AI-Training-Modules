from fastapi import APIRouter

from application.services.chat_service import ChatService
from core.schemas.chat_request import ChatRequest
from core.schemas.chat_response import ChatResponse
from infrastructure.container import create_chat_service


router = APIRouter()

chat_service: ChatService = create_chat_service()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return chat_service.chat(
        conversation_id=request.conversation_id,
        message=request.message,
        context=request.context,
    )