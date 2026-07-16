from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session

from ..deps import get_db
from ...schemas import schemas
from ...crud import posts as crud_posts

router = APIRouter(prefix="/api/posts", tags=["posts"])

@router.get("", response_model=List[schemas.Post])
def read_posts(
    q: Optional[str] = Query(None),
    lang: str = Query("ko", pattern="^(ko|en)$", description="Content display language"),
    db: Session = Depends(get_db),
):
    return crud_posts.get_posts(db, q, lang=lang)

@router.get("/{post_id}", response_model=schemas.Post)
def read_post(
    post_id: int,
    lang: str = Query("ko", pattern="^(ko|en)$", description="Content display language"),
    db: Session = Depends(get_db),
):
    post = crud_posts.get_post(db, post_id, lang=lang)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud_posts.create_post(db, post)

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    return crud_posts.update_post(db, post_id, post)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    crud_posts.delete_post(db, post_id)
