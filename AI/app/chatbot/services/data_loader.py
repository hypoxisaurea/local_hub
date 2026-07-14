import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.chatbot.config import get_settings


CONTENT_TYPE_BY_FILE = {
    "서울_관광지.json": "관광지",
    "서울_레포츠.json": "레포츠",
    "서울_문화시설.json": "문화시설",
    "서울_쇼핑.json": "쇼핑",
    "서울_숙박.json": "숙박",
    "서울_여행코스.json": "여행코스",
    "서울_축제공연행사.json": "축제공연행사",
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache
def load_local_documents() -> list[dict[str, Any]]:
    settings = get_settings()
    documents: list[dict[str, Any]] = []

    for path in sorted(settings.data_dir.glob("서울_*.json")):
        data = _load_json(path)
        content_type = str(data.get("contentType") or CONTENT_TYPE_BY_FILE.get(path.name, path.stem))

        for item in data.get("items", []):
            title = str(item.get("title") or "").strip()
            if not title:
                continue

            documents.append(
                {
                    "content_type": content_type,
                    "source_file": path.name,
                    "title": title,
                    "address": " ".join(
                        part.strip()
                        for part in [str(item.get("addr1") or ""), str(item.get("addr2") or "")]
                        if part and part.strip()
                    ),
                    "tel": str(item.get("tel") or "").strip(),
                    "image": str(item.get("firstimage") or item.get("firstimage2") or "").strip(),
                    "mapx": str(item.get("mapx") or "").strip(),
                    "mapy": str(item.get("mapy") or "").strip(),
                    "contentid": str(item.get("contentid") or "").strip(),
                    "modifiedtime": str(item.get("modifiedtime") or "").strip(),
                    "raw": item,
                }
            )

    return documents
