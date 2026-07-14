#  DB 스키마를 선언 (DB)
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from .database import Base

# 과거 초반 데이터 설정할 때 만든 것 (임시)
class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, index=True)
    category = Column(String(80), nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=True)

# 테이블 설계하고 생성한 카테고리
class Category(Base):
    __tablename__ = "categories"

    pk_category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True, index=True)

    posts = relationship("Post", back_populates="category", cascade="all, delete-orphan")

# 테이블 설계하고 생성한 포스트(게시글)
class Post(Base):
    __tablename__ = "posts"

    pk_post_id = Column(Integer, primary_key=True, index=True)
    fk_category_id = Column(Integer, ForeignKey("categories.pk_category_id"), nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=True)
    password = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

# 테이블 설계하고 생성한 포스트(댓글)
class Comment(Base):
    __tablename__ = "comments"

    pk_comment_id = Column(Integer, primary_key=True, index=True)
    fk_post_id = Column(Integer, ForeignKey("posts.pk_post_id"), nullable=False, index=True)
    content = Column(Text, nullable=True)
    password = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    post = relationship("Post", back_populates="comments")

# 관광지 정보 (Json 데이터 기반)
class TourItem(Base):
    __tablename__ = "tour_items"

    id = Column(Integer, primary_key=True, index=True)
    contentid = Column(String(80), nullable=False, index=True)
    contenttypeid = Column(String(20), nullable=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    addr1 = Column(String(255), nullable=True)
    addr2 = Column(String(255), nullable=True)
    zipcode = Column(String(20), nullable=True)
    tel = Column(String(80), nullable=True)
    mapx = Column(String(60), nullable=True)
    mapy = Column(String(60), nullable=True)
    mlevel = Column(String(20), nullable=True)
    areacode = Column(String(20), nullable=True)
    sigungucode = Column(String(20), nullable=True)
    lDongRegnCd = Column(String(50), nullable=True)
    lDongSignguCd = Column(String(50), nullable=True)
    cat1 = Column(String(50), nullable=True)
    cat2 = Column(String(50), nullable=True)
    cat3 = Column(String(50), nullable=True)
    lclsSystm1 = Column(String(100), nullable=True)
    lclsSystm2 = Column(String(100), nullable=True)
    lclsSystm3 = Column(String(100), nullable=True)
    firstimage = Column(String(500), nullable=True)
    firstimage2 = Column(String(500), nullable=True)
    cpyrhtDivCd = Column(String(50), nullable=True)
    createdtime = Column(String(30), nullable=True)
    modifiedtime = Column(String(30), nullable=True)
    region = Column(String(100), nullable=True)
    contentType = Column(String(100), nullable=True)
