from fastapi import APIRouter

from app.chatbot.graph.builder import chatbot_graph
from app.chatbot.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chatbot"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await chatbot_graph.ainvoke({
        "message": request.message,
        "history": request.history,
        "language": request.language,
    })

    return ChatResponse(
        answer=result["answer"],
        route=result["route"],
        sources=result.get("sources", []),
    )
