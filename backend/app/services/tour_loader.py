
# json 데이터들을 각 파일별로 각각의 테이블에 넣기
import json
from pathlib import Path
from typing import List

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    select,
    func,
    inspect,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from ..db.base import Base, engine
from ..models import models

def get_data_directory() -> Path:
    return Path(__file__).resolve().parents[3] / "data"

def _normalize_table_name(stem: str) -> str:
    name = stem.lower().replace(" ", "_").replace("-", "_")
    return f"tour_{name}"

def _tour_columns():
    return [
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("contentid", String(80)),
        Column("contenttypeid", String(20)),
        Column("title", String(255)),
        Column("addr1", String(255)),
        Column("addr2", String(255)),
        Column("zipcode", String(20)),
        Column("tel", String(80)),
        Column("mapx", String(60)),
        Column("mapy", String(60)),
        Column("mlevel", String(20)),
        Column("areacode", String(20)),
        Column("sigungucode", String(20)),
        Column("lDongRegnCd", String(50)),
        Column("lDongSignguCd", String(50)),
        Column("cat1", String(50)),
        Column("cat2", String(50)),
        Column("cat3", String(50)),
        Column("lclsSystm1", String(100)),
        Column("lclsSystm2", String(100)),
        Column("lclsSystm3", String(100)),
        Column("firstimage", String(500)),
        Column("firstimage2", String(500)),
        Column("cpyrhtDivCd", String(50)),
        Column("createdtime", String(30)),
        Column("modifiedtime", String(30)),
        Column("region", String(100)),
        Column("contentType", String(100)),
    ]

def _get_or_create_table(table_name: str, metadata: MetaData, engine: Engine) -> Table:
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        return Table(table_name, metadata, autoload_with=engine)
    cols = _tour_columns()
    table = Table(table_name, metadata, *cols)
    metadata.create_all(engine, tables=[table])
    return table

def load_tour_items_separate_tables(db: Session) -> int:
    """
    각 JSON 파일마다 별도 테이블을 만들고 데이터를 로드합니다.
    반환값: 삽입된 총 레코드 수
    """
    data_dir = get_data_directory()
    json_files: List[Path] = sorted(data_dir.glob("*.json"))
    total_inserted = 0
    metadata = Base.metadata

    for json_file in json_files:
        with json_file.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        stem = json_file.stem
        table_name = _normalize_table_name(stem)
        table = _get_or_create_table(table_name, metadata, engine)

        # 이미 데이터가 있으면 건너뜀
        with engine.connect() as conn:
            count_stmt = select(func.count()).select_from(table)
            existing = conn.execute(count_stmt).scalar() or 0
            if existing > 0:
                continue

        rows = []
        region = payload.get("region")
        contentType = payload.get("contentType")

        for raw in payload.get("items", []) or []:
            rows.append(
                {
                    "contentid": str(raw.get("contentid", "")),
                    "contenttypeid": str(raw.get("contenttypeid", "")),
                    "title": str(raw.get("title", "")),
                    "addr1": raw.get("addr1"),
                    "addr2": raw.get("addr2"),
                    "zipcode": raw.get("zipcode"),
                    "tel": raw.get("tel"),
                    "mapx": raw.get("mapx"),
                    "mapy": raw.get("mapy"),
                    "mlevel": raw.get("mlevel"),
                    "areacode": raw.get("areacode"),
                    "sigungucode": raw.get("sigungucode"),
                    "lDongRegnCd": raw.get("lDongRegnCd"),
                    "lDongSignguCd": raw.get("lDongSignguCd"),
                    "cat1": raw.get("cat1"),
                    "cat2": raw.get("cat2"),
                    "cat3": raw.get("cat3"),
                    "lclsSystm1": raw.get("lclsSystm1"),
                    "lclsSystm2": raw.get("lclsSystm2"),
                    "lclsSystm3": raw.get("lclsSystm3"),
                    "firstimage": raw.get("firstimage"),
                    "firstimage2": raw.get("firstimage2"),
                    "cpyrhtDivCd": raw.get("cpyrhtDivCd"),
                    "createdtime": raw.get("createdtime"),
                    "modifiedtime": raw.get("modifiedtime"),
                    "region": region,
                    "contentType": contentType,
                }
            )

        if not rows:
            continue

        with engine.begin() as conn:
            conn.execute(table.insert(), rows)
            total_inserted += len(rows)

    return total_inserted
