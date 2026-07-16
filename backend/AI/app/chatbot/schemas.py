from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"] = "user"
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: list[ChatMessage] = Field(default_factory=list)
    language: str | None = Field(default=None, description="Preferred response language.")


class ChatSource(BaseModel):
    type: str
    title: str
    address: str | None = None
    tel: str | None = None
    image: str | None = None
    mapx: str | None = None
    mapy: str | None = None
    contentid: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    answer: str
    route: str
    sources: list[ChatSource] = Field(default_factory=list)
