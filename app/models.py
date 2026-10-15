from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant"]
    text: str = Field(min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[Message] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    emergency: bool
