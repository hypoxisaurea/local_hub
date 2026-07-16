import re
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ..llm.client import get_chat_model
from backend.app.db.base import engine

DANGEROUS_KEYWORDS = {
    "delete",
    "update",
    "insert",
    "drop",
    "alter",
    "truncate",
    "create",
    "grant",
    "revoke",
}

SCHEMA_PROMPT = """
당신은 한국어 질문을 SQL SELECT 쿼리로 바꾸는 에이전트입니다.
다음 스키마를 참고하세요.

- posts(pk_post_id, fk_category_id, title, content, password, created_at)
- comments(pk_comment_id, fk_post_id, content, password, created_at)
- tour_items(id, title, addr1, region, contentType, contenttypeid, contentid, firstimage)
- tour_서울_관광지, tour_서울_문화시설, tour_서울_축제공연행사, tour_서울_여행코스,
  tour_서울_레포츠, tour_서울_숙박, tour_서울_쇼핑, tour_서울_음식점
- categories(pk_category_id, name)

관광 데이터의 contentType 값:
관광지, 문화시설, 축제공연행사, 여행코스, 레포츠, 숙박, 쇼핑, 음식점
"""

COUNT_HINTS = ("개수", "몇", "몇개", "몇 개", "총", "얼마나", "count")
LIST_HINTS = ("목록", "리스트", "보여줘", "조회", "찾아줘")
TOUR_CONTENT_TYPES = {
    "관광지": ("관광지", "관광", "명소", "가볼만"),
    "문화시설": ("문화시설", "문화", "박물관", "미술관", "도서관", "공연장", "전시관"),
    "축제공연행사": ("축제공연행사", "축제", "행사", "공연", "페스티벌", "이벤트"),
    "여행코스": ("여행코스", "코스", "여행 코스", "여행코스", "루트"),
    "레포츠": ("레포츠", "스포츠", "체험", "운동"),
    "숙박": ("숙박", "숙소", "호텔", "게스트하우스"),
    "쇼핑": ("쇼핑", "시장", "상가", "몰", "백화점"),
    "음식점": ("음식점", "식당", "맛집", "먹거리", "카페"),
}
TOUR_TABLES = {
    content_type: f'tour_서울_{content_type}'
    for content_type in TOUR_CONTENT_TYPES
}

def _is_safe_sql(sql: str) -> bool:
    normalized = sql.lower().strip()
    if not normalized.startswith("select"):
        return False
    if any(keyword in normalized for keyword in DANGEROUS_KEYWORDS):
        return False
    if ";" in normalized:
        return False
    return True

def _extract_sql(text_response: str) -> str:
    match = re.search(r"```(?:sql)?\s*(.*?)```", text_response, re.S | re.I)
    if match:
        return match.group(1).strip()
    return text_response.strip()

def _known_sql_from_text(message: str) -> str | None:
    lowered = message.lower()
    if "게시글" in lowered and ("개수" in lowered or "몇" in lowered):
        return "SELECT COUNT(*) AS cnt FROM posts"
    if "게시글" in lowered and ("목록" in lowered or "리스트" in lowered or "보여줘" in lowered):
        return "SELECT pk_post_id, title, created_at FROM posts ORDER BY created_at DESC LIMIT 10"

    content_type = _detect_content_type(lowered)
    if content_type and any(hint in lowered for hint in COUNT_HINTS):
        return f'SELECT COUNT(*) AS cnt FROM "{TOUR_TABLES[content_type]}"'
    if content_type and any(hint in lowered for hint in LIST_HINTS):
        return (
            f'SELECT id, title, addr1, region FROM "{TOUR_TABLES[content_type]}" '
            "ORDER BY id LIMIT 10"
        )

    return None


def _detect_content_type(lowered_message: str) -> str | None:
    for content_type, keywords in TOUR_CONTENT_TYPES.items():
        if any(keyword.lower() in lowered_message for keyword in keywords):
            return content_type
    return None


async def generate_sql_from_text(message: str) -> str:
    known_sql = _known_sql_from_text(message)
    if known_sql:
        return known_sql

    model = get_chat_model()

    if model is not None:
        try:
            response = await model.ainvoke([
                ("system", SCHEMA_PROMPT),
                ("human", f'사용자 질문: {message}\n\n반드시 SELECT 문만 생성하고, SQL만 출력하세요.'),
            ])
            sql = _extract_sql(str(response.content))
            if _is_safe_sql(sql):
                return sql
        except Exception:
            pass

    raise ValueError("지원하지 않는 DB 질의입니다.")

async def execute_sql(sql: str) -> list[dict[str, Any]]:
    if not _is_safe_sql(sql):
        raise ValueError("안전하지 않은 SQL 쿼리입니다.")

    with engine.begin() as conn:
        result = conn.execute(text(sql))
        columns = result.keys()
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        return rows

def format_db_result(message: str, rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "조회 결과가 없습니다."

    if len(rows) == 1 and "cnt" in rows[0]:
        label = _detect_content_type(message.lower())
        if "게시글" in message:
            label = "게시글"
        target = f"{_with_topic_particle(label)} " if label else "조회 결과는 "
        return f"{target}총 {rows[0]['cnt']}개입니다."

    return "조회 결과입니다:\n" + "\n".join(str(row) for row in rows)


def _with_topic_particle(label: str) -> str:
    last = label[-1]
    has_batchim = (ord(last) - ord("가")) % 28 != 0 if "가" <= last <= "힣" else False
    return f"{label}{'은' if has_batchim else '는'}"
