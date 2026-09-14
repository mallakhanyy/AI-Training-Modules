from ollama import Client

from core.interfaces.llm_service import LLMService
from shared.config import settings


class OllamaLLMService(LLMService):

    def __init__(self):
        self.client = Client(host=settings.ollama_host)

    def generate(self, messages: list[dict[str, str]]) -> str:
        response = self.client.chat(
            model=settings.ollama_model,
            messages=messages,
        )

        return response["message"]["content"]