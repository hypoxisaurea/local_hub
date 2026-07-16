from typing import Any, Literal, TypedDict

RouteName = Literal["local", "local_plus_general", "community", "general", "db"]

class ChatbotState(TypedDict, total=False):
    message: str
    history: list[Any]
    language: str | None
    route: RouteName

    local_docs: list[dict[str, Any]]
    community_docs: list[dict[str, Any]]

    db_query_sql: str
    db_results: list[dict[str, Any]]
    db_error: str | None

    answer: str
    sources: list[dict[str, Any]]