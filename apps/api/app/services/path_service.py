from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime
from app.models import LearningPath
from app.schemas import LearningPathGenerate
from app.services.ai_service import generate_path_with_ai


async def generate_path(
    db: AsyncSession,
    path_data: LearningPathGenerate,
    user_id: int
) -> LearningPath:
    """AI 生成学习路径"""
    
    # 调用 AI 服务生成路径
    ai_response = await generate_path_with_ai(path_data)
    
    # 创建学习路径
    learning_path = LearningPath(
        user_id=user_id,
        path_name=ai_response.get("pathName", "自定义学习路径"),
        description=ai_response.get("description", ""),
        target_goal=path_data.targetGoal,
        total_duration=ai_response.get("totalDuration", "12 周"),
        path_data=ai_response,
        status="active",
        current_phase=0,
        overall_progress=0,
        started_at=datetime.utcnow()
    )
    
    # 计算预估结束日期
    if path_data.deadline:
        learning_path.estimated_end_date = datetime.fromisoformat(path_data.deadline)
    else:
        # 根据持续时间计算
        weeks = int(ai_response.get("totalDuration", "12").replace("周", ""))
        from datetime import timedelta
        learning_path.estimated_end_date = datetime.utcnow() + timedelta(weeks=weeks)
    
    db.add(learning_path)
    await db.commit()
    await db.refresh(learning_path)
    
    return learning_path


async def list_paths(db: AsyncSession, user_id: int) -> List[LearningPath]:
    """获取用户的学习路径列表"""
    result = await db.execute(
        select(LearningPath)
        .where(LearningPath.user_id == user_id)
        .order_by(LearningPath.created_at.desc())
    )
    return result.scalars().all()


async def get_path(db: AsyncSession, path_id: int) -> LearningPath | None:
    """获取学习路径详情"""
    result = await db.execute(
        select(LearningPath).where(LearningPath.id == path_id)
    )
    return result.scalar_one_or_none()


async def update_progress(db: AsyncSession, path_id: int, progress: int) -> LearningPath:
    """更新路径进度"""
    path = await get_path(db, path_id)
    if not path:
        raise ValueError("路径不存在")
    
    path.overall_progress = progress
    await db.commit()
    await db.refresh(path)
    return path
