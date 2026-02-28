from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import ChatMessage, ChatResponse
from app.services import chat_service

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(
    message_data: ChatMessage,
    db: AsyncSession = Depends(get_db)
):
    """发送消息给 AI 导师"""
    response = await chat_service.send_message(db, message_data)
    return response


@router.get("/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取对话历史"""
    history = await chat_service.get_conversation(db, conversation_id)
    return {"conversationId": conversation_id, "messages": history}


@router.get("/user/{user_id}/conversations")
async def list_conversations(
    user_id: int,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """获取用户的对话列表"""
    conversations = await chat_service.list_conversations(db, user_id, limit)
    return conversations
