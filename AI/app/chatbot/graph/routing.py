from app.chatbot.graph.state import RouteName
from app.chatbot.services.local_search import detect_categories, has_local_intent

GENERAL_HINTS = {"왜", "방법", "어떻게", "팁", "추천 이유", "일반", "계획", "일정 짜", "동선"}
COMMUNITY_HINTS = {"게시글", "커뮤니티", "후기", "리뷰", "글 검색", "작성글"}
COUNT_HINTS = {"개수", "몇", "몇개", "몇 개", "총", "얼마나", "count"}
LIST_HINTS = {"목록", "리스트", "조회", "보여줘"}
DB_HINTS = COUNT_HINTS | LIST_HINTS | {"예약", "사용자"}
DB_TARGET_HINTS = {
    "게시글",
    "숙소",
    "관광",
    "관광지",
    "축제",
    "행사",
    "공연",
    "문화",
    "레포츠",
    "쇼핑",
    "음식점",
    "맛집",
    "여행코스",
    "코스",
    "예약",
    "사용자",
    "댓글",
    "카테고리",
}

def is_db_query(message: str) -> bool:
    lowered = message.lower()
    if not any(keyword in lowered for keyword in DB_HINTS):
        return False
    if detect_categories(message):
        return True
    return any(keyword in lowered for keyword in DB_TARGET_HINTS)

def classify_route(message: str) -> RouteName:
    if is_db_query(message):
        return "db"

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
    if route == "db":
        return "db"
    if route in {"local", "local_plus_general"}:
        return "retrieve_local"
    if route == "community":
        return "retrieve_community"
    return "generate_answer"
