

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..deps import get_db
from ...schemas import schemas
from ...crud import map as crud_map

router = APIRouter(prefix="/api/map-spots", tags=["map_spots"])

@router.get("", response_model=List[schemas.MapSpot])
def read_map_spots(
    category: str = Query("all", description="all, 관광지, 레포츠, 맛집, 문화시설, 쇼핑, 축제"),
    q: Optional[str] = Query(None, description="검색어"),
    limit: int = Query(300, ge=1, le=1000),
):
    normalized = crud_map.MAP_CATEGORY_ALIASES.get(category, category)

    if normalized == "all":
        per_table_limit = max(1, limit // len(crud_map.MAP_SPOT_TABLES))
        combined = []
        for label, table_name in crud_map.MAP_SPOT_TABLES.items():
            combined.extend(crud_map._fetch_map_spot_rows(label, table_name, q=q, limit=per_table_limit))
        return combined[:limit]

    table_name = crud_map.MAP_SPOT_TABLES.get(normalized)
    if not table_name:
        raise HTTPException(status_code=400, detail="Unsupported map category")

    return crud_map._fetch_map_spot_rows(normalized, table_name, q=q, limit=limit)
