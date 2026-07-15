from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.base import engine

MAP_SPOT_TABLES = {
    "관광지": "tour_서울_관광지",
    "레포츠": "tour_서울_레포츠",
    "맛집": "tour_서울_음식점",
    "문화시설": "tour_서울_문화시설",
    "쇼핑": "tour_서울_쇼핑",
    "축제": "tour_서울_축제공연행사",
}

MAP_CATEGORY_ALIASES = {
    "all": "all",
    "전체": "all",
    "관광": "관광지",
    "관광지": "관광지",
    "attractions": "관광지",
    "레포츠": "레포츠",
    "sports": "레포츠",
    "맛집": "맛집",
    "음식점": "맛집",
    "restaurants": "맛집",
    "food": "맛집",
    "문화시설": "문화시설",
    "culture": "문화시설",
    "쇼핑": "쇼핑",
    "shopping": "쇼핑",
    "축제": "축제",
    "축제공연행사": "축제",
    "festivals": "축제",
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


def _fetch_map_spot_rows(category: str, table_name: str, q: Optional[str] = None, limit: int = 300) -> List[dict]:
    if not inspect(engine).has_table(table_name):
        return []

    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f'''
                SELECT id, contentid, title, addr1, mapx, mapy, firstimage, contentType
                FROM "{table_name}"
                WHERE mapx IS NOT NULL
                  AND mapy IS NOT NULL
                  AND TRIM(mapx) != ''
                  AND TRIM(mapy) != ''
                ORDER BY id DESC
                LIMIT :limit
                '''
            ),
            {"limit": limit},
        ).mappings().all()
        items = [dict(row) for row in rows]

    if q:
        like_q = q.lower()
        items = [
            item for item in items
            if like_q in (item.get("title") or "").lower()
            or like_q in (item.get("addr1") or "").lower()
            or like_q in (item.get("contentType") or "").lower()
        ]

    return [
        {
            **item,
            "category": category,
            "mapx": str(item.get("mapx") or ""),
            "mapy": str(item.get("mapy") or ""),
        }
        for item in items
    ]
