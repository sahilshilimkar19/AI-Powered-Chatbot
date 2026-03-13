from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Provider: "groq" (free), "gemini" (free), or "openai" (paid)
    llm_provider: str = "groq"

    # Groq (free) - https://console.groq.com/keys
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Google Gemini (free) - https://aistudio.google.com/apikey
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    # OpenAI (paid) - https://platform.openai.com/api-keys
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"

    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def active_api_key(self) -> str:
        return {
            "groq": self.groq_api_key,
            "gemini": self.gemini_api_key,
            "openai": self.openai_api_key,
        }.get(self.llm_provider, "")

    @property
    def active_model(self) -> str:
        return {
            "groq": self.groq_model,
            "gemini": self.gemini_model,
            "openai": self.openai_model,
        }.get(self.llm_provider, "")

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
