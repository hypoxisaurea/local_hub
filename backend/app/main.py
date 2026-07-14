from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LocalHub API", version="0.1.0")


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
