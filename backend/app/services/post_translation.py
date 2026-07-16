import json
import re

from backend.AI.app.chatbot.llm.client import get_chat_model


def _extract_json(text: str) -> dict[str, str] | None:
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None

    if not isinstance(data, dict):
        return None
    return {
        "title": str(data.get("title") or "").strip(),
        "content": str(data.get("content") or "").strip(),
    }


def translate_post_to_english(title: str, content: str | None) -> dict[str, str]:
    source_content = content or ""
    fallback = {"title": title, "content": source_content}

    model = get_chat_model()
    if model is None:
        return fallback

    try:
        response = model.invoke(
            [
                (
                    "system",
                    "Translate Korean community posts into natural English. "
                    "Return JSON only with keys title and content. "
                    "Do not summarize, censor, or add new information.",
                ),
                (
                    "human",
                    json.dumps(
                        {"title": title, "content": source_content},
                        ensure_ascii=False,
                    ),
                ),
            ]
        )
    except Exception:
        return fallback

    translated = _extract_json(str(response.content))
    if not translated:
        return fallback

    return {
        "title": translated["title"] or title,
        "content": translated["content"] or source_content,
    }
