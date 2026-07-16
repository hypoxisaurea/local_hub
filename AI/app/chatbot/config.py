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
        validation_alias=AliasChoices(
            "OPENAI_API_KEY",
            "OPEN_AI_API_KEY",
            "CHATBOT_OPENAI_API_KEY",
            "CHATBOT_OPEN_AI_API_KEY",
        ),
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        validation_alias=AliasChoices(
            "OPENAI_MODEL",
            "OPEN_AI_MODEL",
            "CHATBOT_OPENAI_MODEL",
            "CHATBOT_OPEN_AI_MODEL",
        ),
    )
    temperature: float = Field(
        default=0.2,
        validation_alias=AliasChoices(
            "OPENAI_TEMPERATURE",
            "CHATBOT_TEMPERATURE",
        ),
    )
    data_dir: Path = Field(
        default=PROJECT_DIR / "data",
        validation_alias=AliasChoices(
            "DATA_DIR",
            "CHATBOT_DATA_DIR",
        ),
    )
    max_context_items: int = Field(
        default=8,
        validation_alias=AliasChoices(
            "MAX_CONTEXT_ITEMS",
            "CHATBOT_MAX_CONTEXT_ITEMS",
        ),
    )
    max_search_results: int = Field(
        default=5,
        validation_alias=AliasChoices(
            "MAX_SEARCH_RESULTS",
            "CHATBOT_MAX_SEARCH_RESULTS",
        ),
    )

    model_config = SettingsConfigDict(
        env_file=(
            PROJECT_DIR / ".env",
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
