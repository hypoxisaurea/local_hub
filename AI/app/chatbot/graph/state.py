from typing import Any, Literal, TypedDict


RouteName = Literal["local", "local_plus_general", "community", "general"]


class ChatbotState(TypedDict, total=False):
    message: str
    history: list[Any]
    language: str | None
    route: RouteName
    local_docs: list[dict[str, Any]]
    community_docs: list[dict[str, Any]]
    answer: str
    sources: list[dict[str, Any]]
