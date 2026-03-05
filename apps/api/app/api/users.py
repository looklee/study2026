# 用户管理 API

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any, Dict, List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, UserBadge, Pet, CheckinRecord
from app.services import pet_service, checkin_service

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/me", response_model=Dict[str, Any])
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户资料"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "avatar_url": current_user.avatar_url,
        "bio": current_user.bio,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "is_active": current_user.is_active
    }


@router.put("/me", response_model=Dict[str, Any])
async def update_user_profile(
    username: str = None,
    bio: str = None,
    avatar_url: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户资料"""
    if username:
        # 检查用户名是否已被占用
        result = await db.execute(select(User).where(User.username == username, User.id != current_user.id))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="用户名已被占用")
        current_user.username = username
    
    if bio:
        current_user.bio = bio
    
    if avatar_url:
        current_user.avatar_url = avatar_url
    
    await db.commit()
    await db.refresh(current_user)
    
    return {
        "status": "success",
        "message": "资料更新成功",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "avatar_url": current_user.avatar_url,
            "bio": current_user.bio
        }
    }


@router.get("/me/stats", response_model=Dict[str, Any])
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户统计信息"""
    # 获取宠物信息
    pet = await pet_service.get_pet(db, current_user.id)
    
    # 获取签到信息
    checkin_info = await checkin_service.get_user_checkin_info(db, current_user.id)
    
    # 获取徽章
    result = await db.execute(select(UserBadge).where(UserBadge.user_id == current_user.id))
    badges = result.scalars().all()
    
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "pet": {
            "id": pet.id,
            "name": pet.name,
            "type": pet.pet_type,
            "level": pet.level,
            "exp": pet.exp,
            "happiness": pet.happiness,
            "energy": pet.energy
        } if pet else None,
        "checkin": {
            "total_days": checkin_info.get("total_days", 0),
            "current_streak": checkin_info.get("current_streak", 0),
            "longest_streak": checkin_info.get("longest_streak", 0)
        },
        "badges": [
            {
                "id": badge.id,
                "name": badge.badge_name,
                "description": badge.description,
                "earned_at": badge.earned_at.isoformat() if badge.earned_at else None
            }
            for badge in badges
        ]
    }


@router.get("/me/badges", response_model=Dict[str, Any])
async def get_user_badges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户徽章列表"""
    result = await db.execute(
        select(UserBadge).where(UserBadge.user_id == current_user.id)
    )
    badges = result.scalars().all()
    
    return {
        "badges": [
            {
                "id": badge.id,
                "name": badge.badge_name,
                "description": badge.description,
                "icon": badge.icon_url,
                "earned_at": badge.earned_at.isoformat() if badge.earned_at else None
            }
            for badge in badges
        ],
        "total": len(badges)
    }
