# AI 学习伴侣服务 - 虚拟宠物养成 (数据库版本)

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import random
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Pet, User
from app.core.database import get_db

# 宠物等级配置
PET_LEVELS = {
    1: {"name": "蛋蛋", "icon": "🥚", "min_exp": 0},
    2: {"name": "小雏", "icon": "🐣", "min_exp": 100},
    3: {"name": "学童", "icon": "🐤", "min_exp": 300},
    4: {"name": "学子", "icon": "🐥", "min_exp": 600},
    5: {"name": "学师", "icon": "🦅", "min_exp": 1000},
    6: {"name": "学尊", "icon": "🦉", "min_exp": 1600},
    7: {"name": "学圣", "icon": "🐉", "min_exp": 2500},
    8: {"name": "学神", "icon": "✨", "min_exp": 4000},
}

PET_TYPES = [
    {"id": "owl", "name": "智慧猫头鹰", "icon": "🦉", "trait": "博学"},
    {"id": "dragon", "name": "知识巨龙", "icon": "🐉", "trait": "强大"},
    {"id": "fox", "name": "灵狐", "icon": "🦊", "trait": "聪慧"},
    {"id": "cat", "name": "学霸猫", "icon": "🐱", "trait": "专注"},
    {"id": "dog", "name": "忠犬", "icon": "🐶", "trait": "陪伴"},
]


async def create_pet(db: AsyncSession, user_id: int, pet_type: str = None) -> Pet:
    """创建用户的初始宠物"""
    if pet_type is None:
        pet_type_data = random.choice(PET_TYPES)
    else:
        pet_type_data = next((p for p in PET_TYPES if p["id"] == pet_type), PET_TYPES[0])
    
    pet = Pet(
        user_id=user_id,
        name=f"{pet_type_data['name']}",
        pet_type=pet_type_data["id"],
        avatar_url=None,
        level=1,
        experience=0,
        experience_to_next_level=100,
        happiness=50,
        energy=100,
        health=100,
        total_interactions=0,
        consecutive_days=0,
    )
    
    db.add(pet)
    await db.commit()
    await db.refresh(pet)
    return pet


async def get_pet(db: AsyncSession, user_id: int) -> Optional[Pet]:
    """获取用户宠物信息"""
    result = await db.execute(select(Pet).where(Pet.user_id == user_id))
    return result.scalar_one_or_none()


async def get_or_create_pet(db: AsyncSession, user_id: int) -> Pet:
    """获取或创建宠物"""
    pet = await get_pet(db, user_id)
    if pet is None:
        pet = await create_pet(db, user_id)
    return pet


async def add_exp(db: AsyncSession, user_id: int, exp: int, reason: str = "学习") -> Dict[str, Any]:
    """增加宠物经验值"""
    pet = await get_pet(db, user_id)
    if pet is None:
        pet = await create_pet(db, user_id)
    
    pet.experience += exp
    pet.total_interactions += 1
    pet.last_interaction_at = datetime.now()
    
    # 检查升级
    level_ups = []
    while pet.experience >= pet.experience_to_next_level and pet.level < max(PET_LEVELS.keys()):
        pet.level += 1
        pet.experience -= pet.experience_to_next_level
        pet.experience_to_next_level = int(pet.experience_to_next_level * 1.5)
        
        level_info = PET_LEVELS.get(pet.level, PET_LEVELS[max(PET_LEVELS.keys())])
        level_ups.append({
            "level": pet.level,
            "name": level_info["name"],
            "icon": level_info["icon"]
        })
    
    await db.commit()
    await db.refresh(pet)
    
    return {
        "status": "success",
        "exp_added": exp,
        "reason": reason,
        "current_exp": pet.experience,
        "exp_to_next": pet.experience_to_next_level,
        "level": pet.level,
        "level_ups": level_ups
    }


async def check_in_bonus(db: AsyncSession, user_id: int) -> Dict[str, Any]:
    """签到奖励"""
    pet = await get_pet(db, user_id)
    if pet is None:
        pet = await create_pet(db, user_id)
    
    pet.consecutive_days += 1
    pet.happiness = min(100, pet.happiness + 10)
    pet.energy = min(100, pet.energy + 20)
    
    base_exp = 20
    streak_bonus = min(pet.consecutive_days, 30)
    total_exp = base_exp + streak_bonus
    
    result = await add_exp(db, user_id, total_exp, "签到奖励")
    return result


async def interact(db: AsyncSession, user_id: int, action: str) -> Dict[str, Any]:
    """与宠物互动"""
    pet = await get_pet(db, user_id)
    if pet is None:
        return {"status": "error", "message": "还没有宠物，先创建一个吧！"}
    
    pet.last_interaction_at = datetime.now()
    pet.total_interactions += 1
    
    if action == "feed":
        pet.happiness = min(100, pet.happiness + 15)
        pet.energy = min(100, pet.energy + 10)
        message = f"{get_pet_icon(pet.pet_type)} 吃饱了，好开心！"
        exp_gain = 5
    elif action == "play":
        pet.happiness = min(100, pet.happiness + 20)
        pet.energy = max(0, pet.energy - 10)
        message = f"{get_pet_icon(pet.pet_type)} 玩得很开心！"
        exp_gain = 10
    elif action == "rest":
        pet.energy = min(100, pet.energy + 30)
        pet.happiness = min(100, pet.happiness + 5)
        message = f"{get_pet_icon(pet.pet_type)} 休息好了，精力充沛！"
        exp_gain = 5
    elif action == "study":
        pet.happiness = min(100, pet.happiness + 5)
        pet.energy = max(0, pet.energy - 5)
        message = f"{get_pet_icon(pet.pet_type)} 陪你一起学习！"
        exp_gain = 20
    else:
        message = "未知的互动动作"
        exp_gain = 0
    
    await db.commit()
    await db.refresh(pet)
    
    if exp_gain > 0:
        await add_exp(db, user_id, exp_gain, f"互动：{action}")
    
    return {
        "status": "success",
        "message": message,
        "happiness": pet.happiness,
        "energy": pet.energy,
        "exp_gain": exp_gain
    }


def get_pet_icon(pet_type: str) -> str:
    """获取宠物图标"""
    pet_data = next((p for p in PET_TYPES if p["id"] == pet_type), PET_TYPES[0])
    return pet_data["icon"]


async def get_pet_message(db: AsyncSession, user_id: int) -> str:
    """获取宠物的消息"""
    pet = await get_pet(db, user_id)
    if pet is None:
        return "快来领养一只学习伴侣吧！🥚"
    
    messages = []
    icon = get_pet_icon(pet.pet_type)
    
    if pet.happiness < 30:
        messages.append(f"{icon} 看起来有点不开心，来陪陪我吧...😢")
    elif pet.happiness > 80:
        messages.append(f"{icon} 今天心情超好的！继续加油！😄")
    
    if pet.energy < 20:
        messages.append(f"{icon} 好累啊...让我休息一下吧😴")
    elif pet.energy > 80:
        messages.append(f"{icon} 精力充沛！一起学习吧！💪")
    
    if pet.level == 1:
        messages.append("我还在蛋里，需要更多学习才能孵化哦！🥚")
    elif pet.level < 5:
        level_info = PET_LEVELS.get(pet.level, {})
        messages.append(f"我会和你一起成长的！当前等级：{level_info.get('name', '未知')}")
    else:
        level_info = PET_LEVELS.get(pet.level, {})
        messages.append(f"我已经是{level_info.get('name', '未知')}了！继续变强吧！")
    
    if pet.last_interaction_at:
        hours_since = (datetime.now() - pet.last_interaction_at).total_seconds() / 3600
        if hours_since > 24:
            messages.append(f"你已经{int(hours_since)}小时没理我了...😢")
        if hours_since > 12 and pet.happiness > 50:
            messages.append("主人，今天还没学习哦~ 我等你很久了！📚")
    
    if not messages:
        messages.append(f"{icon} 随时准备和你一起学习！")
    
    return " ".join(messages)


async def get_pet_status(db: AsyncSession, user_id: int) -> Dict[str, Any]:
    """获取宠物完整状态"""
    pet = await get_pet(db, user_id)
    if pet is None:
        pet = await create_pet(db, user_id)
    
    level_info = PET_LEVELS.get(pet.level, PET_LEVELS[max(PET_LEVELS.keys())])
    icon = get_pet_icon(pet.pet_type)
    message = await get_pet_message(db, user_id)
    
    return {
        "pet_type": pet.pet_type,
        "pet_name": pet.name,
        "icon": icon,
        "level": pet.level,
        "level_name": level_info["name"],
        "exp": pet.experience,
        "exp_to_next": pet.experience_to_next_level,
        "happiness": pet.happiness,
        "energy": pet.energy,
        "health": pet.health,
        "total_interactions": pet.total_interactions,
        "consecutive_days": pet.consecutive_days,
        "message": message,
        "created_at": pet.created_at.isoformat() if pet.created_at else None,
        "last_interaction": pet.last_interaction_at.isoformat() if pet.last_interaction_at else None
    }


def get_all_pet_types() -> List[Dict[str, Any]]:
    """获取所有宠物类型"""
    return PET_TYPES
