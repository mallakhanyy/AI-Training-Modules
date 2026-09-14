from abc import ABC, abstractmethod

class LLMService(ABC):

    @abstractmethod
    def generate(self, messages: list[dict[str:str]]) -> str:
        pass