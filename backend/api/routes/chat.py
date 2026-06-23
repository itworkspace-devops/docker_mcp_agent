from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from backend.database.repository import (
    get_chat_sessions,
    get_chat_messages,
    save_chat_message,
)

router = APIRouter()

class ChatMessageSchema(BaseModel):
    role: str
    content: str
    created_at: datetime

class ChatSessionSchema(BaseModel):
    id: str
    title: str
    created_at: datetime

@router.get("/sessions", response_model=List[ChatSessionSchema])
def list_sessions():
    return get_chat_sessions()

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageSchema])
def list_messages(session_id: str):
    return get_chat_messages(session_id)

@router.post("/sessions/{session_id}/messages")
def add_message(session_id: str, payload: dict):
    # This is mainly for manual saves if needed, but Agent API will usually handle this
    return save_chat_message(
        session_id,
        payload["role"],
        payload["content"],
        payload.get("title")
    )
