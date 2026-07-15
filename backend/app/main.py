#api 호출 파트 (FastAPI 사용) //라우터 기능들 전부 여기다 넣음 -> 추후 라우터 파일로 분리?

from fastapi import FastAPI, Depends, Query, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas
from .database import SessionLocal, engine, get_db
from .seed import seed_initial_data
from .tour_loader import load_tour_items_separate_tables as load_tour_items

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


@app.get("/api/posts", response_model=List[schemas.Post])
def read_posts(
    q: Optional[str] = Query(None, description="검색어"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Post)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            models.Post.title.ilike(like_q)
            | models.Post.content.ilike(like_q)
        )
    return query.order_by(models.Post.pk_post_id.desc()).all()


@app.get("/api/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.pk_post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/api/posts", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.pk_post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# OG 태그를 포함한 HTML을 반환하는 엔드포인트 (OpenAI 코드 / 수정 필요)
@app.get("/share/post/{post_id}", response_class=HTMLResponse)
def get_post_og_tags(post_id: int, db: Session = Depends(get_db)):
    # 1. DB에서 게시글 조회 (SQLite) [cite: 11, 38]
    post = db.query(models.Post).filter(models.Post.pk_post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 2. 메인 서비스 URL (Netlify 주소 등 환경변수 처리 필요) [cite: 40, 44]
    frontend_url = f"https://your-netlify-site.netlify.app/posts/{post_id}"
    
    # 3. OG 태그가 포함된 HTML 리턴 (카카오톡 등의 크롤러 수집용) 
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>{post.title} - LocalHub</title>
        
        <meta property="og:title" content="{post.title}" />
        <meta property="og:description" content="{post.content[:100]}" />
        <meta property="og:type" content="article" />
        <meta property="og:url" content="{frontend_url}" />
        <meta property="og:image" content="https://your-netlify-site.netlify.app/logo.png" />
        
        <script>
            window.location.href = "{frontend_url}";
        </script>
    </head>
    <body>
        <h1>{post.title}</h1>
        <p>{post.content}</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)