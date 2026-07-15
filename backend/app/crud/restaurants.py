from sqlalchemy.orm import Session
from ..models import models

def get_restaurants(db: Session, q: str | None = None):
    query = db.query(models.Restaurant)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            models.Restaurant.title.ilike(like_q)
            | models.Restaurant.address.ilike(like_q)
            | models.Restaurant.new_address.ilike(like_q)
            | models.Restaurant.represent_menu.ilike(like_q)
            | models.Restaurant.subway_info.ilike(like_q)
        )
    return query.order_by(models.Restaurant.id.desc()).limit(200).all()