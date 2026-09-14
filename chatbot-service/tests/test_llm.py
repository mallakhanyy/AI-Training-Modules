from infrastructure.llm.ollama_llm_service import OllamaLLMService


def test_ollama_llm():
    llm_service = OllamaLLMService()

    messages = [
        {
            "role": "user",
            "content": "Hello, introduce yourself in one short sentence.",
        }
    ]

    response = llm_service.generate(messages)

    assert isinstance(response, str)
    assert response.strip()