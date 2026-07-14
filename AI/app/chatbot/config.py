from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


CHATBOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CHATBOT_DIR.parents[1]
PROJECT_DIR = BACKEND_DIR.parent


class ChatbotSettings(BaseSettings):
    openai_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("OPENAI_API_KEY", "CHATBOT_OPENAI_API_KEY"),
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        validation_alias=AliasChoices("OPENAI_MODEL", "CHATBOT_OPENAI_MODEL"),
    )
    temperature: float = 0.2
    data_dir: Path = PROJECT_DIR / "data"
    max_search_results: int = 6
    max_context_items: int = 8

    model_config = SettingsConfigDict(
        env_file=(
            BACKEND_DIR / ".env",
            CHATBOT_DIR / "api" / ".env",
        ),
        env_file_encoding="utf-8",
        env_prefix="CHATBOT_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> ChatbotSettings:
    return ChatbotSettings()
