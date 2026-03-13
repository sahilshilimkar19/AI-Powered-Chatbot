from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str  # "user", "assistant", or "system"
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    stream: bool = True


class ChatResponse(BaseModel):
    role: str
    content: str


class KnowledgeEntry(BaseModel):
    question: str
    answer: str


class HealthResponse(BaseModel):
    status: str
    model: str
