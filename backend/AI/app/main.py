from fastapi import FastAPI

from .chatbot.router import router as chatbot_router


app = FastAPI(title="Local Hub Backend")

app.include_router(chatbot_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
