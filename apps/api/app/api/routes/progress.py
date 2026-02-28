# 学习进度 API 端点

from fastapi import APIRouter
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import datetime

router = APIRouter()

class ProgressTrackRequest(BaseModel):
    """进度追踪请求"""
    userId: str
    pathId: str
    action: str = "update"
    itemType: str = "topic"
    itemId: str
    completed: bool = False
    timeSpentMinutes: int = 0
    notes: str = ""

class ProgressQueryRequest(BaseModel):
    """进度查询请求"""
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = 10

@router.get("/api/v1/progress/stats/{user_id}")
async def get_progress_stats(user_id: str):
    """获取进度统计"""
    from app.progress_engine import progress_engine
    
    result = progress_engine.get_user_stats(user_id)
    return result

@router.get("/api/v1/progress/{user_id}")
async def get_user_progress(user_id: str, path_id: Optional[str] = None):
    """获取用户进度"""
    from app.progress_engine import progress_engine
    
    result = progress_engine.get_user_progress(user_id, path_id)
    return result

@router.post("/api/v1/progress/track")
async def track_progress(request: ProgressTrackRequest):
    """追踪学习进度"""
    from app.progress_engine import progress_engine
    
    result = await progress_engine.track_progress(
        user_id=request.userId,
        path_id=request.path_id,
        data={
            "action": request.action,
            "item_type": request.itemType,
            "item_id": request.itemId,
            "completed": request.completed,
            "time_spent_minutes": request.timeSpentMinutes,
            "notes": request.notes
        }
    )
    
    return result

@router.get("/api/v1/progress/{user_id}/achievements")
async def get_achievements(user_id: str):
    """获取用户成就"""
    from app.progress_engine import progress_engine
    
    result = progress_engine.get_achievements(user_id)
    return result

@router.get("/api/v1/progress/{user_id}/timeline")
async def get_activity_timeline(user_id: str, days: int = 30):
    """获取活动时间线"""
    from app.progress_engine import progress_engine
    
    result = progress_engine.get_activity_timeline(user_id, days)
    return result

@router.get("/api/v1/progress/streak/{user_id}")
async def get_streak(user_id: str):
    """获取连续学习天数"""
    from app.progress_engine import progress_engine
    
    if user_id not in progress_engine.user_stats:
        return {"status": "success", "streak": 0, "longest_streak": 0}
    
    stats = progress_engine.user_stats[user_id]
    return {
        "status": "success",
        "streak": stats["current_streak"],
        "longest_streak": stats["longest_streak"]
    }
