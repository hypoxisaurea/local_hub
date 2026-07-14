from app.chatbot.graph.state import RouteName
from app.chatbot.services.local_search import detect_categories, has_local_intent


GENERAL_HINTS = {"왜", "방법", "어떻게", "팁", "추천 이유", "일반", "계획", "일정 짜", "동선"}
COMMUNITY_HINTS = {"게시글", "커뮤니티", "후기", "리뷰", "글 검색", "작성글"}


def classify_route(message: str) -> RouteName:
    if any(keyword in message for keyword in COMMUNITY_HINTS):
        return "community"

    local = has_local_intent(message)
    categories = detect_categories(message)
    general = any(keyword in message for keyword in GENERAL_HINTS)

    if local and (general or len(categories) > 1):
        return "local_plus_general"
    if local:
        return "local"
    return "general"


def next_node_for_route(state: dict) -> str:
    route = state.get("route", "general")
    if route in {"local", "local_plus_general"}:
        return "retrieve_local"
    if route == "community":
        return "retrieve_community"
    return "generate_answer"
