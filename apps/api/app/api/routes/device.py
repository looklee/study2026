# 设备识别和用户 API 端点

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()

class DeviceInfo(BaseModel):
    """设备信息"""
    platform: str = "unknown"
    browser: str = "unknown"
    language: str = "zh-CN"
    timezone: str = "Asia/Shanghai"
    screen: str = "unknown"
    cores: int = 0
    memory: int = 0

class UserPreferences(BaseModel):
    """用户偏好"""
    theme: Optional[str] = None
    language: Optional[str] = None
    notifications: Optional[bool] = None

@router.post("/api/v1/device/identify")
async def identify_device(request: Request, device_info: DeviceInfo):
    """识别设备并自动登录"""
    from app.device_engine import device_engine
    
    # 获取客户端 IP
    client_ip = request.client.host if request.client else "unknown"
    device_info_dict = device_info.model_dump()
    device_info_dict["ip"] = client_ip
    
    # 注册/识别设备
    result = device_engine.register_device(device_info_dict)
    
    # 创建会话
    session = device_engine.create_session(
        user_id=result["user"]["user_id"],
        device_id=result["device_id"]
    )
    
    return {
        "status": "success",
        "device_id": result["device_id"],
        "session_id": session["session_id"],
        "user": result["user"],
        "message": result["message"]
    }

@router.get("/api/v1/device/verify/{session_id}")
async def verify_session(session_id: str):
    """验证会话"""
    from app.device_engine import device_engine
    
    session = device_engine.validate_session(session_id)
    
    if not session:
        return {"status": "error", "message": "会话已过期"}
    
    # 获取用户信息
    user_stats = device_engine.get_user_stats(session["user_id"])
    
    return {
        "status": "success",
        "session": session,
        "user": user_stats["user"]
    }

@router.get("/api/v1/user/{user_id}")
async def get_user(user_id: str):
    """获取用户信息"""
    from app.device_engine import device_engine
    
    result = device_engine.get_user_stats(user_id)
    return result

@router.post("/api/v1/user/{user_id}/preferences")
async def update_user_preferences(user_id: str, preferences: UserPreferences):
    """更新用户偏好"""
    from app.device_engine import device_engine
    
    pref_dict = {k: v for k, v in preferences.model_dump().items() if v is not None}
    result = device_engine.update_user_preferences(user_id, pref_dict)
    
    return result

@router.get("/api/v1/users")
async def get_all_users():
    """获取所有用户（仅用于调试）"""
    from app.device_engine import device_engine
    
    users = device_engine.get_all_users()
    return {
        "status": "success",
        "count": len(users),
        "users": users
    }

@router.get("/api/v1/devices")
async def get_all_devices():
    """获取所有设备（仅用于调试）"""
    from app.device_engine import device_engine
    
    devices = device_engine.get_all_devices()
    return {
        "status": "success",
        "count": len(devices),
        "devices": devices
    }

@router.post("/api/v1/device/{device_id}/link")
async def link_device(device_id: str, user_id: str):
    """关联设备到用户"""
    from app.device_engine import device_engine
    
    result = device_engine.link_device_to_user(user_id, device_id)
    return result
