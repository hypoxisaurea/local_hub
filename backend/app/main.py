#api 호출 파트 (FastAPI 사용)

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas
from .database import SessionLocal, engine, get_db
from .seed import seed_initial_data
from .tour_loader import load_tour_items

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LocalHub API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    with SessionLocal() as db:
        seed_initial_data(db)
        load_tour_items(db)


@app.get("/api/places", response_model=List[schemas.Place])
def read_places(
    q: Optional[str] = Query(None, description="검색어"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Place)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            models.Place.title.ilike(like_q)
            | models.Place.category.ilike(like_q)
            | models.Place.description.ilike(like_q)
            | models.Place.address.ilike(like_q)
        )
    return query.order_by(models.Place.id.desc()).all()


@app.get("/api/tour-items", response_model=List[schemas.TourItem])
def read_tour_items(
    q: Optional[str] = Query(None, description="검색어"),
    contentTypeId: Optional[str] = Query(None, alias="contentTypeId"),
    db: Session = Depends(get_db)
):
    query = db.query(models.TourItem)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            models.TourItem.title.ilike(like_q)
            | models.TourItem.addr1.ilike(like_q)
            | models.TourItem.addr2.ilike(like_q)
            | models.TourItem.region.ilike(like_q)
            | models.TourItem.contentType.ilike(like_q)
        )
    if contentTypeId:
        query = query.filter(models.TourItem.contenttypeid == contentTypeId)
    return query.order_by(models.TourItem.id.desc()).limit(200).all()


@app.post("/api/places", response_model=schemas.Place)
def create_place(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    db_place = models.Place(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
