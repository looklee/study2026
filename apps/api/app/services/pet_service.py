# AI 学习伴侣服务 - 虚拟宠物养成

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import random

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

# 宠物类型
PET_TYPES = [
    {"id": "owl", "name": "智慧猫头鹰", "icon": "🦉", "trait": "博学"},
    {"id": "dragon", "name": "知识巨龙", "icon": "🐉", "trait": "强大"},
    {"id": "fox", "name": "灵狐", "icon": "🦊", "trait": "聪慧"},
    {"id": "cat", "name": "学霸猫", "icon": "🐱", "trait": "专注"},
    {"id": "dog", "name": "忠犬", "icon": "🐶", "trait": "陪伴"},
]

# 内存存储
user_pets: Dict[str, Dict[str, Any]] = {}  # user_id -> pet_data


def create_pet(user_id: str, username: str = "用户", pet_type: str = None) -> Dict[str, Any]:
    """创建用户的初始宠物"""
    if pet_type is None:
        pet_type = random.choice(PET_TYPES)
    
    pet = {
        "user_id": user_id,
        "username": username,
        "pet_type": pet_type["id"],
        "pet_name": f"{pet_type['name']}",
        "icon": pet_type["icon"],
        "level": 1,
        "exp": 0,
        "exp_to_next": 100,
        "happiness": 50,  # 心情值 0-100
        "energy": 100,    # 精力值 0-100
        "total_study_time": 0,  # 总学习时长（分钟）
        "checkin_days": 0,
        "created_at": datetime.now().isoformat(),
        "last_interaction": datetime.now().isoformat(),
        "messages": [],
        "achievements": []
    }
    
    user_pets[user_id] = pet
    return pet


def get_pet(user_id: str) -> Optional[Dict[str, Any]]:
    """获取用户宠物信息"""
    return user_pets.get(user_id)


def get_or_create_pet(user_id: str, username: str = "用户") -> Dict[str, Any]:
    """获取或创建宠物"""
    pet = user_pets.get(user_id)
    if pet is None:
        pet = create_pet(user_id, username)
    return pet


def add_exp(user_id: str, exp: int, reason: str = "学习") -> Dict[str, Any]:
    """增加宠物经验值"""
    pet = user_pets.get(user_id)
    if pet is None:
        pet = create_pet(user_id)
    
    pet["exp"] += exp
    pet["total_study_time"] += max(0, exp // 10)  # 每 10 经验 = 1 分钟学习
    pet["last_interaction"] = datetime.now().isoformat()
    
    # 检查升级
    level_ups = []
    while pet["exp"] >= pet["exp_to_next"] and pet["level"] < max(PET_LEVELS.keys()):
        pet["level"] += 1
        pet["exp"] -= pet["exp_to_next"]
        pet["exp_to_next"] = int(pet["exp_to_next"] * 1.5)
        
        level_info = PET_LEVELS.get(pet["level"], PET_LEVELS[max(PET_LEVELS.keys())])
        pet["icon"] = level_info["icon"]
        level_ups.append({
            "level": pet["level"],
            "name": level_info["name"],
            "icon": level_info["icon"]
        })
    
    return {
        "status": "success",
        "exp_added": exp,
        "reason": reason,
        "current_exp": pet["exp"],
        "exp_to_next": pet["exp_to_next"],
        "level": pet["level"],
        "level_ups": level_ups
    }


def check_in_bonus(user_id: str) -> Dict[str, Any]:
    """签到奖励"""
    pet = user_pets.get(user_id)
    if pet is None:
        pet = create_pet(user_id)
    
    pet["checkin_days"] += 1
    pet["happiness"] = min(100, pet["happiness"] + 10)
    pet["energy"] = min(100, pet["energy"] + 20)
    
    # 签到奖励经验
    base_exp = 20
    streak_bonus = min(pet["checkin_days"], 30)  # 最多 30 天加成
    total_exp = base_exp + streak_bonus
    
    return add_exp(user_id, total_exp, "签到奖励")


def interact(user_id: str, action: str) -> Dict[str, Any]:
    """与宠物互动"""
    pet = user_pets.get(user_id)
    if pet is None:
        return {"status": "error", "message": "还没有宠物，先创建一个吧！"}
    
    pet["last_interaction"] = datetime.now().isoformat()
    
    if action == "feed":
        pet["happiness"] = min(100, pet["happiness"] + 15)
        pet["energy"] = min(100, pet["energy"] + 10)
        message = f"{pet['icon']} 吃饱了，好开心！"
        exp_gain = 5
    elif action == "play":
        pet["happiness"] = min(100, pet["happiness"] + 20)
        pet["energy"] = max(0, pet["energy"] - 10)
        message = f"{pet['icon']} 玩得很开心！"
        exp_gain = 10
    elif action == "rest":
        pet["energy"] = min(100, pet["energy"] + 30)
        pet["happiness"] = min(100, pet["happiness"] + 5)
        message = f"{pet['icon']} 休息好了，精力充沛！"
        exp_gain = 5
    elif action == "study":
        pet["happiness"] = min(100, pet["happiness"] + 5)
        pet["energy"] = max(0, pet["energy"] - 5)
        message = f"{pet['icon']} 陪你一起学习！"
        exp_gain = 20
    else:
        message = "未知的互动动作"
        exp_gain = 0
    
    if exp_gain > 0:
        add_exp(user_id, exp_gain, f"互动：{action}")
    
    return {
        "status": "success",
        "message": message,
        "happiness": pet["happiness"],
        "energy": pet["energy"],
        "exp_gain": exp_gain
    }


def get_pet_message(user_id: str) -> str:
    """获取宠物的消息（根据状态生成）"""
    pet = user_pets.get(user_id)
    if pet is None:
        return "快来领养一只学习伴侣吧！🥚"
    
    messages = []
    
    # 根据心情生成消息
    if pet["happiness"] < 30:
        messages.append(f"{pet['icon']} 看起来有点不开心，来陪陪我吧...😢")
    elif pet["happiness"] > 80:
        messages.append(f"{pet['icon']} 今天心情超好的！继续加油！😄")
    
    # 根据精力生成消息
    if pet["energy"] < 20:
        messages.append(f"{pet['icon']} 好累啊...让我休息一下吧😴")
    elif pet["energy"] > 80:
        messages.append(f"{pet['icon']} 精力充沛！一起学习吧！💪")
    
    # 根据等级生成消息
    if pet["level"] == 1:
        messages.append("我还在蛋里，需要更多学习才能孵化哦！🥚")
    elif pet["level"] < 5:
        messages.append(f"我会和你一起成长的！当前等级：{PET_LEVELS.get(pet['level'], {}).get('name', '未知')}")
    else:
        messages.append(f"我已经是{PET_LEVELS.get(pet['level'], {}).get('name', '未知')}了！继续变强吧！")
    
    # 长时间未互动
    last_interaction = datetime.fromisoformat(pet["last_interaction"])
    hours_since = (datetime.now() - last_interaction).total_seconds() / 3600
    if hours_since > 24:
        messages.append(f"你已经{int(hours_since)}小时没理我了...😢")
    
    # 学习提醒
    if hours_since > 12 and pet["happiness"] > 50:
        messages.append("主人，今天还没学习哦~ 我等你很久了！📚")
    
    if not messages:
        messages.append(f"{pet['icon']} 随时准备和你一起学习！")
    
    return " ".join(messages)


def get_pet_status(user_id: str) -> Dict[str, Any]:
    """获取宠物完整状态"""
    pet = user_pets.get(user_id)
    if pet is None:
        pet = create_pet(user_id)
    
    level_info = PET_LEVELS.get(pet["level"], PET_LEVELS[max(PET_LEVELS.keys())])
    
    return {
        "pet_type": pet["pet_type"],
        "pet_name": pet["pet_name"],
        "icon": pet["icon"],
        "level": pet["level"],
        "level_name": level_info["name"],
        "exp": pet["exp"],
        "exp_to_next": pet["exp_to_next"],
        "happiness": pet["happiness"],
        "energy": pet["energy"],
        "total_study_time": pet["total_study_time"],
        "checkin_days": pet["checkin_days"],
        "message": get_pet_message(user_id),
        "created_at": pet["created_at"],
        "last_interaction": pet["last_interaction"]
    }


def get_all_pet_types() -> List[Dict[str, Any]]:
    """获取所有宠物类型"""
    return PET_TYPES
