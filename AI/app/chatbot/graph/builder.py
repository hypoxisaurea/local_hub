from langgraph.graph import END, START, StateGraph

from app.chatbot.graph.nodes import (
    classify_query,
    execute_db_query,
    generate_answer,
    retrieve_community,
    retrieve_local,
    text2sql_query,
)
from app.chatbot.graph.routing import next_node_for_route
from app.chatbot.graph.state import ChatbotState


def build_chatbot_graph():
    graph = StateGraph(ChatbotState)

    graph.add_node("classify_query", classify_query)
    graph.add_node("text2sql_query", text2sql_query)
    graph.add_node("execute_db_query", execute_db_query)
    graph.add_node("retrieve_local", retrieve_local)
    graph.add_node("retrieve_community", retrieve_community)
    graph.add_node("generate_answer", generate_answer)

    graph.add_edge(START, "classify_query")

    graph.add_conditional_edges(
        "classify_query",
        next_node_for_route,
        {
            "db": "text2sql_query",
            "retrieve_local": "retrieve_local",
            "retrieve_community": "retrieve_community",
            "generate_answer": "generate_answer",
        },
    )

    graph.add_edge("text2sql_query", "execute_db_query")
    graph.add_edge("execute_db_query", "generate_answer")
    graph.add_edge("retrieve_local", "generate_answer")
    graph.add_edge("retrieve_community", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()

chatbot_graph = build_chatbot_graph()