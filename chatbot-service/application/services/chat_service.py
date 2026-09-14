from datetime import datetime
from uuid import uuid4

from core.entities.conversation import Conversation
from core.entities.message import Message
from core.enums.role import Role
from core.interfaces.conversation_repository import ConversationRepository
from core.interfaces.llm_service import LLMService
from core.schemas.chat_response import ChatResponse


class ChatService:

    def __init__(
        self,
        llm_service: LLMService,
        conversation_repository: ConversationRepository,
    ):
        self.llm_service = llm_service
        self.conversation_repository = conversation_repository

    def _create_conversation(self, conversation_id: str) -> Conversation:
        return Conversation(
            conversation_id=conversation_id,
            messages=[],
            created_at=datetime.now(),
        )

    def _create_message(
        self,
        conversation_id: str,
        role: Role,
        content: str,
    ) -> Message:
        return Message(
            message_id=str(uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.now(),
        )

    def _build_llm_messages(
        self,
        conversation: Conversation,
        context: str | None = None,
    ) -> list[dict[str, str]]:

        messages = [
            {
                "role": "system",
                "content": (
                    "أنت مساعد ذكي للمستخدم وتجيب دائمًا باللغة العربية. "
                    "استخدم سجل المحادثة السابق لفهم سياق الحديث والإجابة عن أسئلة المستخدم. "
                    "إذا ذكر المستخدم معلومة عن نفسه، مثل اسمه، فتذكرها واستخدمها عند الحاجة. "
                    "لا تقل إنك لا تعرف معلومة سبق أن ذكرها المستخدم في المحادثة. "
                    "كن واضحًا ومباشرًا ومختصرًا. "
                    "لا تخترع معلومات غير موجودة في المحادثة أو في السياق المقدم لك."
                ),
            }
        ]

        if context:
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "لديك المعلومات التالية من خدمة أخرى في النظام. "
                        "استخدمها كمرجع عند الإجابة على المستخدم، "
                        "ولا تخترع معلومات غير موجودة فيها:\n\n"
                        f"{context}"
                    ),
                }
            )

        messages.extend(
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in conversation.messages
        )

        return messages

    def chat(
        self,
        conversation_id: str,
        message: str,
        context: str | None = None,
    ) -> ChatResponse:

        conversation = self.conversation_repository.get(conversation_id)

        if conversation is None:
            conversation = self._create_conversation(conversation_id)

        user_message = self._create_message(
            conversation_id=conversation_id,
            role=Role.USER,
            content=message,
        )

        conversation.messages.append(user_message)

        llm_messages = self._build_llm_messages(
            conversation=conversation,
            context=context,
        )

        assistant_response = self.llm_service.generate(
            llm_messages
        )

        assistant_message = self._create_message(
            conversation_id=conversation_id,
            role=Role.ASSISTANT,
            content=assistant_response,
        )

        conversation.messages.append(assistant_message)

        self.conversation_repository.save(conversation)

        return ChatResponse(
            conversation_id=conversation_id,
            message=assistant_response,
        )