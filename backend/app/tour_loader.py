import json
from pathlib import Path
from typing import List

from sqlalchemy.orm import Session

from . import models


def get_data_directory() -> Path:
    return Path(__file__).resolve().parents[2] / "data"


def load_tour_items(db: Session) -> int:
    if db.query(models.TourItem).count() > 0:
        return 0

    data_dir = get_data_directory()
    json_files: List[Path] = sorted(data_dir.glob("*.json"))
    tour_items = []

    for json_file in json_files:
        with json_file.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        region = payload.get("region")
        contentType = payload.get("contentType")

        for raw in payload.get("items", []) or []:
            tour_items.append(
                models.TourItem(
                    contentid=str(raw.get("contentid", "")),
                    contenttypeid=str(raw.get("contenttypeid", "")),
                    title=str(raw.get("title", "")),
                    addr1=raw.get("addr1"),
                    addr2=raw.get("addr2"),
                    zipcode=raw.get("zipcode"),
                    tel=raw.get("tel"),
                    mapx=raw.get("mapx"),
                    mapy=raw.get("mapy"),
                    mlevel=raw.get("mlevel"),
                    areacode=raw.get("areacode"),
                    sigungucode=raw.get("sigungucode"),
                    lDongRegnCd=raw.get("lDongRegnCd"),
                    lDongSignguCd=raw.get("lDongSignguCd"),
                    cat1=raw.get("cat1"),
                    cat2=raw.get("cat2"),
                    cat3=raw.get("cat3"),
                    lclsSystm1=raw.get("lclsSystm1"),
                    lclsSystm2=raw.get("lclsSystm2"),
                    lclsSystm3=raw.get("lclsSystm3"),
                    firstimage=raw.get("firstimage"),
                    firstimage2=raw.get("firstimage2"),
                    cpyrhtDivCd=raw.get("cpyrhtDivCd"),
                    createdtime=raw.get("createdtime"),
                    modifiedtime=raw.get("modifiedtime"),
                    region=region,
                    contentType=contentType,
                )
            )

    db.bulk_save_objects(tour_items)
    db.commit()
    return len(tour_items)
