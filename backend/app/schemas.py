# 백엔드에서 API 요청과 응답에 사용하는 데이터 구조를 정의하는 파일
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 초기에 임시로 넣었던 플레이스(장소) 정보
class PlaceBase(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    address: Optional[str] = None

# 초기에 임시로 넣었던 플레이스(장소) 생성
class PlaceCreate(PlaceBase):
    pass

# 초기에 임시로 넣었던 플레이스(장소) 정보
class Place(PlaceBase):
    id: int

    class Config:
        orm_mode = True

# 사용자가 카테고리를 사용할 때 사용하는 정보
class CategoryBase(BaseModel):
    name: str

# 카테고리 생성
class CategoryCreate(CategoryBase):
    pass

# 서버가 카테고리를 사용할 때 사용하는 정보
class Category(CategoryBase):
    pk_category_id: int

    class Config:
        orm_mode = True

# 게시글
class PostBase(BaseModel):
    fk_category_id: int
    title: str
    content: Optional[str] = None
    password: int


class PostCreate(PostBase):
    pass


class Post(PostBase):
    pk_post_id: int
    created_at: Optional[datetime]
    category: Optional[Category] = None

    class Config:
        orm_mode = True

# 댓글
class CommentBase(BaseModel):
    fk_post_id: int
    content: Optional[str] = None
    password: int


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    pk_comment_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

# 관광지 정보 (Json 데이터 기반)
class TourItem(BaseModel):
    id: int
    contentid: str
    contenttypeid: Optional[str] = None
    title: str
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    zipcode: Optional[str] = None
    tel: Optional[str] = None
    mapx: Optional[str] = None
    mapy: Optional[str] = None
    mlevel: Optional[str] = None
    areacode: Optional[str] = None
    sigungucode: Optional[str] = None
    lDongRegnCd: Optional[str] = None
    lDongSignguCd: Optional[str] = None
    cat1: Optional[str] = None
    cat2: Optional[str] = None
    cat3: Optional[str] = None
    lclsSystm1: Optional[str] = None
    lclsSystm2: Optional[str] = None
    lclsSystm3: Optional[str] = None
    firstimage: Optional[str] = None
    firstimage2: Optional[str] = None
    cpyrhtDivCd: Optional[str] = None
    createdtime: Optional[str] = None
    modifiedtime: Optional[str] = None
    region: Optional[str] = None
    contentType: Optional[str] = None

    class Config:
        orm_mode = True
