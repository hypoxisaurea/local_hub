from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.base import engine

MAP_SPOT_TABLES = {
    "관광지": "tour_서울_관광지",
    "레포츠": "tour_서울_레포츠",
    "맛집": "tour_서울_맛집",
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


def _normalize_lang(lang: str) -> str:
    return "en" if lang == "en" else "ko"


def _localized_table_name(table_name: str, lang: str) -> str:
    return f"{table_name}_en" if _normalize_lang(lang) == "en" else table_name


def _fetch_map_spot_rows(
    category: str,
    table_name: str,
    q: Optional[str] = None,
    limit: int = 300,
    lang: str = "ko",
) -> List[dict]:
    source_table = _localized_table_name(table_name, lang)

    if not inspect(engine).has_table(source_table):
        return []

    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f'''
                SELECT
                    source.id,
                    source.contentid,
                    source.title,
                    source.addr1,
                    source.mapx,
                    source.mapy,
                    source.firstimage,
                    source.contentType
                FROM "{source_table}" AS source
                WHERE source.mapx IS NOT NULL
                  AND source.mapy IS NOT NULL
                  AND TRIM(source.mapx) != ''
                  AND TRIM(source.mapy) != ''
                ORDER BY source.id DESC
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
