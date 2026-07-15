import re
from collections import Counter
from typing import Any

from app.chatbot.config import get_settings
from app.chatbot.services.data_loader import load_local_documents


CATEGORY_KEYWORDS = {
    "관광지": {
        "관광",
        "명소",
        "가볼만",
        "갈만",
        "추천",
        "공원",
        "궁",
        "거리",
        "한강",
        "tour",
        "tourist",
        "attraction",
        "place",
        "places",
        "sightseeing",
        "landmark",
    },
    "축제공연행사": {
        "축제",
        "행사",
        "공연",
        "일정",
        "페스티벌",
        "전시",
        "이벤트",
        "festival",
        "festivals",
        "event",
        "events",
        "performance",
        "concert",
        "exhibition",
        "show",
        "october",
        "november",
        "december",
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
    },
    "숙박": {"숙박", "호텔", "게스트하우스", "숙소", "잠", "묵", "hotel", "stay", "lodging", "accommodation"},
    "쇼핑": {"쇼핑", "시장", "상가", "몰", "백화점", "기념품", "shopping", "market", "mall", "store"},
    "문화시설": {
        "문화",
        "박물관",
        "미술관",
        "도서관",
        "공연장",
        "전시관",
        "culture",
        "museum",
        "gallery",
        "library",
    },
    "레포츠": {"레포츠", "스포츠", "체험", "운동", "자전거", "클라이밍", "sports", "activity", "activities"},
    "여행코스": {"코스", "일정", "루트", "여행 계획", "동선", "course", "route", "itinerary", "plan"},
    "음식점": {"음식점", "식당", "맛집", "모범음식점", "먹거리", "카페", "restaurant", "food", "cafe"},
}

SEOUL_DISTRICTS = {
    "강남구",
    "강동구",
    "강북구",
    "강서구",
    "관악구",
    "광진구",
    "구로구",
    "금천구",
    "노원구",
    "도봉구",
    "동대문구",
    "동작구",
    "마포구",
    "서대문구",
    "서초구",
    "성동구",
    "성북구",
    "송파구",
    "양천구",
    "영등포구",
    "용산구",
    "은평구",
    "종로구",
    "중구",
    "중랑구",
}

TOKEN_RE = re.compile(r"[0-9A-Za-z가-힣]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text or "") if len(token) > 1]


def detect_categories(message: str) -> set[str]:
    lowered = message.lower()
    categories: set[str] = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            categories.add(category)
    return categories


def detect_districts(message: str) -> set[str]:
    return {district for district in SEOUL_DISTRICTS if district in message}


def search_local_data(message: str, limit: int | None = None) -> list[dict[str, Any]]:
    settings = get_settings()
    limit = limit or settings.max_search_results
    tokens = tokenize(message)
    token_counts = Counter(tokens)
    categories = detect_categories(message)
    districts = detect_districts(message)

    scored: list[tuple[float, dict[str, Any]]] = []
    for doc in load_local_documents():
        haystack = " ".join(
            [
                doc["title"],
                doc["address"],
                doc["content_type"],
                doc.get("tel", ""),
            ]
        ).lower()

        score = 0.0
        for token, count in token_counts.items():
            if token in haystack:
                score += 2.5 * count if token in doc["title"].lower() else 1.0 * count

        if categories:
            if doc["content_type"] in categories:
                score += 4.0
            else:
                score -= 1.0

        if districts:
            if any(district in doc["address"] for district in districts):
                score += 5.0
            else:
                score -= 0.5

        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:limit]]


def has_local_intent(message: str) -> bool:
    lowered = message.lower()
    local_words = {
        "서울",
        "seoul",
        "near",
        "nearby",
        "area",
        "address",
        "location",
        "phone",
        "recommend",
        "tour",
        "stay",
        "festival",
        "event",
        "shopping",
        "culture",
        "food",
        "restaurant",
    }
    return bool(detect_categories(message) or detect_districts(message) or any(word in lowered for word in local_words))
