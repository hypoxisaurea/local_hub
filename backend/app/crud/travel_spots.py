from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.base import engine

TRAVEL_SPOT_TABLES = {
    "attractions": "tour_서울_관광지",
    "sports": "tour_서울_레포츠",
    "culture": "tour_서울_문화시설",
    "shopping": "tour_서울_쇼핑",
    "festivals": "tour_서울_축제공연행사",
}

def _fetch_travel_spot_rows(table_name: str, q: Optional[str] = None, limit: int = 200) -> List[dict]:
    if not inspect(engine).has_table(table_name):
        return []
    with engine.connect() as conn:
        rows = conn.execute(text(f'SELECT * FROM "{table_name}"')).mappings().all()
    items = [dict(row) for row in rows]
    if q:
        like_q = q.lower()
        items = [
            item for item in items
            if like_q in (item.get("title") or "").lower()
            or like_q in (item.get("addr1") or "").lower()
            or like_q in (item.get("contentType") or "").lower()
        ]
    return items[:limit]


# id, 이미지, 이름, 주소 만 가져오는 간단한 조회용 API (검색어 가능)
def _fetch_travel_spot_simple_rows(
    table_name: str,
    q: Optional[str] = None,
    limit: int = 200
) -> List[dict]:
    if not inspect(engine).has_table(table_name):
        return []

    with engine.connect() as conn:
        rows = conn.execute(
            text(f'SELECT contentid, firstimage, title, addr1 FROM "{table_name}"')
        ).mappings().all()
        items = [dict(row) for row in rows]

    if q:
        like_q = q.lower()
        items = [
            item for item in items
            if like_q in (item.get("title") or "").lower()
            or like_q in (item.get("addr1") or "").lower()
            or like_q in (item.get("contentid") or "").lower()
        ]

    return items[:limit]