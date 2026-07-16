# 백엔드에서 API 요청과 응답에 사용하는 데이터 구조를 정의하는 파일
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


# 사용자가 카테고리를 사용할 때 사용하는 정보
class CategoryBase(BaseModel):
    name: str

# 카테고리 생성
class CategoryCreate(CategoryBase):
    pass

# 서버가 카테고리를 사용할 때 사용하는 정보
class Category(CategoryBase):
    pk_category_id: int

    model_config = ConfigDict(from_attributes=True)

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
    likes: int = 0

    model_config = ConfigDict(from_attributes=True)

# 게시글 수정
class PostUpdate(BaseModel):
    fk_category_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    password: int


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

    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)


class RestaurantBase(BaseModel):
    post_sn: int
    title: str
    address: Optional[str] = None
    new_address: Optional[str] = None
    subway_info: Optional[str] = None
    tel: Optional[str] = None
    homepage_url: Optional[str] = None
    homepage_lang: Optional[str] = None
    represent_menu: Optional[str] = None
    use_time: Optional[str] = None
    post_url: Optional[str] = None
    lang_code_id: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# 관광지 요약 정보 (Json 데이터 기반)
class TravelSpotSummary(BaseModel):
    contentid: str
    firstimage: Optional[str] = None
    title: str
    addr1: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MapSpot(BaseModel):
    id: int
    contentid: Optional[str] = None
    category: str
    title: str
    addr1: Optional[str] = None
    mapx: str
    mapy: str
    firstimage: Optional[str] = None
    contentType: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TourItemTranslationBase(BaseModel):
    category: str
    contentid: str
    lang: str
    title: Optional[str] = None
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    contentType: Optional[str] = None


class TourItemTranslationCreate(TourItemTranslationBase):
    pass


class TourItemTranslation(TourItemTranslationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
