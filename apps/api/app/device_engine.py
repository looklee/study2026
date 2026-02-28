# 设备指纹和自动识别引擎

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import hashlib
import json
import os

class DeviceEngine:
    """设备指纹引擎"""
    
    def __init__(self):
        self.devices = {}
        self.users = {}
        self.sessions = {}
    
    def generate_device_fingerprint(self, device_info: Dict[str, Any]) -> str:
        """生成设备指纹"""
        # 组合设备信息
        fingerprint_data = {
            "platform": device_info.get("platform", "unknown"),
            "browser": device_info.get("browser", "unknown"),
            "language": device_info.get("language", "zh-CN"),
            "timezone": device_info.get("timezone", "Asia/Shanghai"),
            "screen": device_info.get("screen", "unknown"),
            "cores": device_info.get("cores", 0),
            "memory": device_info.get("memory", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        # 生成哈希
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        device_id = hashlib.sha256(fingerprint_string.encode()).hexdigest()[:32]
        
        return device_id
    
    def register_device(self, device_info: Dict[str, Any]) -> Dict:
        """注册设备"""
        device_id = self.generate_device_fingerprint(device_info)
        
        # 检查设备是否已存在
        if device_id in self.devices:
            device = self.devices[device_id]
            device["last_seen"] = datetime.now().isoformat()
            device["login_count"] = device.get("login_count", 0) + 1
            
            # 自动创建/更新用户
            user = self._get_or_create_user(device_id)
            
            return {
                "status": "success",
                "device_id": device_id,
                "user": user,
                "message": "设备已识别"
            }
        
        # 新设备注册
        device = {
            "device_id": device_id,
            "device_info": device_info,
            "created_at": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "login_count": 1,
            "status": "active"
        }
        
        self.devices[device_id] = device
        
        # 自动创建用户
        user = self._get_or_create_user(device_id)
        
        return {
            "status": "success",
            "device_id": device_id,
            "user": user,
            "message": "设备已注册"
        }
    
    def _get_or_create_user(self, device_id: str) -> Dict:
        """获取或创建用户"""
        # 查找是否已有用户关联此设备
        for user_id, user in self.users.items():
            if device_id in user.get("devices", []):
                user["last_login"] = datetime.now().isoformat()
                user["login_count"] = user.get("login_count", 0) + 1
                return user
        
        # 创建新用户
        user_id = f"user_{device_id[:8]}"
        user = {
            "user_id": user_id,
            "username": f"用户_{device_id[:8]}",
            "email": f"{user_id}@local.device",
            "devices": [device_id],
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
            "login_count": 1,
            "status": "active",
            "preferences": {
                "theme": "light",
                "language": "zh-CN",
                "notifications": True
            },
            "learning_stats": {
                "paths_started": 0,
                "total_study_time": 0,
                "achievements_unlocked": 0
            }
        }
        
        self.users[user_id] = user
        return user
    
    def get_user_by_device(self, device_id: str) -> Optional[Dict]:
        """通过设备 ID 获取用户"""
        if device_id not in self.devices:
            return None
        
        # 查找关联用户
        for user_id, user in self.users.items():
            if device_id in user.get("devices", []):
                return user
        
        return None
    
    def create_session(self, user_id: str, device_id: str) -> Dict:
        """创建会话"""
        session_id = f"session_{user_id}_{datetime.now().timestamp()}"
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "device_id": device_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "status": "active"
        }
        
        self.sessions[session_id] = session
        
        return session
    
    def validate_session(self, session_id: str) -> Optional[Dict]:
        """验证会话"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        expires_at = datetime.fromisoformat(session["expires_at"])
        
        if datetime.now() > expires_at:
            session["status"] = "expired"
            return None
        
        if session["status"] != "active":
            return None
        
        # 延长会话
        session["expires_at"] = (datetime.now() + timedelta(days=30)).isoformat()
        
        return session
    
    def get_user_stats(self, user_id: str) -> Dict:
        """获取用户统计"""
        if user_id not in self.users:
            return {"status": "error", "message": "用户不存在"}
        
        user = self.users[user_id]
        device_count = len(user.get("devices", []))
        
        return {
            "status": "success",
            "user": {
                "user_id": user["user_id"],
                "username": user["username"],
                "created_at": user["created_at"],
                "last_login": user["last_login"],
                "login_count": user["login_count"],
                "device_count": device_count
            },
            "learning_stats": user.get("learning_stats", {}),
            "preferences": user.get("preferences", {})
        }
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> Dict:
        """更新用户偏好"""
        if user_id not in self.users:
            return {"status": "error", "message": "用户不存在"}
        
        user = self.users[user_id]
        user["preferences"].update(preferences)
        
        return {"status": "success", "message": "偏好已更新"}
    
    def link_device_to_user(self, user_id: str, device_id: str) -> Dict:
        """关联设备到用户"""
        if user_id not in self.users:
            return {"status": "error", "message": "用户不存在"}
        
        if device_id not in self.devices:
            return {"status": "error", "message": "设备不存在"}
        
        user = self.users[user_id]
        if device_id not in user["devices"]:
            user["devices"].append(device_id)
        
        return {"status": "success", "message": "设备已关联"}
    
    def get_all_users(self) -> List[Dict]:
        """获取所有用户"""
        return list(self.users.values())
    
    def get_all_devices(self) -> List[Dict]:
        """获取所有设备"""
        return list(self.devices.values())
    
    def cleanup_expired_sessions(self):
        """清理过期会话"""
        now = datetime.now()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if datetime.fromisoformat(session["expires_at"]) < now
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        return len(expired_sessions)

# 全局引擎实例
device_engine = DeviceEngine()
