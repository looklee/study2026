# 聊天 API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Conversation
from app.services.ai_service import get_ai_service

router = APIRouter(prefix="/chat", tags=["AI 聊天"])


@router.post("/message", response_model=Dict[str, Any])
async def send_message(
    message: str,
    conversation_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发送消息并获取 AI 回复"""
    ai_service = get_ai_service()
    
    # 创建或获取会话
    if not conversation_id:
        conversation = Conversation(
            user_id=current_user.id,
            title=message[:50] + "..." if len(message) > 50 else message
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        conversation_id = conversation.id
    else:
        from sqlalchemy import select
        result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
        conversation = result.scalar_one_or_none()
        if not conversation or conversation.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="会话不存在")
    
    # 调用 AI 服务
    response = await ai_service.chat(
        message=message,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    
    return {
        "status": "success",
        "conversation_id": conversation_id,
        "user_message": message,
        "ai_response": response.get("response", ""),
        "model": response.get("model", "default"),
        "timestamp": datetime.now().isoformat()
    }


@router.get("/conversations", response_model=Dict[str, Any])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的会话列表"""
    from sqlalchemy import select
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().all()
    
    return {
        "conversations": [
            {
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at.isoformat() if conv.created_at else None,
                "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
                "message_count": conv.message_count
            }
            for conv in conversations
        ],
        "total": len(conversations)
    }


@router.get("/conversations/{conversation_id}", response_model=Dict[str, Any])
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取会话详情"""
    from sqlalchemy import select
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
        "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
        "message_count": conversation.message_count
    }


@router.delete("/conversations/{conversation_id}", response_model=Dict[str, Any])
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除会话"""
    from sqlalchemy import select, delete
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    await db.delete(conversation)
    await db.commit()
    
    return {
        "status": "success",
        "message": "会话已删除"
    }
