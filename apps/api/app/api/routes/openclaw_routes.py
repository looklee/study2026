"""
OpenClaw API 路由
提供OpenClaw AI助手功能的HTTP接口
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from app.services.openclaw_service import get_openclaw_service, OpenClawService


router = APIRouter(prefix="/openclaw", tags=["openclaw"])


class ProcessRequest(BaseModel):
    """处理请求模型"""
    input_text: str
    context: Optional[Dict[str, Any]] = None


class SkillExecutionRequest(BaseModel):
    """技能执行请求模型"""
    skill_name: str
    params: Dict[str, Any]


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    conversation_id: Optional[str] = None


@router.post("/process")
async def process_request(
    request: ProcessRequest,
    openclaw_service: OpenClawService = Depends(get_openclaw_service)
):
    """
    处理用户请求
    """
    try:
        result = await openclaw_service.process_request(
            user_input=request.input_text,
            context=request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute-skill")
async def execute_skill(
    request: SkillExecutionRequest,
    openclaw_service: OpenClawService = Depends(get_openclaw_service)
):
    """
    执行特定技能
    """
    try:
        result = await openclaw_service.execute_skill(
            skill_name=request.skill_name,
            params=request.params
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/skills")
async def get_available_skills(
    openclaw_service: OpenClawService = Depends(get_openclaw_service)
):
    """
    获取可用技能列表
    """
    try:
        skills = await openclaw_service.get_available_skills()
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat_with_memory(
    request: ChatRequest,
    openclaw_service: OpenClawService = Depends(get_openclaw_service)
):
    """
    带记忆的对话
    """
    try:
        result = await openclaw_service.chat_with_memory(
            user_message=request.message,
            conversation_id=request.conversation_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy", "service": "openclaw"}