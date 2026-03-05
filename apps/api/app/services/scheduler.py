# 定时任务调度器

from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
import logging

logger = logging.getLogger(__name__)


class TaskScheduler:
    """定时任务调度器"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self._initialized = False
    
    def start(self):
        """启动调度器"""
        if not self._initialized:
            self.scheduler.start()
            self._initialized = True
            logger.info("任务调度器已启动")
    
    def shutdown(self, wait: bool = True):
        """关闭调度器"""
        if self._initialized:
            self.scheduler.shutdown(wait=wait)
            self._initialized = False
            logger.info("任务调度器已关闭")
    
    def add_cron_job(
        self,
        task_id: str,
        func: Callable,
        cron_expression: str = None,
        hour: int = None,
        minute: int = None,
        day_of_week: str = None,
        args: tuple = None,
        kwargs: dict = None,
        description: str = ""
    ):
        """添加 Cron 任务"""
        if cron_expression:
            # 解析 cron 表达式 (简化版)
            parts = cron_expression.split()
            if len(parts) >= 2:
                minute = int(parts[0]) if parts[0] != "*" else None
                hour = int(parts[1]) if parts[1] != "*" else None
                day_of_week = parts[2] if len(parts) > 2 and parts[2] != "*" else None
        
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            day_of_week=day_of_week,
            timezone="Asia/Shanghai"
        )
        
        self.scheduler.add_job(
            func,
            trigger,
            id=task_id,
            args=args or (),
            kwargs=kwargs or {},
            name=description or task_id,
            replace_existing=True
        )
        
        self.tasks[task_id] = {
            "type": "cron",
            "func": func.__name__,
            "description": description,
            "cron": f"{minute} {hour} {day_of_week or '*'}",
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"添加定时任务：{task_id} - {description}")
        return True
    
    def add_interval_job(
        self,
        task_id: str,
        func: Callable,
        seconds: int = None,
        minutes: int = None,
        hours: int = None,
        days: int = None,
        args: tuple = None,
        kwargs: dict = None,
        description: str = ""
    ):
        """添加间隔任务"""
        trigger = IntervalTrigger(
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            timezone="Asia/Shanghai"
        )
        
        self.scheduler.add_job(
            func,
            trigger,
            id=task_id,
            args=args or (),
            kwargs=kwargs or {},
            name=description or task_id,
            replace_existing=True
        )
        
        self.tasks[task_id] = {
            "type": "interval",
            "func": func.__name__,
            "description": description,
            "interval": f"{days or 0}d {hours or 0}h {minutes or 0}m {seconds or 0}s",
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"添加间隔任务：{task_id} - {description}")
        return True
    
    def add_onetime_job(
        self,
        task_id: str,
        func: Callable,
        run_date: datetime,
        args: tuple = None,
        kwargs: dict = None,
        description: str = ""
    ):
        """添加一次性任务"""
        trigger = DateTrigger(run_date=run_date, timezone="Asia/Shanghai")
        
        self.scheduler.add_job(
            func,
            trigger,
            id=task_id,
            args=args or (),
            kwargs=kwargs or {},
            name=description or task_id,
            replace_existing=True
        )
        
        self.tasks[task_id] = {
            "type": "onetime",
            "func": func.__name__,
            "description": description,
            "run_date": run_date.isoformat(),
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"添加一次性任务：{task_id} - {description}")
        return True
    
    def remove_job(self, task_id: str):
        """移除任务"""
        try:
            self.scheduler.remove_job(task_id)
            if task_id in self.tasks:
                del self.tasks[task_id]
            logger.info(f"移除任务：{task_id}")
            return True
        except Exception as e:
            logger.error(f"移除任务失败：{task_id}, 错误：{e}")
            return False
    
    def get_task_info(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务信息"""
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """列出所有任务"""
        return [
            {
                "task_id": task_id,
                **info
            }
            for task_id, info in self.tasks.items()
        ]
    
    def get_next_run_time(self, task_id: str) -> Optional[datetime]:
        """获取下次执行时间"""
        job = self.scheduler.get_job(task_id)
        if job:
            return job.next_run_time
        return None


# 预定义任务函数
async def daily_checkin_reminder():
    """每日签到提醒"""
    logger.info("发送每日签到提醒")
    # 实际实现：发送推送通知/邮件给用户


async def weekly_report_generator():
    """生成周报"""
    logger.info("生成学习周报")
    # 实际实现：统计用户学习数据，生成报告


async def pet_status_updater():
    """更新宠物状态"""
    logger.info("更新宠物状态")
    # 实际实现：减少宠物精力值，检查健康状态


async def data_cleanup():
    """数据清理"""
    logger.info("清理过期数据")
    # 实际实现：清理过期的会话、日志等


# 全局实例
_scheduler: Optional[TaskScheduler] = None


def get_scheduler() -> TaskScheduler:
    """获取调度器实例"""
    global _scheduler
    if _scheduler is None:
        _scheduler = TaskScheduler()
        _scheduler.start()
        
        # 注册默认任务
        _scheduler.add_cron_job(
            "daily_reminder",
            daily_checkin_reminder,
            hour=9,
            minute=0,
            description="每日签到提醒"
        )
        
        _scheduler.add_cron_job(
            "weekly_report",
            weekly_report_generator,
            hour=20,
            minute=0,
            day_of_week="sun",
            description="每周日报生成"
        )
        
        _scheduler.add_interval_job(
            "pet_update",
            pet_status_updater,
            hours=1,
            description="宠物状态更新"
        )
        
        _scheduler.add_cron_job(
            "data_cleanup",
            data_cleanup,
            hour=3,
            minute=0,
            description="数据清理"
        )
    
    return _scheduler
