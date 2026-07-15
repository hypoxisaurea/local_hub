# 데이터들 db에 넣기
import random

from faker import Faker
from sqlalchemy.orm import Session

from ..models import models

fake = Faker("ko_KR")


def seed_initial_data(db: Session):
    # ------------------------
    # Category
    # ------------------------
    if not db.query(models.Category).first():
        categories = [
            models.Category(pk_category_id=1, name="여행"),
            models.Category(pk_category_id=2, name="문화"),
            models.Category(pk_category_id=3, name="맛집"),
            models.Category(pk_category_id=4, name="카페"),
            models.Category(pk_category_id=5, name="축제"),
            models.Category(pk_category_id=6, name="쇼핑"),
        ]

        db.add_all(categories)
        db.flush()

    # ------------------------
    # Post
    # ------------------------
    if not db.query(models.Post).first():
        posts = []

        POST_COUNT = 100

        for i in range(1, POST_COUNT + 1):
            posts.append(
                models.Post(
                    pk_post_id=i,
                    fk_category_id=random.randint(1, 6),
                    title=fake.sentence(nb_words=5),
                    content="\n".join(fake.paragraphs(nb=3)),
                    password=random.randint(1000, 9999),
                    likes=random.randint(0, 300),
                )
            )

        db.add_all(posts)
        db.flush()

    # ------------------------
    # Comment
    # ------------------------
    if not db.query(models.Comment).first():
        comments = []

        COMMENT_COUNT = 500

        for i in range(1, COMMENT_COUNT + 1):
            comments.append(
                models.Comment(
                    pk_comment_id=i,
                    fk_post_id=random.randint(1, POST_COUNT),
                    content=fake.sentence(nb_words=10),
                    password=random.randint(1000, 9999),
                )
            )

        db.add_all(comments)

    db.commit()