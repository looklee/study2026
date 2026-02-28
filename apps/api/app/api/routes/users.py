from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.models import User, LearningPath
from app.schemas import (
    UserCreate, UserResponse, UserUpdate,
    LearningPathGenerate, LearningPathResponse,
    MessageResponse
)
from app.services import user_service, path_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    user = await user_service.create_user(db, user_data)
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user(db: AsyncSession = Depends(get_db)):
    """获取当前用户"""
    # TODO: 添加 JWT 认证
    user = await user_service.get_user_by_id(db, 1)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/me", response_model=UserResponse)
async def update_user(user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    """更新用户信息"""
    user = await user_service.update_user(db, 1, user_data)
    return user


@router.post("/paths/generate", response_model=LearningPathResponse)
async def generate_learning_path(
    path_data: LearningPathGenerate,
    db: AsyncSession = Depends(get_db)
):
    """AI 生成学习路径"""
    learning_path = await path_service.generate_path(db, path_data, user_id=1)
    return learning_path


@router.get("/paths", response_model=List[LearningPathResponse])
async def list_paths(db: AsyncSession = Depends(get_db)):
    """获取用户的学习路径列表"""
    paths = await path_service.list_paths(db, user_id=1)
    return paths


@router.get("/paths/{path_id}", response_model=LearningPathResponse)
async def get_path(path_id: int, db: AsyncSession = Depends(get_db)):
    """获取学习路径详情"""
    path = await path_service.get_path(db, path_id)
    if not path:
        raise HTTPException(status_code=404, detail="路径不存在")
    return path
