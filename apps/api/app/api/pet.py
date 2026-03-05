# 宠物系统 API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.services import pet_service

router = APIRouter(prefix="/pet", tags=["宠物系统"])


@router.get("/status", response_model=Dict[str, Any])
async def get_pet_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取宠物状态"""
    status = await pet_service.get_pet_status(db, current_user.id)
    return status


@router.post("/create", response_model=Dict[str, Any])
async def create_pet(
    pet_type: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建宠物"""
    pet = await pet_service.get_pet(db, current_user.id)
    if pet:
        raise HTTPException(status_code=400, detail="已有宠物，无需重复创建")
    
    pet = await pet_service.create_pet(db, current_user.id, pet_type)
    return {
        "status": "success",
        "message": "宠物创建成功",
        "pet": {
            "id": pet.id,
            "name": pet.name,
            "type": pet.pet_type,
            "level": pet.level
        }
    }


@router.post("/interact", response_model=Dict[str, Any])
async def interact_with_pet(
    action: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """与宠物互动"""
    result = await pet_service.interact(db, current_user.id, action)
    return result


@router.get("/types", response_model=Dict[str, Any])
async def get_pet_types():
    """获取所有宠物类型"""
    return {
        "types": pet_service.get_all_pet_types()
    }
