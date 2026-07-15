from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import models
from ..schemas import schemas

def get_posts(db: Session, q: str | None = None):
    query = db.query(models.Post)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            models.Post.title.ilike(like_q)
            | models.Post.content.ilike(like_q)
        )
    return query.order_by(models.Post.pk_post_id.desc()).all()

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.pk_post_id == post_id).first()

def create_post(db: Session, post_in: schemas.PostCreate):
    db_post = models.Post(**post_in.dict())
    db.add(db_post)
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
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()