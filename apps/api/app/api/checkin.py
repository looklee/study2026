# 签到系统 API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.services import checkin_service

router = APIRouter(prefix="/checkin", tags=["签到系统"])


@router.post("/daily", response_model=Dict[str, Any])
async def daily_checkin(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """每日签到"""
    result = await checkin_service.check_in(db, current_user.id, current_user.username)
    return result


@router.get("/info", response_model=Dict[str, Any])
async def get_checkin_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取签到信息"""
    info = await checkin_service.get_user_checkin_info(db, current_user.id)
    return info


@router.get("/stats", response_model=Dict[str, Any])
async def get_checkin_stats(
    db: AsyncSession = Depends(get_db)
):
    """获取全局签到统计"""
    stats = await checkin_service.get_checkin_stats(db)
    return stats
