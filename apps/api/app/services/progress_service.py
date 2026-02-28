from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from app.models import ProgressRecord, User
from app.schemas import ProgressTrack
import json


async def track_progress(db: AsyncSession, progress_data: ProgressTrack) -> dict:
    """追踪学习进度"""
    
    # 创建进度记录
    record = ProgressRecord(
        user_id=progress_data.userId,
        path_id=progress_data.pathId,
        item_type=progress_data.itemType,
        item_id=progress_data.itemId,
        action=progress_data.action,
        completed=progress_data.action == "complete",
        progress_data=progress_data.metadata
    )
    
    db.add(record)
    await db.commit()
    
    # 计算统计数据
    stats = await get_user_stats(db, progress_data.userId, progress_data.pathId)
    
    # 生成激励消息
    motivation = generate_motivation(stats["progress"]["overall"])
    
    # 计算连续天数
    streak = await calculate_streak(db, progress_data.userId)
    
    # 成就检查
    achievements = check_achievements(stats["progress"]["overall"])
    
    return {
        "status": "success",
        "progress": stats["progress"],
        "statistics": stats["statistics"],
        "achievements": achievements,
        "motivation": motivation,
        "streak": streak
    }


async def get_user_stats(db: AsyncSession, user_id: int, path_id: int = None) -> dict:
    """获取用户统计"""
    
    # 基础查询
    query = select(ProgressRecord).where(ProgressRecord.user_id == user_id)
    
    if path_id:
        query = query.where(ProgressRecord.path_id == path_id)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    total_items = len(records)
    completed_items = sum(1 for r in records if r.completed)
    progress_percentage = int((completed_items / total_items * 100)) if total_items > 0 else 0
    
    # 按类型分组
    by_type = {}
    for record in records:
        item_type = record.item_type
        if item_type not in by_type:
            by_type[item_type] = {"total": 0, "completed": 0}
        by_type[item_type]["total"] += 1
        if record.completed:
            by_type[item_type]["completed"] += 1
    
    # 计算学习时间
    if records:
        start_date = min(r.created_at for r in records)
        total_days = (datetime.utcnow() - start_date).days + 1
        avg_per_week = int((completed_items / total_days) * 7)
    else:
        start_date = datetime.utcnow()
        total_days = 0
        avg_per_week = 0
    
    return {
        "progress": {
            "overall": progress_percentage,
            "completedItems": completed_items,
            "totalItems": total_items,
            "byType": by_type
        },
        "statistics": {
            "startDate": start_date.isoformat(),
            "totalDays": total_days,
            "averagePerWeek": avg_per_week,
            "estimatedCompletionDate": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
    }


async def calculate_streak(db: AsyncSession, user_id: int) -> int:
    """计算连续学习天数"""
    
    # 获取最近的学习记录日期
    result = await db.execute(
        select(func.date(ProgressRecord.created_at))
        .where(ProgressRecord.user_id == user_id)
        .distinct()
        .order_by(func.date(ProgressRecord.created_at).desc())
    )
    
    dates = [row[0] for row in result.all()]
    if not dates:
        return 0
    
    streak = 1
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    if dates[0] != today and dates[0] != yesterday:
        return 0
    
    for i in range(1, len(dates)):
        if (dates[i-1] - dates[i]).days == 1:
            streak += 1
        else:
            break
    
    return streak


async def daily_check_in(db: AsyncSession, user_id: int, minutes_studied: int):
    """每日打卡"""
    # 实现打卡逻辑
    pass


def generate_motivation(progress: int) -> str:
    """生成激励消息"""
    messages = [
        (0, "🌱 开始你的学习之旅吧！"),
        (25, "💪 不错的开始，继续保持！"),
        (50, "🎯 已经过半了，加油！"),
        (75, "🔥 胜利在望，冲刺！"),
        (100, "🏆 恭喜完成！你是最棒的！")
    ]
    
    for threshold, message in reversed(messages):
        if progress >= threshold:
            return message
    return messages[0][1]


def check_achievements(progress: int) -> list:
    """检查成就"""
    all_achievements = [
        {"id": "first_step", "name": "第一步", "unlocked": progress >= 1},
        {"id": "quarter_way", "name": "四分之一", "unlocked": progress >= 25},
        {"id": "halfway", "name": "半途", "unlocked": progress >= 50},
        {"id": "almost_there", "name": "指日可待", "unlocked": progress >= 75},
        {"id": "champion", "name": "冠军", "unlocked": progress >= 100}
    ]
    return all_achievements
