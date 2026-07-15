from app.chatbot.config import get_settings
from app.chatbot.graph.routing import classify_route
from app.chatbot.graph.state import ChatbotState
from app.chatbot.llm.client import get_chat_model
from app.chatbot.llm.prompts import answer_prompt
from app.chatbot.services.answer_formatter import fallback_answer, format_context, source_from_document
from app.chatbot.services.community_search import search_community_posts
from app.chatbot.services.local_search import search_local_data
from app.chatbot.services.generate_sql import execute_sql, format_db_result, generate_sql_from_text


async def classify_query(state: ChatbotState) -> ChatbotState:
    return {"route": classify_route(state["message"])}


async def text2sql_query(state: ChatbotState) -> ChatbotState:
    sql = await generate_sql_from_text(state["message"])
    return {"db_query_sql": sql}


async def execute_db_query(state: ChatbotState) -> ChatbotState:
    try:
        result = await execute_sql(state["db_query_sql"])
        return {"db_results": result}
    except Exception as e:
        return {"db_error": str(e)}


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


async def generate_answer(state: ChatbotState) -> ChatbotState:
    route = state.get("route", "general")

    if route == "db":
        if state.get("db_error"):
            return {"answer": f"DB 조회 중 오류가 발생했습니다: {state['db_error']}"}
        rows = state.get("db_results", [])
        return {"answer": format_db_result(state["message"], rows)}

    docs = state.get("local_docs", [])
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