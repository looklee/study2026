# 学习进度 API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List
from datetime import datetime, timedelta
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, LearningPath, ProgressRecord

router = APIRouter(prefix="/progress", tags=["学习进度"])


@router.get("/summary", response_model=Dict[str, Any])
async def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取学习进度汇总"""
    # 总学习时长
    result = await db.execute(
        select(func.sum(ProgressRecord.duration_minutes))
        .where(ProgressRecord.user_id == current_user.id)
    )
    total_minutes = result.scalar() or 0
    
    # 学习路径进度
    result = await db.execute(
        select(LearningPath).where(LearningPath.user_id == current_user.id)
    )
    paths = result.scalars().all()
    
    path_progress = [
        {
            "id": path.id,
            "name": path.name,
            "progress": path.progress_percentage,
            "status": path.status
        }
        for path in paths
    ]
    
    # 最近学习记录
    result = await db.execute(
        select(ProgressRecord)
        .where(ProgressRecord.user_id == current_user.id)
        .order_by(ProgressRecord.learned_at.desc())
        .limit(10)
    )
    recent_records = result.scalars().all()
    
    return {
        "total_learning_minutes": total_minutes,
        "total_learning_hours": round(total_minutes / 60, 2),
        "paths": path_progress,
        "recent_activity": [
            {
                "id": record.id,
                "activity_type": record.activity_type,
                "duration_minutes": record.duration_minutes,
                "learned_at": record.learned_at.isoformat() if record.learned_at else None
            }
            for record in recent_records
        ]
    }


@router.post("/record", response_model=Dict[str, Any])
async def record_learning_activity(
    activity_type: str,
    duration_minutes: int,
    description: str = None,
    path_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """记录学习活动"""
    record = ProgressRecord(
        user_id=current_user.id,
        activity_type=activity_type,
        duration_minutes=duration_minutes,
        description=description,
        path_id=path_id,
        learned_at=datetime.now()
    )
    
    db.add(record)
    await db.commit()
    await db.refresh(record)
    
    # 更新学习路径进度
    if path_id:
        result = await db.execute(
            select(LearningPath).where(LearningPath.id == path_id)
        )
        path = result.scalar_one_or_none()
        if path and path.user_id == current_user.id:
            # 简化：每次增加 5% 进度
            path.progress_percentage = min(100, path.progress_percentage + 5)
            if path.progress_percentage >= 100:
                path.status = "completed"
            await db.commit()
    
    return {
        "status": "success",
        "message": "学习活动已记录",
        "record": {
            "id": record.id,
            "activity_type": record.activity_type,
            "duration_minutes": record.duration_minutes,
            "learned_at": record.learned_at.isoformat()
        }
    }


@router.get("/paths", response_model=Dict[str, Any])
async def get_learning_paths(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的学习路径"""
    result = await db.execute(
        select(LearningPath).where(LearningPath.user_id == current_user.id)
    )
    paths = result.scalars().all()
    
    return {
        "paths": [
            {
                "id": path.id,
                "name": path.name,
                "description": path.description,
                "progress": path.progress_percentage,
                "status": path.status,
                "created_at": path.created_at.isoformat() if path.created_at else None
            }
            for path in paths
        ],
        "total": len(paths)
    }


@router.post("/paths", response_model=Dict[str, Any])
async def create_learning_path(
    name: str,
    description: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建学习路径"""
    path = LearningPath(
        user_id=current_user.id,
        name=name,
        description=description,
        progress_percentage=0,
        status="in_progress"
    )
    
    db.add(path)
    await db.commit()
    await db.refresh(path)
    
    return {
        "status": "success",
        "message": "学习路径创建成功",
        "path": {
            "id": path.id,
            "name": path.name,
            "description": path.description,
            "progress": path.progress_percentage
        }
    }


@router.get("/stats", response_model=Dict[str, Any])
async def get_learning_stats(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取学习统计"""
    from_date = datetime.now() - timedelta(days=days)
    
    # 每日学习时长
    result = await db.execute(
        select(
            func.date(ProgressRecord.learned_at).label("date"),
            func.sum(ProgressRecord.duration_minutes).label("total_minutes")
        )
        .where(
            ProgressRecord.user_id == current_user.id,
            ProgressRecord.learned_at >= from_date
        )
        .group_by(func.date(ProgressRecord.learned_at))
    )
    daily_stats = result.all()
    
    return {
        "period_days": days,
        "daily_stats": [
            {
                "date": str(date),
                "minutes": minutes or 0
            }
            for date, minutes in daily_stats
        ]
    }
