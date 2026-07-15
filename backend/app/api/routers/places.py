from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..deps import get_db
from ...schemas import schemas
from ...crud import places as crud_places

router = APIRouter(prefix="/api/places", tags=["places"])

@router.get("", response_model=List[schemas.Place])
def read_places(q: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return crud_places.get_places(db, q)

@router.post("", response_model=schemas.Place)
def create_place(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    return crud_places.create_place(db, place)