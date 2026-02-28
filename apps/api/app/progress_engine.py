# 学习进度追踪引擎

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

class ProgressEngine:
    """学习进度引擎"""
    
    def __init__(self):
        self.progress_records = {}
        self.user_stats = {}
        self.achievements_db = self._init_achievements()
    
    def _init_achievements(self) -> List[Dict]:
        """初始化成就系统"""
        return [
            {
                "id": "first_step",
                "name": "第一步",
                "description": "开始第一个学习路径",
                "icon": "🎯",
                "condition": {"type": "paths_started", "value": 1},
                "reward": "经验值 +10"
            },
            {
                "id": "week_streak",
                "name": "持之以恒",
                "description": "连续学习 7 天",
                "icon": "🔥",
                "condition": {"type": "streak_days", "value": 7},
                "reward": "经验值 +50"
            },
            {
                "id": "quarter_way",
                "name": "四分之一",
                "description": "学习进度达到 25%",
                "icon": "📈",
                "condition": {"type": "progress_percent", "value": 25},
                "reward": "经验值 +25"
            },
            {
                "id": "halfway",
                "name": "半途",
                "description": "学习进度达到 50%",
                "icon": "🎯",
                "condition": {"type": "progress_percent", "value": 50},
                "reward": "经验值 +50"
            },
            {
                "id": "almost_there",
                "name": "指日可待",
                "description": "学习进度达到 75%",
                "icon": "🚀",
                "condition": {"type": "progress_percent", "value": 75},
                "reward": "经验值 +75"
            },
            {
                "id": "champion",
                "name": "冠军",
                "description": "完成整个学习路径",
                "icon": "🏆",
                "condition": {"type": "progress_percent", "value": 100},
                "reward": "经验值 +100"
            },
            {
                "id": "speed_learner",
                "name": "速学者",
                "description": "1 天内完成 5 个主题",
                "icon": "⚡",
                "condition": {"type": "topics_per_day", "value": 5},
                "reward": "经验值 +30"
            },
            {
                "id": "knowledge_seeker",
                "name": "求知者",
                "description": "累计学习 100 小时",
                "icon": "📚",
                "condition": {"type": "total_hours", "value": 100},
                "reward": "经验值 +200"
            }
        ]
    
    async def track_progress(self, user_id: str, path_id: str, data: Dict[str, Any]) -> Dict:
        """追踪学习进度"""
        record_id = f"{user_id}_{path_id}_{datetime.now().timestamp()}"
        
        record = {
            "record_id": record_id,
            "user_id": user_id,
            "path_id": path_id,
            "action": data.get("action", "update"),
            "item_type": data.get("item_type", "topic"),
            "item_id": data.get("item_id"),
            "completed": data.get("completed", False),
            "time_spent_minutes": data.get("time_spent_minutes", 0),
            "notes": data.get("notes", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存记录
        if user_id not in self.progress_records:
            self.progress_records[user_id] = []
        self.progress_records[user_id].append(record)
        
        # 更新统计
        self._update_user_stats(user_id, record)
        
        # 检查成就
        unlocked_achievements = self._check_achievements(user_id)
        
        return {
            "status": "success",
            "record": record,
            "unlocked_achievements": unlocked_achievements,
            "message": "进度已更新"
        }
    
    def _update_user_stats(self, user_id: str, record: Dict):
        """更新用户统计"""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                "total_time_minutes": 0,
                "total_items_completed": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "last_activity_date": None,
                "paths_started": 0,
                "paths_completed": 0,
                "achievements_unlocked": [],
                "experience_points": 0
            }
        
        stats = self.user_stats[user_id]
        
        # 更新时间
        stats["total_time_minutes"] += record.get("time_spent_minutes", 0)
        
        # 更新完成数
        if record.get("completed"):
            stats["total_items_completed"] += 1
        
        # 更新连续学习
        today = datetime.now().date()
        if stats["last_activity_date"]:
            last_date = datetime.fromisoformat(stats["last_activity_date"]).date()
            days_diff = (today - last_date).days
            if days_diff == 1:
                stats["current_streak"] += 1
            elif days_diff > 1:
                stats["current_streak"] = 1
        else:
            stats["current_streak"] = 1
        
        stats["longest_streak"] = max(stats["longest_streak"], stats["current_streak"])
        stats["last_activity_date"] = datetime.now().isoformat()
        
        # 更新经验值
        if record.get("completed"):
            stats["experience_points"] += 10
    
    def _check_achievements(self, user_id: str) -> List[Dict]:
        """检查并解锁成就"""
        if user_id not in self.user_stats:
            return []
        
        stats = self.user_stats[user_id]
        unlocked = []
        
        for achievement in self.achievements_db:
            if achievement["id"] in stats["achievements_unlocked"]:
                continue
            
            condition = achievement["condition"]
            met = False
            
            if condition["type"] == "paths_started":
                met = stats["paths_started"] >= condition["value"]
            elif condition["type"] == "streak_days":
                met = stats["current_streak"] >= condition["value"]
            elif condition["type"] == "progress_percent":
                # 需要计算平均进度
                met = self._get_average_progress(user_id) >= condition["value"]
            elif condition["type"] == "topics_per_day":
                met = self._get_topics_completed_today(user_id) >= condition["value"]
            elif condition["type"] == "total_hours":
                met = (stats["total_time_minutes"] / 60) >= condition["value"]
            
            if met:
                stats["achievements_unlocked"].append(achievement["id"])
                stats["experience_points"] += int(achievement["reward"].split("+")[1])
                unlocked.append(achievement)
        
        return unlocked
    
    def _get_average_progress(self, user_id: str) -> float:
        """获取平均进度"""
        if user_id not in self.progress_records:
            return 0.0
        
        records = self.progress_records[user_id]
        if not records:
            return 0.0
        
        completed = sum(1 for r in records if r.get("completed"))
        return (completed / len(records)) * 100 if records else 0.0
    
    def _get_topics_completed_today(self, user_id: str) -> int:
        """获取今天完成的主题数"""
        if user_id not in self.progress_records:
            return 0
        
        today = datetime.now().date()
        records = self.progress_records[user_id]
        
        count = 0
        for record in records:
            record_date = datetime.fromisoformat(record["timestamp"]).date()
            if record_date == today and record.get("completed") and record.get("item_type") == "topic":
                count += 1
        
        return count
    
    def get_user_progress(self, user_id: str, path_id: Optional[str] = None) -> Dict:
        """获取用户进度"""
        if user_id not in self.progress_records:
            return self._get_empty_progress()
        
        records = self.progress_records[user_id]
        
        # 按路径筛选
        if path_id:
            records = [r for r in records if r["path_id"] == path_id]
        
        # 计算统计
        total_items = len(records)
        completed_items = sum(1 for r in records if r.get("completed"))
        progress_percent = (completed_items / total_items * 100) if total_items > 0 else 0
        
        # 按类型分组
        by_type = {}
        for record in records:
            item_type = record.get("item_type", "unknown")
            if item_type not in by_type:
                by_type[item_type] = {"total": 0, "completed": 0}
            by_type[item_type]["total"] += 1
            if record.get("completed"):
                by_type[item_type]["completed"] += 1
        
        # 时间统计
        total_time_minutes = sum(r.get("time_spent_minutes", 0) for r in records)
        
        # 计算开始日期
        start_date = min((r["timestamp"] for r in records), default=datetime.now().isoformat())
        total_days = max(1, (datetime.now() - datetime.fromisoformat(start_date)).days)
        avg_per_week = (completed_items / total_days * 7) if total_days > 0 else 0
        
        return {
            "status": "success",
            "progress": {
                "overall": round(progress_percent),
                "completedItems": completed_items,
                "totalItems": total_items,
                "byType": by_type
            },
            "statistics": {
                "startDate": start_date,
                "totalDays": total_days,
                "averagePerWeek": round(avg_per_week, 1),
                "totalTimeMinutes": total_time_minutes,
                "estimatedCompletionDate": self._estimate_completion(progress_percent, total_days)
            }
        }
    
    def _estimate_completion(self, current_progress: float, days_elapsed: int) -> str:
        """预估完成日期"""
        if current_progress <= 0:
            return (datetime.now() + timedelta(days=30)).isoformat()
        
        daily_progress = current_progress / days_elapsed if days_elapsed > 0 else 1
        remaining_progress = 100 - current_progress
        days_remaining = int(remaining_progress / daily_progress) if daily_progress > 0 else 30
        
        return (datetime.now() + timedelta(days=days_remaining)).isoformat()
    
    def _get_empty_progress(self) -> Dict:
        """返回空进度"""
        return {
            "status": "success",
            "progress": {
                "overall": 0,
                "completedItems": 0,
                "totalItems": 0,
                "byType": {}
            },
            "statistics": {
                "startDate": datetime.now().isoformat(),
                "totalDays": 0,
                "averagePerWeek": 0,
                "totalTimeMinutes": 0,
                "estimatedCompletionDate": (datetime.now() + timedelta(days=30)).isoformat()
            }
        }
    
    def get_user_stats(self, user_id: str) -> Dict:
        """获取用户统计"""
        if user_id not in self.user_stats:
            return self._get_empty_stats()
        
        stats = self.user_stats[user_id]
        
        return {
            "status": "success",
            "stats": {
                "userId": user_id,
                "overallProgress": self._get_average_progress(user_id),
                "totalItemsCompleted": stats["total_items_completed"],
                "studyStreak": stats["current_streak"],
                "longestStreak": stats["longest_streak"],
                "totalStudyTime": round(stats["total_time_minutes"] / 60, 1),
                "averagePerWeek": 0,
                "experiencePoints": stats["experience_points"],
                "achievementsUnlocked": len(stats["achievements_unlocked"]),
                "totalAchievements": len(self.achievements_db)
            }
        }
    
    def _get_empty_stats(self) -> Dict:
        """返回空统计"""
        return {
            "status": "success",
            "stats": {
                "userId": "",
                "overallProgress": 0,
                "totalItemsCompleted": 0,
                "studyStreak": 0,
                "longestStreak": 0,
                "totalStudyTime": 0,
                "averagePerWeek": 0,
                "experiencePoints": 0,
                "achievementsUnlocked": 0,
                "totalAchievements": len(self.achievements_db)
            }
        }
    
    def get_achievements(self, user_id: str) -> Dict:
        """获取用户成就"""
        if user_id not in self.user_stats:
            return {"status": "success", "achievements": [], "unlocked_ids": []}
        
        stats = self.user_stats[user_id]
        unlocked_ids = stats.get("achievements_unlocked", [])
        
        achievements = []
        for achievement in self.achievements_db:
            achievements.append({
                **achievement,
                "unlocked": achievement["id"] in unlocked_ids
            })
        
        return {
            "status": "success",
            "achievements": achievements,
            "unlocked_ids": unlocked_ids
        }
    
    def get_activity_timeline(self, user_id: str, days: int = 30) -> Dict:
        """获取活动时间线"""
        if user_id not in self.progress_records:
            return {"status": "success", "timeline": []}
        
        records = self.progress_records[user_id]
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 按日期分组
        by_date = {}
        for record in records:
            record_date = datetime.fromisoformat(record["timestamp"]).date()
            if record_date >= cutoff_date.date():
                date_str = record_date.isoformat()
                if date_str not in by_date:
                    by_date[date_str] = {
                        "date": date_str,
                        "items_completed": 0,
                        "time_spent": 0,
                        "activities": []
                    }
                
                if record.get("completed"):
                    by_date[date_str]["items_completed"] += 1
                by_date[date_str]["time_spent"] += record.get("time_spent_minutes", 0)
                by_date[date_str]["activities"].append({
                    "type": record.get("item_type"),
                    "action": record.get("action"),
                    "completed": record.get("completed")
                })
        
        timeline = sorted(by_date.values(), key=lambda x: x["date"], reverse=True)
        
        return {
            "status": "success",
            "timeline": timeline
        }

# 全局引擎实例
progress_engine = ProgressEngine()
