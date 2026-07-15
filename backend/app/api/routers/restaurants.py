from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..deps import get_db
from ...schemas import schemas
from ...crud import restaurants as crud_restaurants

router = APIRouter(prefix="/api/restaurants", tags=["restaurants"])

@router.get("", response_model=List[schemas.Restaurant])
def read_restaurants(
    q: Optional[str] = Query(None),
    lang: str = Query("ko", pattern="^(ko|en)$", description="콘텐츠 표시 언어"),
    db: Session = Depends(get_db),
):
    return crud_restaurants.get_restaurants(db, q, lang=lang)
