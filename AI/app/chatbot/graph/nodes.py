from app.chatbot.config import get_settings
from app.chatbot.graph.routing import classify_route
from app.chatbot.graph.state import ChatbotState
from app.chatbot.llm.client import get_chat_model
from app.chatbot.llm.prompts import answer_prompt
from app.chatbot.services.answer_formatter import fallback_answer, format_context, source_from_document
from app.chatbot.services.community_search import search_community_posts
from app.chatbot.services.local_search import search_local_data


async def classify_query(state: ChatbotState) -> ChatbotState:
    return {"route": classify_route(state["message"])}


async def retrieve_local(state: ChatbotState) -> ChatbotState:
    settings = get_settings()
    docs = search_local_data(state["message"], limit=settings.max_context_items)
    return {
        "local_docs": docs,
        "sources": [source_from_document(doc) for doc in docs[: settings.max_search_results]],
    }


async def retrieve_community(state: ChatbotState) -> ChatbotState:
    docs = await search_community_posts(state["message"])
    return {"community_docs": docs, "sources": []}


def _format_history(history: list | None) -> str:
    if not history:
        return "No previous conversation."

    lines: list[str] = []
    for item in history[-6:]:
        if isinstance(item, dict):
            role = item.get("role", "user")
            content = item.get("content", "")
        else:
            role = getattr(item, "role", "user")
            content = getattr(item, "content", "")
        if content:
            lines.append(f"{role}: {content}")
    return "\n".join(lines) if lines else "No previous conversation."


async def generate_answer(state: ChatbotState) -> ChatbotState:
    docs = state.get("local_docs", [])
    route = state.get("route", "general")
    model = get_chat_model()

    if route == "community" and not state.get("community_docs"):
        return {"answer": fallback_answer(state["message"], route, docs, state.get("language"))}

    if model is None:
        return {"answer": fallback_answer(state["message"], route, docs, state.get("language"))}

    chain = answer_prompt | model
    response = await chain.ainvoke(
        {
            "message": state["message"],
            "route": route,
            "context": format_context(docs),
            "history": _format_history(state.get("history")),
        }
    )
    return {"answer": response.content}
