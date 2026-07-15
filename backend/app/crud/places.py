from sqlalchemy.orm import Session
from ..models import models

def get_places(db: Session, q: str | None = None):
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

def create_place(db: Session, place_in):
    db_place = models.Place(**place_in.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place