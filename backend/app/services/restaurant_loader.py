import json
from pathlib import Path

from sqlalchemy.orm import Session

from ..models import models


def get_restaurant_data_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "서울_맛집.json"


def load_restaurant_items(db: Session) -> int:
    data_path = get_restaurant_data_path()
    if not data_path.exists():
        return 0

    with data_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    items = payload.get("DATA", []) or []
    inserted_count = 0

    for raw in items:
        post_sn = raw.get("post_sn")
        if post_sn is None:
            continue

        post_sn_int = int(post_sn)

        existing = (
            db.query(models.Restaurant)
            .filter(models.Restaurant.post_sn == post_sn_int)
            .first()
        )
        if existing:
            continue

        db.add(
            models.Restaurant(
                post_sn=post_sn_int,
                title=str(raw.get("post_sj", "") or "").strip(),
                address=raw.get("address"),
                new_address=raw.get("new_address"),
                subway_info=raw.get("subway_info"),
                tel=raw.get("cmmn_telno"),
                homepage_url=raw.get("cmmn_hmpg_url"),
                homepage_lang=raw.get("cmmn_hmpg_lang"),
                represent_menu=raw.get("fd_reprsnt_menu"),
                use_time=raw.get("cmmn_use_time"),
                post_url=raw.get("post_url"),
                lang_code_id=raw.get("lang_code_id"),
            )
        )
        inserted_count += 1

    if inserted_count:
        db.commit()

    return inserted_count
