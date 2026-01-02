from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    message: str
    selected_text: Optional[str] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[str]


class WebSocketMessage(BaseModel):
    type: str
    content: Optional[str] = None
    conversation_id: Optional[str] = None
    selected_text: Optional[str] = None


class WebSocketResponse(BaseModel):
    type: str
    content: Optional[str] = None
    sources: Optional[List[str]] = None
    conversation_id: Optional[str] = None