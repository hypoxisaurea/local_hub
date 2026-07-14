from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PlaceBase(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    address: Optional[str] = None


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    pk_category_id: int

    class Config:
        orm_mode = True


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
