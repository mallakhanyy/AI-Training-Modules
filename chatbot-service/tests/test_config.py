from shared.config import settings


def test_settings():

    assert settings.ollama_host == "http://localhost:11434"

    assert settings.ollama_model == "qwen3:1.7b"