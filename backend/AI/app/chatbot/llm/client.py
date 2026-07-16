from langchain_openai import ChatOpenAI

from ..config import get_settings


def get_chat_model() -> ChatOpenAI | None:
    settings = get_settings()
    if not settings.openai_api_key:
        return None

    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=settings.temperature,
    )
