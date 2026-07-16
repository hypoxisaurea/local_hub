import json
import sys
from itertools import islice
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.AI.app.chatbot.llm.client import get_chat_model
from backend.app.db.base import Base, SessionLocal, engine
from backend.app.models import models


BATCH_SIZE = 5


def chunked(items, size):
    iterator = iter(items)
    while chunk := list(islice(iterator, size)):
        yield chunk


def extract_json(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object in model response")
    return json.loads(text[start : end + 1])


def translate_batch(model, posts: list[models.Post]) -> dict[int, dict[str, str]]:
    payload = [
        {
            "id": post.pk_post_id,
            "title": post.title,
            "content": post.content or "",
        }
        for post in posts
    ]
    response = model.invoke(
        [
            (
                "system",
                "Translate Korean community posts into natural English. "
                "Return valid JSON only in this shape: "
                '{"items":[{"id":1,"title":"...","content":"..."}]}. '
                "Escape all quotation marks and newline characters correctly. "
                "Keep every id. Do not summarize or add information.",
            ),
            ("human", json.dumps({"items": payload}, ensure_ascii=False)),
        ]
    )
    data = extract_json(str(response.content))
    translations: dict[int, dict[str, str]] = {}
    for item in data.get("items", []):
        post_id = int(item["id"])
        translations[post_id] = {
            "title": str(item.get("title") or "").strip(),
            "content": str(item.get("content") or "").strip(),
        }
    return translations


def main():
    Base.metadata.create_all(bind=engine)
    model = get_chat_model()
    if model is None:
        raise RuntimeError("OpenAI API key is not configured.")

    db = SessionLocal()
    try:
        posts = (
            db.query(models.Post)
            .join(models.PostEn, models.Post.pk_post_id == models.PostEn.pk_post_id)
            .filter(models.Post.title == models.PostEn.title)
            .order_by(models.Post.pk_post_id)
            .all()
        )
        updated = 0

        for batch_index, batch in enumerate(chunked(posts, BATCH_SIZE), start=1):
            translations = translate_batch(model, batch)

            for post in batch:
                translated = translations.get(post.pk_post_id)
                if not translated:
                    raise RuntimeError(f"Missing translation for post {post.pk_post_id}")

                post_en = (
                    db.query(models.PostEn)
                    .filter(models.PostEn.pk_post_id == post.pk_post_id)
                    .first()
                )
                if post_en is None:
                    post_en = models.PostEn(pk_post_id=post.pk_post_id)
                    db.add(post_en)

                post_en.fk_category_id = post.fk_category_id
                post_en.title = translated["title"] or post.title
                post_en.content = translated["content"] or (post.content or "")
                post_en.likes = post.likes
                post_en.password = post.password
                if post.created_at is not None:
                    post_en.created_at = post.created_at
                updated += 1

            db.commit()
            print(f"batch {batch_index} committed ({updated}/{len(posts)})")

        print(f"done {updated}/{len(posts)}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
