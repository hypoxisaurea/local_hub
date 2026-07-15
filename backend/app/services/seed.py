# 데이터들 db에 넣기
# 코드에서 직접 만든 초기 샘플 데이터를 DB에 넣음
from sqlalchemy.orm import Session

from ..models import models

def seed_initial_data(db: Session):
    existing = db.query(models.Category).first()
    if existing:
        return

    categories = [
        models.Category(pk_category_id=1, name="여행"),
        models.Category(pk_category_id=2, name="문화"),
        models.Category(pk_category_id=3, name="맛집"),
    ]
    db.add_all(categories)
    db.flush()

    posts = [
        models.Post(
            pk_post_id=1,
            fk_category_id=1,
            title="한강공원 자전거 코스 후기",
            content="한강 자전거 코스가 넓고 경치도 좋았습니다. 중간에 쉬기 좋은 카페도 많아요.",
            password=1234,
            likes=5,
        ),
        models.Post(
            pk_post_id=2,
            fk_category_id=2,
            title="광화문 야간 축제 추천",
            content="광화문에서 열리는 야간 축제는 가족과 함께 다녀오기 좋습니다.",
            password=5678,
            likes=12,
        ),
        models.Post(
            pk_post_id=3,
            fk_category_id=3,
            title="명동 가성비 숙박 정보",
            content="명동 근처 게스트하우스는 가격이 합리적이고 접근성이 좋습니다.",
            password=9012,
            likes=3,
        ),
    ]
    db.add_all(posts)
    db.flush()

    comments = [
        models.Comment(
            pk_comment_id=1,
            fk_post_id=1,
            content="자전거 대여소 정보도 함께 있으면 좋겠어요.",
            password=1111,
        ),
        models.Comment(
            pk_comment_id=2,
            fk_post_id=1,
            content="한강 야경이 정말 예뻐요.",
            password=2222,
        ),
        models.Comment(
            pk_comment_id=3,
            fk_post_id=2,
            content="야간 축제 분위기가 너무 좋았어요.",
            password=3333,
        ),
    ]
    db.add_all(comments)
    db.commit()
