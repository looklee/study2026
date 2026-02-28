# 签到服务 - 每日签到 + Streak 追踪

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import json

# 内存存储（生产环境应使用数据库）
checkin_records: Dict[str, List[str]] = {}  # user_id -> [date_strings]
user_streaks: Dict[str, Dict[str, Any]] = {}  # user_id -> streak_data


def get_date_str(dt: datetime = None) -> str:
    """获取日期字符串"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d")


def check_in(user_id: str, username: str = "用户") -> Dict[str, Any]:
    """
    用户签到
    返回：签到结果、当前 streak、是否连续、奖励信息
    """
    today = get_date_str()
    
    # 初始化用户数据
    if user_id not in checkin_records:
        checkin_records[user_id] = []
    if user_id not in user_streaks:
        user_streaks[user_id] = {
            "current_streak": 0,
            "longest_streak": 0,
            "last_checkin": None,
            "total_checkins": 0,
            "username": username
        }
    
    streak_data = user_streaks[user_id]
    checkin_dates = checkin_records[user_id]
    
    # 检查今天是否已签到
    if today in checkin_dates:
        return {
            "status": "already_checked_in",
            "message": "今天已经签到过了，明天再来哦~",
            "streak": streak_data["current_streak"],
            "today": today
        }
    
    # 计算 streak
    yesterday = get_date_str(datetime.now() - timedelta(days=1))
    last_checkin = streak_data.get("last_checkin")
    
    if last_checkin == yesterday:
        # 连续签到
        streak_data["current_streak"] += 1
        is_continuous = True
    elif last_checkin == today:
        # 今天已经签到（已处理）
        is_continuous = True
    else:
        # 中断了，重新开始
        if streak_data["current_streak"] > streak_data["longest_streak"]:
            streak_data["longest_streak"] = streak_data["current_streak"]
        streak_data["current_streak"] = 1
        is_continuous = False
    
    # 记录签到
    checkin_dates.append(today)
    streak_data["last_checkin"] = today
    streak_data["total_checkins"] += 1
    
    # 计算奖励
    reward = calculate_reward(streak_data["current_streak"], is_continuous)
    
    # 更新最长连续记录
    if streak_data["current_streak"] > streak_data["longest_streak"]:
        streak_data["longest_streak"] = streak_data["current_streak"]
    
    # 生成消息
    messages = {
        1: "新的开始！加油！🎉",
        3: "连续 3 天！你很棒！👍",
        7: "一周坚持！获得「周勤学者」徽章！🏆",
        14: "两周不断！获得「半月达人」徽章！🥈",
        30: "月度传奇！获得「月勤学者」徽章！🥇",
        100: "百日传奇！你是真正的学习王者！👑"
    }
    
    milestone_message = messages.get(streak_data["current_streak"], f"连续{streak_data['current_streak']}天！继续保持！🔥")
    
    return {
        "status": "success",
        "message": f"签到成功！{milestone_message}",
        "streak": streak_data["current_streak"],
        "longest_streak": streak_data["longest_streak"],
        "total_checkins": streak_data["total_checkins"],
        "is_continuous": is_continuous,
        "reward": reward,
        "today": today,
        "badges_earned": reward.get("badges", [])
    }


def calculate_reward(streak: int, is_continuous: bool) -> Dict[str, Any]:
    """计算签到奖励"""
    reward = {
        "points": 10 if is_continuous else 5,
        "badges": [],
        "items": []
    }
    
    # 连续奖励
    if streak >= 7:
        reward["badges"].append("周勤学者")
    if streak >= 14:
        reward["badges"].append("半月达人")
    if streak >= 30:
        reward["badges"].append("月勤学者")
    if streak >= 100:
        reward["badges"].append("百日传奇")
    
    # 特殊天数奖励
    if streak % 10 == 0:
        reward["items"].append(f"🎁 {streak}天纪念宝箱")
    
    return reward


def get_user_checkin_info(user_id: str) -> Dict[str, Any]:
    """获取用户签到信息"""
    if user_id not in user_streaks:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "total_checkins": 0,
            "last_checkin": None,
            "today_checked": False,
            "checkin_calendar": []
        }
    
    streak_data = user_streaks[user_id]
    today = get_date_str()
    
    # 生成最近 30 天的签到日历
    calendar = []
    checkin_dates = set(checkin_records.get(user_id, []))
    
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
        "current_streak": streak_data["current_streak"],
        "longest_streak": streak_data["longest_streak"],
        "total_checkins": streak_data["total_checkins"],
        "last_checkin": streak_data.get("last_checkin"),
        "today_checked": today in checkin_records.get(user_id, []),
        "checkin_calendar": calendar
    }


def get_checkin_stats() -> Dict[str, Any]:
    """获取全局签到统计"""
    total_users = len(user_streaks)
    total_checkins = sum(s["total_checkins"] for s in user_streaks.values())
    avg_streak = sum(s["current_streak"] for s in user_streaks.values()) / max(total_users, 1)
    max_streak = max((s["longest_streak"] for s in user_streaks.values()), default=0)
    
    return {
        "total_users": total_users,
        "total_checkins": total_checkins,
        "average_streak": round(avg_streak, 1),
        "max_streak": max_streak
    }
