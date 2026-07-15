#api 호출 파트 (FastAPI 사용) //라우터 기능들 전부 여기다 넣음 -> 추후 라우터 파일로 분리?

from fastapi import FastAPI, Depends, Query, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from typing import List, Optional

from .models import models

from .schemas import schemas
from .db.base import SessionLocal, engine, get_db
from .services.seed import seed_initial_data
from .services.tour_loader import load_tour_items_separate_tables as load_tour_items
from .services.restaurant_loader import load_restaurant_items

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LocalHub API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    with SessionLocal() as db:
        seed_initial_data(db)
        load_tour_items(db)
        load_restaurant_items(db)


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

# 투어 데이터 전체 있는 테이블 조회 (임시) 였는데, 테이블 단위로 나눠서 사용하므로 지금은 필요없음. 추후 필요하면 다시 살릴 수 있음
# @app.get("/api/tour-items", response_model=List[schemas.TourItem])
# def read_tour_items(
#     q: Optional[str] = Query(None, description="검색어"),
#     contentTypeId: Optional[str] = Query(None, alias="contentTypeId"),
#     db: Session = Depends(get_db)
# ):
#     query = db.query(models.TourItem)
#     if q:
#         like_q = f"%{q}%"
#         query = query.filter(
#             models.TourItem.title.ilike(like_q)
#             | models.TourItem.addr1.ilike(like_q)
#             | models.TourItem.addr2.ilike(like_q)
#             | models.TourItem.region.ilike(like_q)
#             | models.TourItem.contentType.ilike(like_q)
#         )
#     if contentTypeId:
#         query = query.filter(models.TourItem.contenttypeid == contentTypeId)
#     return query.order_by(models.TourItem.id.desc()).limit(200).all()


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


@app.get("/api/restaurants", response_model=List[schemas.Restaurant])
def read_restaurants(
    q: Optional[str] = Query(None, description="검색어"),
    db: Session = Depends(get_db)
):
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


TRAVEL_SPOT_TABLES = {
    "attractions": "tour_서울_관광지",
    "sports": "tour_서울_레포츠",
    "culture": "tour_서울_문화시설",
    "shopping": "tour_서울_쇼핑",
    "festivals": "tour_서울_축제공연행사",
}


def _fetch_travel_spot_rows(table_name: str, q: Optional[str] = None, limit: int = 200) -> List[dict]:
    if not inspect(engine).has_table(table_name):
        return []

    with engine.connect() as conn:
        rows = conn.execute(text(f'SELECT * FROM "{table_name}"')).mappings().all()
        items = [dict(row) for row in rows]

    if q:
        like_q = q.lower()
        items = [
            item for item in items
            if like_q in (item.get("title") or "").lower()
            or like_q in (item.get("addr1") or "").lower()
            or like_q in (item.get("contentType") or "").lower()
        ]

    return items[:limit]

@app.get("/api/travel-spots/attractions", response_model=List[schemas.TourItem])
def read_travel_spots_attractions(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_rows(TRAVEL_SPOT_TABLES["attractions"], q=q)


@app.get("/api/travel-spots/sports", response_model=List[schemas.TourItem])
def read_travel_spots_sports(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_rows(TRAVEL_SPOT_TABLES["sports"], q=q)


@app.get("/api/travel-spots/culture", response_model=List[schemas.TourItem])
def read_travel_spots_culture(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_rows(TRAVEL_SPOT_TABLES["culture"], q=q)


@app.get("/api/travel-spots/shopping", response_model=List[schemas.TourItem])
def read_travel_spots_shopping(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_rows(TRAVEL_SPOT_TABLES["shopping"], q=q)

@app.get("/api/festivals", response_model=List[schemas.TourItem])
def read_festivals(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_rows(TRAVEL_SPOT_TABLES["festivals"], q=q)

@app.get("/api/travel-spots", response_model=List[schemas.TourItem])
def read_travel_spots(
    q: Optional[str] = Query(None, description="검색어"),
):
    combined = []
    for table_name in TRAVEL_SPOT_TABLES.values():
        combined.extend(_fetch_travel_spot_rows(table_name, q=q, limit=200))
    return combined


# id, 이미지, 이름, 주소 만 가져오는 간단한 조회용 API (검색어 가능)
def _fetch_travel_spot_simple_rows(
    table_name: str,
    q: Optional[str] = None,
    limit: int = 200
) -> List[dict]:
    if not inspect(engine).has_table(table_name):
        return []

    with engine.connect() as conn:
        rows = conn.execute(
            text(f'SELECT contentid, firstimage, title, addr1 FROM "{table_name}"')
        ).mappings().all()
        items = [dict(row) for row in rows]

    if q:
        like_q = q.lower()
        items = [
            item for item in items
            if like_q in (item.get("title") or "").lower()
            or like_q in (item.get("addr1") or "").lower()
            or like_q in (item.get("contentid") or "").lower()
        ]

    return items[:limit]

@app.get("/api/travel-spots-simple/attractions", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_attractions(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_simple_rows(TRAVEL_SPOT_TABLES["attractions"], q=q)

@app.get("/api/travel-spots-simple/sports", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_sports(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_simple_rows(TRAVEL_SPOT_TABLES["sports"], q=q)

@app.get("/api/travel-spots-simple/culture", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_culture(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_simple_rows(TRAVEL_SPOT_TABLES["culture"], q=q)

@app.get("/api/travel-spots-simple/shopping", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_shopping(
    q: Optional[str] = Query(None, description="검색어"),
):
    return _fetch_travel_spot_simple_rows(TRAVEL_SPOT_TABLES["shopping"], q=q)



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