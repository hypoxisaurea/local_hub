import json
from pathlib import Path

from sqlalchemy.orm import Session

from ..models import models


def get_translation_file() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "tour_item_translations.json"


def load_tour_item_translations(db: Session) -> int:
    translation_file = get_translation_file()

    if not translation_file.exists():
        return 0

    with translation_file.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    rows = payload.get("items", []) if isinstance(payload, dict) else payload
    inserted_or_updated = 0

    for raw in rows or []:
        category = str(raw.get("category") or "").strip()
        contentid = str(raw.get("contentid") or "").strip()
        lang = str(raw.get("lang") or "").strip().lower()

        if not category or not contentid or lang not in {"en"}:
            continue

        existing = (
            db.query(models.TourItemTranslation)
            .filter(
                models.TourItemTranslation.category == category,
                models.TourItemTranslation.contentid == contentid,
                models.TourItemTranslation.lang == lang,
            )
            .first()
        )

        values = {
            "title": raw.get("title"),
            "addr1": raw.get("addr1"),
            "addr2": raw.get("addr2"),
            "contentType": raw.get("contentType"),
        }

        if existing:
            for key, value in values.items():
                setattr(existing, key, value)
        else:
            db.add(
                models.TourItemTranslation(
                    category=category,
                    contentid=contentid,
                    lang=lang,
                    **values,
                )
            )

        inserted_or_updated += 1

    if inserted_or_updated:
        db.commit()

    return inserted_or_updated
