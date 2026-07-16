from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import models
from ..schemas import schemas
from ..services.post_translation import translate_post_to_english

def _post_model(lang: str):
    return models.PostEn if lang == "en" else models.Post


def _upsert_post_en(db: Session, db_post: models.Post, use_llm: bool = True):
    translated = (
        translate_post_to_english(db_post.title, db_post.content)
        if use_llm
        else {"title": db_post.title, "content": db_post.content or ""}
    )
    db_post_en = db.query(models.PostEn).filter(models.PostEn.pk_post_id == db_post.pk_post_id).first()

    if db_post_en is None:
        db_post_en = models.PostEn(pk_post_id=db_post.pk_post_id)
        db.add(db_post_en)

    db_post_en.fk_category_id = db_post.fk_category_id
    db_post_en.title = translated["title"]
    db_post_en.content = translated["content"]
    db_post_en.likes = db_post.likes
    db_post_en.password = db_post.password
    if db_post.created_at is not None:
        db_post_en.created_at = db_post.created_at


def ensure_missing_post_en(db: Session):
    posts = (
        db.query(models.Post)
        .outerjoin(models.PostEn, models.PostEn.pk_post_id == models.Post.pk_post_id)
        .filter(models.PostEn.pk_post_id.is_(None))
        .all()
    )
    if not posts:
        return 0

    for db_post in posts:
        _upsert_post_en(db, db_post, use_llm=False)

    db.commit()
    return len(posts)


def get_posts(db: Session, q: str | None = None, lang: str = "ko"):
    model = _post_model(lang)
    query = db.query(model)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            model.title.ilike(like_q)
            | model.content.ilike(like_q)
        )
    return query.order_by(model.pk_post_id.desc()).all()

def get_post(db: Session, post_id: int, lang: str = "ko"):
    model = _post_model(lang)
    return db.query(model).filter(model.pk_post_id == post_id).first()

def create_post(db: Session, post_in: schemas.PostCreate):
    db_post = models.Post(**post_in.dict())
    db.add(db_post)
    db.flush()
    _upsert_post_en(db, db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_in: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.password != post_in.password:
        raise HTTPException(status_code=403, detail="Incorrect password")
    if post_in.fk_category_id is not None:
        db_post.fk_category_id = post_in.fk_category_id
    if post_in.title is not None:
        db_post.title = post_in.title
    if post_in.content is not None:
        db_post.content = post_in.content
    _upsert_post_en(db, db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.query(models.PostEn).filter(models.PostEn.pk_post_id == post_id).delete()
    db.delete(db_post)
    db.commit()
