import random

from faker import Faker
from sqlalchemy.orm import Session

from ..models import models

fake = Faker("ko_KR")

# 3가지 카테고리에 맞춘 키워드 및 문구 세트 정의
CATEGORY_DATA = {
    1: {  # 여행지 (기존 여행, 문화, 쇼핑 통합)
        "locations": ["제주도", "경주", "부산", "여수", "강릉", "속초", "미술관", "소극장", "아울렛", "편집샵"],
        "adjectives": ["힐링하기 좋은", "풍경이 예술인", "인생샷 건지는", "여유로운", "영감을 주는", "득템 가능한"],
        "actions": ["여행 코스 공유합니다!", "조용히 다녀오기 좋은 곳", "꼭 가봐야 할 명소 추천", "다녀온 솔직 후기", "내돈내산 하울 후기"],
        "reviews": [
            "진짜 뷰가 미쳤습니다... 가슴이 뻥 뚫리는 기분이에요.",
            "부모님 모시고 가기 딱 좋은 코스입니다. 강추해요!",
            "날씨 좋을 때 가면 인생샷 무조건 건집니다. 또 가고 싶네요.",
            "생각보다 볼거리도 많고 즐길 거리가 풍성해서 시간 가는 줄 몰랐습니다."
        ]
    },
    2: {  # 맛집 (기존 맛집, 카페 통합)
        "locations": ["삼겹살집", "파스타 맛집", "노포 식당", "초밥 전문점", "라멘집", "한옥 카페", "오션뷰 카페", "디저트 맛집"],
        "adjectives": ["육즙 가득한", "가성비 넘치는", "웨이팅 필수인", "현지인 추천", "인스타 감성 뿜뿜하는", "커피 향이 너무 좋은"],
        "actions": ["내돈내산 솔직 리뷰", "인생 맛집 찾았습니다!", "메뉴 추천 및 꿀팁", "신상 핫플 털고 왔습니다", "분위기 맛집 인정"],
        "reviews": [
            "한 입 먹자마자 왜 유명한지 바로 이해했습니다. 대존맛!",
            "양이 진짜 엄청 많아요. 가성비 최고고 이 가격에 이 퀄리티라니 믿기지 않습니다.",
            "웨이팅이 좀 길긴 한데, 밑반찬부터 메인 메뉴/음료까지 거를 타선이 없네요.",
            "창밖으로 보이는 뷰를 보면서 멍 때리기 딱 좋은 공간입니다."
        ]
    },
    3: {  # 축제
        "locations": ["벚꽃 축제", "불꽃놀이", "맥주 페스티벌", "재즈 페스티벌", "밤도깨비 야시장", "지역 특산물 축제"],
        "adjectives": ["활기찬 분위기의", "눈이 즐거운", "가족들과 가기 좋은", "볼거리 즐길거리 가득한"],
        "actions": ["일정 및 주차 꿀팁 정보", "준비물 필수 리스트 정리", "현장 분위기 실시간 공유", "솔직한 방문 후기"],
        "reviews": [
            "사람은 진짜 많았는데 그만큼 축제 분위기 제대로 느끼고 왔습니다!",
            "푸드트럭 음식들도 다 맛있고 볼거리가 다양해서 시간 가는 줄 몰랐네요.",
            "야경이 진짜 환상적이었어요. 내년에도 꼭 다시 올 겁니다."
        ]
    }
}

# 댓글용 리액션 문구 세트
SAMPLE_COMMENTS = [
    "와 여기 진짜 꼭 가봐야겠네요! 정보 감사합니다.",
    "꿀팁 대박이네요 ㅋㅋ 저장해두고 주말에 가볼게요.",
    "사진만 봐도 힐링되는 기분이에요.",
    "여기 저도 가봤는데 진짜 좋더라구요!",
    "혹시 대중교통으로 가기에도 괜찮은가요?",
    "웨이팅 보통 얼마나 걸려요?",
    "오... 좋은 정보 감사합니다! 공유할게요.",
    "완전 공감합니다 ㅋㅋ 저도 엄청 만족했었어요."
]


def seed_initial_data(db: Session):
    # ------------------------
    # Category (3개로 축소 및 명칭 변경)
    # ------------------------
    if not db.query(models.Category).first():
        categories = [
            models.Category(pk_category_id=1, name="여행지"),
            models.Category(pk_category_id=2, name="맛집"),
            models.Category(pk_category_id=3, name="축제"),
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
            # 1~3 사이의 카테고리 ID 랜덤 지정 (1: 여행지, 2: 맛집, 3: 축제)
            category_id = random.randint(1, 3)
            meta = CATEGORY_DATA[category_id]

            # 카테고리별 풀(Pool)에서 요소를 뽑아 그럴싸한 제목 생성
            title = f"{random.choice(meta['locations'])} {random.choice(meta['adjectives'])} {random.choice(meta['actions'])}"
            
            # 본문 내용 구성
            fake_content = (
                f"안녕하세요! 최근에 다녀온 후기 남겨봅니다.\n\n"
                f"{random.choice(meta['reviews'])}\n\n"
                f"{fake.sentence(nb_words=6)} 다음에 또 가보고 싶네요."
            )

            posts.append(
                models.Post(
                    pk_post_id=i,
                    fk_category_id=category_id,
                    title=title,
                    content=fake_content,
                    password=str(random.randint(1000, 9999)),
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
                    content=random.choice(SAMPLE_COMMENTS),
                    password=str(random.randint(1000, 9999)),
                )
            )

        db.add_all(comments)

    db.commit()


# -----------------------------------------------------------
# faker 자체만 사용하면, 비즈니스 문구들 위주로 데이터를 생성해서 우선 주석 처리
# import random

# from faker import Faker
# from sqlalchemy.orm import Session

# from ..models import models

# # 한국어 설정 유지
# fake = Faker("ko_KR")


# def seed_initial_data(db: Session):
#     # ------------------------
#     # Category
#     # ------------------------
#     if not db.query(models.Category).first():
#         categories = [
#             models.Category(pk_category_id=1, name="여행"),
#             models.Category(pk_category_id=2, name="문화"),
#             models.Category(pk_category_id=3, name="맛집"),
#             models.Category(pk_category_id=4, name="카페"),
#             models.Category(pk_category_id=5, name="축제"),
#             models.Category(pk_category_id=6, name="쇼핑"),
#         ]

#         db.add_all(categories)
#         db.flush()

#     # ------------------------
#     # Post
#     # ------------------------
#     if not db.query(models.Post).first():
#         posts = []
#         POST_COUNT = 100

#         for i in range(1, POST_COUNT + 1):
#             # catch_phrase 3개를 생성해 줄바꿈(\n)으로 이어 붙여서 본문처럼 만듭니다.
#             fake_content = "\n".join([fake.catch_phrase() for _ in range(3)])

#             posts.append(
#                 models.Post(
#                     pk_post_id=i,
#                     fk_category_id=random.randint(1, 6),
#                     title=fake.catch_phrase(),  # sentence 대신 한국어 문구 사용
#                     content=fake_content,       # paragraphs 대신 한국어 문구 조합 사용
#                     password=str(random.randint(1000, 9999)),  # 숫자 -> 문자열로 안전하게 변환
#                     likes=random.randint(0, 300),
#                 )
#             )

#         db.add_all(posts)
#         db.flush()

#     # ------------------------
#     # Comment
#     # ------------------------
#     if not db.query(models.Comment).first():
#         comments = []
#         COMMENT_COUNT = 500

#         for i in range(1, COMMENT_COUNT + 1):
#             comments.append(
#                 models.Comment(
#                     pk_comment_id=i,
#                     fk_post_id=random.randint(1, POST_COUNT),
#                     content=fake.catch_phrase(),  # 댓글 역시 어색한 라틴어 대신 한국어 문구 적용
#                     password=str(random.randint(1000, 9999)),  # 숫자 -> 문자열 변환
#                 )
#             )

#         db.add_all(comments)

#     db.commit()