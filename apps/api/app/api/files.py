# 文件上传 API

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.services.file_storage import (
    save_file,
    list_user_files,
    delete_file,
    get_file
)

router = APIRouter(prefix="/files", tags=["文件管理"])


@router.post("/upload", response_model=Dict[str, Any])
async def upload_file(
    file: UploadFile = File(...),
    category: str = "general",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """上传文件"""
    result = await save_file(file, current_user.id, category, db)
    return {
        "status": "success",
        "message": "文件上传成功",
        "file": result
    }


@router.get("/list", response_model=Dict[str, Any])
async def list_files(
    category: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """列出用户文件"""
    files = await list_user_files(current_user.id, category, db)
    return {
        "files": files,
        "total": len(files)
    }


@router.delete("/{file_id}", response_model=Dict[str, Any])
async def delete_file_by_id(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除文件"""
    success = await delete_file(file_id, current_user.id, db)
    if success:
        return {"status": "success", "message": "文件已删除"}
    else:
        raise HTTPException(status_code=404, detail="文件不存在或无权限")
