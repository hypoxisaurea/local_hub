from typing import Any


MONTH_WORDS = {
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
    "1월",
    "2월",
    "3월",
    "4월",
    "5월",
    "6월",
    "7월",
    "8월",
    "9월",
    "10월",
    "11월",
    "12월",
}


def _wants_english(message: str, language: str | None = None) -> bool:
    if language and language.lower().startswith("en"):
        return True
    if language and language.lower().startswith("ko"):
        return False

    letters = [char for char in message if char.isalpha()]
    if not letters:
        return False
    ascii_letters = [char for char in letters if char.isascii()]
    return len(ascii_letters) / len(letters) > 0.8


def _asks_for_month(message: str) -> bool:
    lowered = message.lower()
    return any(month in lowered for month in MONTH_WORDS)


def source_from_document(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": doc.get("content_type", ""),
        "title": doc.get("title", ""),
        "address": doc.get("address") or None,
        "tel": doc.get("tel") or None,
        "image": doc.get("image") or None,
        "mapx": doc.get("mapx") or None,
        "mapy": doc.get("mapy") or None,
        "contentid": doc.get("contentid") or None,
        "extra": {
            "source_file": doc.get("source_file"),
            "modifiedtime": doc.get("modifiedtime"),
        },
    }


def format_context(docs: list[dict[str, Any]]) -> str:
    if not docs:
        return "No matching local data candidates."

    lines: list[str] = []
    for index, doc in enumerate(docs, start=1):
        parts = [
            f"{index}. [{doc.get('content_type')}] {doc.get('title')}",
            f"Address: {doc.get('address') or 'Not provided'}",
        ]
        if doc.get("tel"):
            parts.append(f"Phone: {doc['tel']}")
        if doc.get("mapx") and doc.get("mapy"):
            parts.append(f"Coordinates: {doc['mapy']}, {doc['mapx']}")
        lines.append(" / ".join(parts))
    return "\n".join(lines)

def _friendly_general_reply(message: str, language: str | None = None) -> str | None:
    lowered = message.strip().lower()
    english = _wants_english(message, language)

    greeting_words = {"안녕", "안녕하세요", "반가워", "반갑습니다", "hi", "hello", "hey", "ㅎㅇ"}
    thanks_words = {"감사", "감사합니다", "고마워", "고마워요", "thanks", "thank you"}
    goodbye_words = {"잘가", "잘 가", "bye", "바이", "그만", "종료", "exit", "quit"}

    if any(word in lowered for word in greeting_words):
        if english:
            return "Hello! I can help with Seoul travel recommendations. Tell me a place, district, or activity you want to know about."
        return "안녕하세요! 서울 여행 정보로 도와드릴게요. 궁금한 장소나 지역, 원하는 유형을 말해 주세요."

    if any(word in lowered for word in thanks_words):
        if english:
            return "You’re welcome! If you need anything else, feel free to ask."
        return "천천히 말씀해 주세요. 도움이 필요하시면 언제든지 다시 물어보세요."

    if any(word in lowered for word in goodbye_words):
        if english:
            return "Goodbye! Hope your trip goes well."
        return "좋은 여행 되세요! 궁금한 게 있으면 또 찾아와 주세요."

    return None


def _general_fallback_reply(message: str, language: str | None = None) -> str:
    english = _wants_english(message, language)
    if english:
        return "I'm here with you. Ask me about Seoul places, neighborhoods, food, shopping, festivals, or travel routes whenever you're ready."
    return "편하게 말씀해 주세요. 서울의 장소, 지역, 맛집, 쇼핑, 축제, 여행 코스 중 궁금한 걸 물어보시면 같이 찾아볼게요."

def fallback_answer(
    message: str,
    route: str,
    docs: list[dict[str, Any]],
    language: str | None = None,
) -> str:
    english = _wants_english(message, language)
    asks_for_month = _asks_for_month(message)

    if route in {"general", "local_plus_general"}:
        friendly_reply = _friendly_general_reply(message, language)
        if friendly_reply:
            return friendly_reply

    if not docs:
        if route == "general":
            return _general_fallback_reply(message, language)
        if route == "community":
            if english:
                return "Community post search needs a posts database connection. The chatbot node is ready, but no DB search is connected yet."
            return "커뮤니티 게시글 검색은 아직 게시글 DB 연결이 필요합니다. 챗봇 모듈에는 검색 노드와 연결 지점만 준비되어 있어요."
        if english:
            return "I could not find matching items in the provided Seoul data. Try adding a district, category, or place name."
        return "제공 데이터에서는 질문과 직접 연결되는 항목을 찾지 못했습니다. 지역명이나 원하는 유형을 조금 더 구체적으로 입력해 주세요."

    if english:
        lines = ["Based on the provided Seoul data, I found these related items:"]
        for doc in docs[:5]:
            line = f"- {doc.get('title')} ({doc.get('content_type')})"
            if doc.get("address"):
                line += f": {doc['address']}"
            if doc.get("tel"):
                line += f" / Contact: {doc['tel']}"
            lines.append(line)
        if asks_for_month:
            lines.append("The provided JSON data does not include exact event dates, so I cannot confirm whether these are specifically in that month.")
        elif route == "local_plus_general":
            lines.append("For changing details such as schedules or opening status, please check once more before visiting.")
        return "\n".join(lines)

    lines = ["제공 데이터 기준으로 관련 항목을 찾았어요."]
    for doc in docs[:5]:
        line = f"- {doc.get('title')} ({doc.get('content_type')})"
        if doc.get("address"):
            line += f": {doc['address']}"
        if doc.get("tel"):
            line += f" / 문의: {doc['tel']}"
        lines.append(line)

    if asks_for_month:
        lines.append("다만 제공 JSON에는 정확한 행사 기간 필드가 없어 해당 월 개최 여부까지는 확정할 수 없습니다.")
    elif route == "local_plus_general":
        lines.append("일반적으로는 이동 동선, 운영 여부, 혼잡 시간은 방문 직전에 한 번 더 확인하는 것을 추천합니다.")
    return "\n".join(lines)
