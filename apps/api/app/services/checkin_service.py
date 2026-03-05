# 签到服务 - 每日签到 + Streak 追踪 (数据库版本)

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CheckinRecord, User, UserBadge
from app.services.pet_service import add_exp as pet_add_exp


def get_date_str(dt: datetime = None) -> str:
    """获取日期字符串"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d")


async def check_in(db: AsyncSession, user_id: int, username: str = "用户") -> Dict[str, Any]:
    """
    用户签到
    返回：签到结果、当前 streak、是否连续、奖励信息
    """
    today = get_date_str()
    yesterday = get_date_str(datetime.now() - timedelta(days=1))
    
    # 检查今天是否已签到
    result = await db.execute(
        select(CheckinRecord).where(
            and_(CheckinRecord.user_id == user_id, CheckinRecord.checkin_date == today)
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return {
            "status": "already_checked_in",
            "message": "今天已经签到过了，明天再来哦~",
            "streak": 0,
            "today": today
        }
    
    # 获取昨天的签到记录
    result = await db.execute(
        select(CheckinRecord)
        .where(CheckinRecord.user_id == user_id)
        .order_by(CheckinRecord.checkin_date.desc())
    )
    last_record = result.scalar_one_or_none()
    
    # 计算 streak
    if last_record and last_record.checkin_date == yesterday:
        # 连续签到
        result = await db.execute(
            select(func.count()).where(CheckinRecord.user_id == user_id)
        )
        total_checkins = result.scalar() or 0
        current_streak = total_checkins + 1
        is_continuous = True
    else:
        # 中断了，重新开始
        current_streak = 1
        is_continuous = False
    
    # 获取总签到次数
    result = await db.execute(
        select(func.count()).where(CheckinRecord.user_id == user_id)
    )
    total_checkins = result.scalar() or 0
    
    # 创建签到记录
    reward = calculate_reward(current_streak, is_continuous)
    
    checkin = CheckinRecord(
        user_id=user_id,
        checkin_date=today,
        points_earned=reward["points"],
        streak_bonus=reward.get("streak_bonus", 0)
    )
    
    db.add(checkin)
    
    # 获得徽章
    badges_earned = []
    if reward["badges"]:
        for badge_name in reward["badges"]:
            badge = UserBadge(
                user_id=user_id,
                badge_id=f"checkin_{badge_name}",
                badge_name=badge_name,
                badge_description=f"连续签到奖励",
                badge_icon="🏆",
                reason=f"连续签到{current_streak}天"
            )
            db.add(badge)
            badges_earned.append(badge_name)
    
    await db.commit()
    
    # 宠物签到奖励
    pet_result = None
    try:
        from app.services.pet_service import check_in_bonus
        pet_result = await check_in_bonus(db, user_id)
    except:
        pass
    
    # 生成消息
    messages = {
        1: "新的开始！加油！🎉",
        3: "连续 3 天！你很棒！👍",
        7: "一周坚持！获得「周勤学者」徽章！🏆",
        14: "两周不断！获得「半月达人」徽章！🥈",
        30: "月度传奇！获得「月勤学者」徽章！🥇",
        100: "百日传奇！你是真正的学习王者！👑"
    }
    
    milestone_message = messages.get(current_streak, f"连续{current_streak}天！继续保持！🔥")
    
    return {
        "status": "success",
        "message": f"签到成功！{milestone_message}",
        "streak": current_streak,
        "total_checkins": total_checkins + 1,
        "is_continuous": is_continuous,
        "reward": reward,
        "today": today,
        "badges_earned": badges_earned,
        "pet_bonus": pet_result
    }


def calculate_reward(streak: int, is_continuous: bool) -> Dict[str, Any]:
    """计算签到奖励"""
    reward = {
        "points": 10 if is_continuous else 5,
        "streak_bonus": 0,
        "badges": [],
        "items": []
    }
    
    # 连续奖励
    if streak >= 7:
        reward["badges"].append("周勤学者")
        reward["streak_bonus"] = 10
    if streak >= 14:
        reward["badges"].append("半月达人")
        reward["streak_bonus"] = 20
    if streak >= 30:
        reward["badges"].append("月勤学者")
        reward["streak_bonus"] = 50
    if streak >= 100:
        reward["badges"].append("百日传奇")
        reward["streak_bonus"] = 100
    
    # 额外点数
    reward["points"] += reward["streak_bonus"]
    
    # 特殊天数奖励
    if streak % 10 == 0:
        reward["items"].append(f"🎁 {streak}天纪念宝箱")
    
    return reward


async def get_user_checkin_info(db: AsyncSession, user_id: int) -> Dict[str, Any]:
    """获取用户签到信息"""
    today = get_date_str()
    
    # 检查今天是否已签到
    result = await db.execute(
        select(CheckinRecord).where(
            and_(CheckinRecord.user_id == user_id, CheckinRecord.checkin_date == today)
        )
    )
    today_checked = result.scalar_one_or_none() is not None
    
    # 获取总签到次数
    result = await db.execute(
        select(func.count()).where(CheckinRecord.user_id == user_id)
    )
    total_checkins = result.scalar() or 0
    
    # 获取最近签到记录
    result = await db.execute(
        select(CheckinRecord)
        .where(CheckinRecord.user_id == user_id)
        .order_by(CheckinRecord.checkin_date.desc())
    )
    records = result.scalars().all()
    
    # 计算当前 streak
    current_streak = 0
    longest_streak = 0
    if records:
        current_streak = 1
        for i in range(len(records) - 1):
            date1 = datetime.strptime(records[i].checkin_date, "%Y-%m-%d")
            date2 = datetime.strptime(records[i+1].checkin_date, "%Y-%m-%d")
            if (date1 - date2).days == 1:
                current_streak += 1
            else:
                break
        longest_streak = current_streak  # 简化：实际应该计算历史最长
    
    # 获取徽章
    result = await db.execute(
        select(UserBadge).where(UserBadge.user_id == user_id)
    )
    badges = result.scalars().all()
    
    # 生成最近 30 天的签到日历
    calendar = []
    checkin_dates = {r.checkin_date for r in records}
    
    for i in range(29, -1, -1):
        date = datetime.now() - timedelta(days=i)
        date_str = get_date_str(date)
        calendar.append({
            "date": date_str,
            "day": date.day,
            "checked": date_str in checkin_dates,
            "is_today": date_str == today
        })
    
    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_checkins": total_checkins,
        "last_checkin": records[0].checkin_date if records else None,
        "today_checked": today_checked,
        "badges": [{"name": b.badge_name, "icon": b.badge_icon} for b in badges],
        "checkin_calendar": calendar
    }


async def get_checkin_stats(db: AsyncSession) -> Dict[str, Any]:
    """获取全局签到统计"""
    result = await db.execute(select(func.count(func.distinct(CheckinRecord.user_id))))
    total_users = result.scalar() or 0
    
    result = await db.execute(select(func.count()).where(CheckinRecord.id > 0))
    total_checkins = result.scalar() or 0
    
    avg_streak = 0  # 简化：实际应该计算平均值
    max_streak = 0  # 简化：实际应该查询最大值
    
    return {
        "total_users": total_users,
        "total_checkins": total_checkins,
        "average_streak": avg_streak,
        "max_streak": max_streak
    }
