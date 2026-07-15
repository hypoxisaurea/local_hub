from sqlalchemy.orm import Session
from ..models import models

def _restaurant_model(lang: str):
    return models.RestaurantEn if lang == "en" else models.Restaurant

def get_restaurants(db: Session, q: str | None = None, lang: str = "ko"):
    model = _restaurant_model(lang)
    query = db.query(model)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            model.title.ilike(like_q)
            | model.address.ilike(like_q)
            | model.new_address.ilike(like_q)
            | model.represent_menu.ilike(like_q)
            | model.subway_info.ilike(like_q)
        )
    return query.order_by(model.id.desc()).limit(200).all()
