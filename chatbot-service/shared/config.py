from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    ollama_host: str
    ollama_model: str

    api_title: str
    api_version: str
    api_host: str
    api_port: int
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()