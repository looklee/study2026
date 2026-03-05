# Study2026 API - 简化版（包含知识库）

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
from pydantic import BaseModel
import hashlib
import json
from datetime import datetime, timedelta, date

app = FastAPI(
    title="Study2026 API",
    description="AI 学习平台 API",
    version="3.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 内存存储
devices: Dict[str, Dict] = {}
users: Dict[str, Dict] = {}
sessions: Dict[str, Dict] = {}
documents: Dict[str, Dict] = {}

class DeviceInfo(BaseModel):
    platform: str = "unknown"
    browser: str = "unknown"
    language: str = "zh-CN"
    timezone: str = "Asia/Shanghai"
    screen: str = "unknown"
    cores: int = 0
    memory: int = 0

class DocumentUpload(BaseModel):
    file_name: str
    content: str
    category: str = "general"
    tags: list = []

def generate_device_id(device_info: Dict) -> str:
    data = json.dumps(device_info, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()[:32]

def get_or_create_user(device_id: str) -> Dict:
    for user in users.values():
        if device_id in user.get("devices", []):
            user["last_login"] = datetime.now().isoformat()
            user["login_count"] += 1
            return user
    
    user_id = f"user_{device_id[:8]}"
    user = {
        "user_id": user_id,
        "username": f"用户_{device_id[:8]}",
        "email": f"{user_id}@local.device",
        "devices": [device_id],
        "created_at": datetime.now().isoformat(),
        "last_login": datetime.now().isoformat(),
        "login_count": 1,
        "preferences": {"theme": "light", "language": "zh-CN", "notifications": True}
    }
    users[user_id] = user
    return user

@app.get("/")
async def root():
    return {"status": "ok", "message": "Study2026 API v3.0", "version": "3.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/device/identify")
async def identify_device(request: Request, device_info: DeviceInfo):
    device_id = generate_device_id(device_info.model_dump())
    
    if device_id not in devices:
        devices[device_id] = {
            "device_id": device_id,
            "device_info": device_info.model_dump(),
            "created_at": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "login_count": 1
        }
        message = "设备已注册"
    else:
        devices[device_id]["last_seen"] = datetime.now().isoformat()
        devices[device_id]["login_count"] += 1
        message = "设备已识别"
    
    user = get_or_create_user(device_id)
    session_id = f"session_{device_id}_{datetime.now().timestamp()}"
    sessions[session_id] = {
        "session_id": session_id,
        "user_id": user["user_id"],
        "device_id": device_id,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat()
    }
    
    return {
        "status": "success",
        "device_id": device_id,
        "session_id": session_id,
        "user": user,
        "message": message
    }

@app.get("/api/v1/device/verify/{session_id}")
async def verify_session(session_id: str):
    if session_id not in sessions:
        return {"status": "error", "message": "会话不存在"}
    session = sessions[session_id]
    if datetime.now() > datetime.fromisoformat(session["expires_at"]):
        return {"status": "error", "message": "会话已过期"}
    return {"status": "success", "session": session, "user": users.get(session["user_id"])}

@app.get("/api/v1/user/{user_id}")
async def get_user(user_id: str):
    if user_id not in users:
        return {"status": "error", "message": "用户不存在"}
    return {"status": "success", "user": users[user_id]}

# 知识库 API
@app.get("/api/v1/knowledge/stats")
async def get_knowledge_stats():
    total_docs = len(documents)
    by_category = {}
    for doc in documents.values():
        cat = doc.get("category", "general")
        by_category[cat] = by_category.get(cat, 0) + 1
    return {
        "status": "success",
        "stats": {
            "total_documents": total_docs,
            "total_chunks": total_docs * 5,
            "by_category": by_category,
            "by_status": {"processed": total_docs}
        }
    }

@app.get("/api/v1/knowledge/categories")
async def get_categories():
    categories = set(doc.get("category", "general") for doc in documents.values())
    return {"status": "success", "categories": list(categories) if categories else ["general"]}

@app.get("/api/v1/knowledge/documents")
async def list_documents(category: Optional[str] = None, limit: int = 20):
    docs = []
    for doc_id, doc in documents.items():
        if category and doc.get("category") != category:
            continue
        docs.append({
            "doc_id": doc_id,
            "file_name": doc.get("file_name", "未知"),
            "category": doc.get("category", "general"),
            "tags": doc.get("tags", []),
            "status": doc.get("status", "processed"),
            "created_at": doc.get("created_at"),
            "chunks_count": 5
        })
    return {"status": "success", "documents": docs[:limit]}

@app.get("/api/v1/knowledge/documents/{doc_id}")
async def get_document(doc_id: str):
    if doc_id not in documents:
        return {"status": "error", "message": "文档不存在"}
    return {"status": "success", "document": documents[doc_id]}

@app.post("/api/v1/knowledge/documents")
async def create_document(doc_data: DocumentUpload):
    doc_id = f"doc_{datetime.now().timestamp()}"
    documents[doc_id] = {
        "doc_id": doc_id,
        "file_name": doc_data.file_name,
        "content": doc_data.content,
        "category": doc_data.category,
        "tags": doc_data.tags,
        "mime_type": "text/plain",
        "file_size": len(doc_data.content),
        "chunks": [doc_data.content[i:i+500] for i in range(0, len(doc_data.content), 500)],
        "status": "processed",
        "created_at": datetime.now().isoformat()
    }
    return {
        "status": "success",
        "doc_id": doc_id,
        "message": f"文档已上传：{doc_data.file_name}",
        "chunks_count": len(documents[doc_id]["chunks"])
    }

@app.post("/api/v1/knowledge/search")
async def search_knowledge(query_data: Dict[str, Any]):
    query = query_data.get("query", "").lower()
    limit = query_data.get("limit", 10)
    results = []
    for doc_id, doc in documents.items():
        score = 0.0
        content = doc.get("content", "").lower()
        if query in doc.get("file_name", "").lower():
            score += 10.0
        for tag in doc.get("tags", []):
            if query in tag.lower():
                score += 5.0
        if query in content:
            score += 3.0
        if score > 0:
            results.append({
                "doc_id": doc_id,
                "file_name": doc.get("file_name", "未知"),
                "category": doc.get("category", "general"),
                "tags": doc.get("tags", []),
                "score": score,
                "snippet": content[:200] + "..." if len(content) > 200 else content
            })
    results.sort(key=lambda x: x["score"], reverse=True)
    return {"status": "success", "query": query, "total": len(results), "results": results[:limit]}

@app.delete("/api/v1/knowledge/documents/{doc_id}")
async def delete_document(doc_id: str):
    if doc_id in documents:
        del documents[doc_id]
        return {"status": "success", "message": "文档已删除"}
    return {"status": "error", "message": "文档不存在"}

@app.get("/api/v1/users")
async def list_users():
    return {"status": "success", "count": len(users), "users": list(users.values())}

@app.get("/api/v1/devices")
async def list_devices():
    return {"status": "success", "count": len(devices), "devices": list(devices.values())}

# API 密钥管理（简化版）
api_keys = {
    "qwen": {
        "api_key": None,
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "enabled": False,
        "updated_at": None
    },
    "openai": {
        "api_key": None,
        "base_url": "https://api.openai.com/v1",
        "enabled": False,
        "updated_at": None
    },
    "anthropic": {
        "api_key": None,
        "base_url": "https://api.anthropic.com",
        "enabled": False,
        "updated_at": None
    }
}

@app.get("/api/v1/api-keys")
async def get_api_keys():
    result = {}
    for provider, config in api_keys.items():
        result[provider] = {
            "enabled": config["enabled"],
            "configured": config["api_key"] is not None,
            "last_4_digits": config["api_key"][-4:] if config["api_key"] else None,
            "base_url": config["base_url"],
            "updated_at": config["updated_at"]
        }
    return result

@app.post("/api/v1/api-keys/{provider}/configure")
async def configure_api_key(provider: str, config: Dict[str, Any]):
    if provider not in api_keys:
        return {"status": "error", "message": "提供商不存在"}
    
    if config.get("api_key"):
        api_keys[provider]["api_key"] = config["api_key"]
    if config.get("base_url"):
        api_keys[provider]["base_url"] = config["base_url"]
    if config.get("enabled") is not None:
        api_keys[provider]["enabled"] = config["enabled"]
    api_keys[provider]["updated_at"] = datetime.now().isoformat()
    
    return {"status": "success", "message": f"{provider} 配置已保存", "provider": provider}

@app.post("/api/v1/api-keys/{provider}/test")
async def test_api_key(provider: str):
    if provider not in api_keys:
        return {"status": "error", "message": "提供商不存在"}
    
    if not api_keys[provider]["api_key"]:
        return {"status": "error", "message": "请先配置 API 密钥"}
    
    # 模拟测试
    return {"status": "success", "message": f"{provider} API 连接成功", "response_time": 150}

@app.delete("/api/v1/api-keys/{provider}")
async def delete_api_key(provider: str):
    if provider not in api_keys:
        return {"status": "error", "message": "提供商不存在"}
    
    api_keys[provider]["api_key"] = None
    api_keys[provider]["enabled"] = False
    api_keys[provider]["updated_at"] = datetime.now().isoformat()
    
    return {"status": "success", "message": f"{provider} API 密钥已删除"}

@app.post("/api/v1/api-keys/{provider}/toggle")
async def toggle_api_key(provider: str):
    if provider not in api_keys:
        return {"status": "error", "message": "请先配置 API 密钥"}
    
    api_keys[provider]["enabled"] = not api_keys[provider]["enabled"]
    api_keys[provider]["updated_at"] = datetime.now().isoformat()
    
    return {"status": "success", "enabled": api_keys[provider]["enabled"], "provider": provider}

# 学习进度（简化版）
progress_records = {}
user_stats = {}

# 宠物数据（简化版 - 内存存储）
pets_db = {}

# OpenClaw 数据（简化版 - 内存存储）
openclaw_conversations = {}
openclaw_skills = [
    "文本生成", "翻译", "摘要", "问答", "编程辅助", "数据分析", 
    "图像生成", "语音识别", "情感分析", "代码审查"
]
achievements_db = [
    {"id": "first_step", "name": "第一步", "description": "开始第一个学习路径", "icon": "🎯", "unlocked": False},
    {"id": "week_streak", "name": "持之以恒", "description": "连续学习 7 天", "icon": "🔥", "unlocked": False},
    {"id": "quarter_way", "name": "四分之一", "description": "学习进度达到 25%", "icon": "📈", "unlocked": False},
    {"id": "halfway", "name": "半途", "description": "学习进度达到 50%", "icon": "🎯", "unlocked": False},
    {"id": "almost_there", "name": "指日可待", "description": "学习进度达到 75%", "icon": "🚀", "unlocked": False},
    {"id": "champion", "name": "冠军", "description": "完成整个学习路径", "icon": "🏆", "unlocked": False}
]

@app.get("/api/v1/progress/stats/{user_id}")
async def get_progress_stats(user_id: str):
    if user_id not in user_stats:
        user_stats[user_id] = {
            "overallProgress": 35,
            "totalItemsCompleted": 24,
            "studyStreak": 7,
            "longestStreak": 14,
            "totalStudyTime": 42.5,
            "experiencePoints": 350,
            "achievementsUnlocked": 3
        }
    return {"status": "success", "stats": {**user_stats[user_id], "totalAchievements": len(achievements_db)}}

@app.get("/api/v1/progress/{user_id}")
async def get_user_progress(user_id: str, path_id: Optional[str] = None):
    return {
        "status": "success",
        "progress": {
            "overall": 35,
            "completedItems": 24,
            "totalItems": 40,
            "byType": {"topic": {"total": 20, "completed": 10}, "resource": {"total": 20, "completed": 14}}
        },
        "statistics": {
            "startDate": "2026-01-01T00:00:00",
            "totalDays": 58,
            "averagePerWeek": 5.0,
            "totalTimeMinutes": 2550,
            "estimatedCompletionDate": "2026-04-01T00:00:00"
        }
    }

@app.get("/api/v1/progress/{user_id}/achievements")
async def get_achievements(user_id: str):
    return {
        "status": "success",
        "achievements": achievements_db,
        "unlocked_ids": ["first_step", "week_streak", "quarter_way"]
    }

@app.get("/api/v1/progress/{user_id}/timeline")
async def get_activity_timeline(user_id: str, days: int = 7):
    from datetime import timedelta
    timeline = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        timeline.append({
            "date": date.strftime("%Y-%m-%d"),
            "items_completed": i % 5,
            "time_spent": (i + 1) * 15,
            "activities": [{"type": "topic", "action": "complete", "completed": True}] * (i % 3)
        })
    return {"status": "success", "timeline": timeline}

@app.get("/api/v1/progress/streak/{user_id}")
async def get_streak(user_id: str):
    return {"status": "success", "streak": 7, "longest_streak": 14}

@app.post("/api/v1/progress/track")
async def track_progress(request: Dict[str, Any]):
    return {"status": "success", "message": "进度已更新", "unlocked_achievements": []}

# 工作流 API（简化版）
workflows = {}
workflow_executions = []

@app.get("/api/v1/workflows")
async def list_workflows():
    return {"status": "success", "workflows": list(workflows.values())}

@app.post("/api/v1/workflows")
async def create_workflow(workflow: Dict[str, Any]):
    workflow_id = f"workflow_{datetime.now().timestamp()}"
    workflow["id"] = workflow_id
    workflow["created_at"] = datetime.now().isoformat()
    workflows[workflow_id] = workflow
    return {"status": "success", "workflow_id": workflow_id}

@app.post("/api/v1/workflows/execute")
async def execute_workflow(workflow: Dict[str, Any]):
    execution_id = f"exec_{datetime.now().timestamp()}"
    execution = {
        "execution_id": execution_id,
        "workflow_id": workflow.get("workflow_id"),
        "status": "success",
        "started_at": datetime.now().isoformat(),
        "nodes_executed": len(workflow.get("nodes", [])),
        "result": {"message": "工作流执行成功"}
    }
    workflow_executions.append(execution)
    return {"status": "success", "execution_id": execution_id, "result": execution}

@app.get("/api/v1/workflows/{workflow_id}/executions")
async def get_workflow_executions(workflow_id: str):
    execs = [e for e in workflow_executions if e.get("workflow_id") == workflow_id]
    return {"status": "success", "workflow_id": workflow_id, "executions": execs}

# AI 对话 API（简化版）
@app.get("/api/v1/chat/providers")
async def get_chat_providers():
    providers = []
    for provider_id, config in api_keys.items():
        if config.get("enabled") and config.get("api_key"):
            providers.append({
                "id": provider_id,
                "name": provider_id.upper(),
                "enabled": True,
                "configured": True
            })
    
    if not providers:
        providers = [
            {"id": "qwen", "name": "通义千问", "enabled": False, "configured": False},
            {"id": "openai", "name": "OpenAI", "enabled": False, "configured": False},
            {"id": "anthropic", "name": "Anthropic", "enabled": False, "configured": False}
        ]
    
    return {"status": "success", "providers": providers}

@app.post("/api/v1/chat/message")
async def chat_message(message_data: Dict[str, Any]):
    message = message_data.get("message", "")
    
    # 简单的关键词回复
    responses = {
        "你好": "你好！我是你的 AI 导师。有什么问题我可以帮助你吗？😊",
        "机器学习": "机器学习是 AI 的一个分支，它让计算机能够从数据中学习。主要分为监督学习、无监督学习和强化学习。你想了解哪个方面？",
        "深度学习": "深度学习是机器学习的一种，使用多层神经网络来学习数据的层次特征。它在图像识别、自然语言处理等领域取得了巨大成功。",
        "python": "Python 是机器学习领域最常用的编程语言，因为它简洁易学且有丰富的库支持，如 NumPy、Pandas、scikit-learn 等。",
        "推荐": "根据你的水平，我推荐：\n\n📚 课程：吴恩达机器学习\n📖 书籍：《机器学习实战》\n💻 实践：Kaggle 入门竞赛",
        "学习路径": "我可以帮你生成个性化的学习路径。请告诉我你的当前水平、学习目标和每周可用时间。",
        "api": "要配置 API，请访问 API 集成页面，选择对应的 AI 提供商，输入 API Key 并保存。",
        "工作流": "工作流功能允许你可视化编排自动化流程。从左侧节点库添加节点，拖拽连接，然后点击运行即可执行。"
    }
    
    # 查找匹配的回复
    response = None
    for key, value in responses.items():
        if key in message.lower():
            response = value
            break
    
    if not response:
        response = f'这是个好问题！关于"{message}"，我可以为你详细解答。\n\n**核心概念：**\n这个问题涉及到 AI 学习的重要知识点。\n\n**建议学习路径：**\n1. 先理解基础概念\n2. 动手实践相关代码\n3. 完成一个小项目巩固\n\n还有其他问题吗？😊'
    
    return {
        "message": response,
        "conversationId": f"conv_{datetime.now().timestamp()}",
        "provider": "qwen" if api_keys["qwen"]["api_key"] else "fallback",
        "suggestions": [
            "能举个具体的例子吗？",
            "这个概念在实际中怎么应用？",
            "有什么学习资源推荐？"
        ],
        "responseTime": 150
    }


# ============== 签到 API ==============

# 签到数据（简化版 - 内存存储）
checkin_records = {}

@app.post("/api/v1/checkin")
async def check_in(user_id: str = "demo_user", username: str = "演示用户"):
    """用户签到"""
    from datetime import date
    
    today = date.today().strftime("%Y-%m-%d")
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 初始化用户记录
    if user_id not in checkin_records:
        checkin_records[user_id] = {
            "user_id": user_id,
            "username": username,
            "checkin_dates": [],
            "current_streak": 0,
            "longest_streak": 0,
            "total_checkins": 0
        }
    
    user_record = checkin_records[user_id]
    
    # 检查今天是否已经签到
    if today in user_record["checkin_dates"]:
        return {
            "status": "already_checked",
            "message": "今天已经签到过了",
            "streak": user_record["current_streak"],
            "total_checkins": user_record["total_checkins"]
        }
    
    # 检查是否连续签到
    if yesterday in user_record["checkin_dates"]:
        user_record["current_streak"] += 1
    else:
        user_record["current_streak"] = 1
    
    # 更新最长连击
    if user_record["current_streak"] > user_record["longest_streak"]:
        user_record["longest_streak"] = user_record["current_streak"]
    
    # 添加今天的签到记录
    user_record["checkin_dates"].append(today)
    user_record["total_checkins"] += 1
    
    # 返回结果
    return {
        "status": "success",
        "message": "签到成功！",
        "streak": user_record["current_streak"],
        "longest_streak": user_record["longest_streak"],
        "total_checkins": user_record["total_checkins"],
        "today": today
    }


@app.get("/api/v1/checkin/info")
async def get_checkin_info(user_id: str = "demo_user"):
    """获取用户签到信息"""
    from datetime import date, timedelta
    
    today = date.today().strftime("%Y-%m-%d")
    
    # 初始化用户记录
    if user_id not in checkin_records:
        checkin_records[user_id] = {
            "user_id": user_id,
            "username": "演示用户",
            "checkin_dates": [],
            "current_streak": 0,
            "longest_streak": 0,
            "total_checkins": 0
        }
    
    user_record = checkin_records[user_id]
    
    # 计算今天的签到状态
    today_checked = today in user_record["checkin_dates"]
    
    # 生成最近一个月的日历
    calendar = []
    for i in range(30):
        check_date = (date.today() - timedelta(days=29-i)).strftime("%Y-%m-%d")
        day_num = int(check_date.split('-')[2])
        calendar.append({
            "date": check_date,
            "day": day_num,
            "checked": check_date in user_record["checkin_dates"],
            "is_today": check_date == today
        })
    
    return {
        "current_streak": user_record["current_streak"],
        "longest_streak": user_record["longest_streak"],
        "total_checkins": user_record["total_checkins"],
        "last_checkin": user_record["checkin_dates"][-1] if user_record["checkin_dates"] else None,
        "today_checked": today_checked,
        "checkin_calendar": calendar
    }


@app.get("/api/v1/checkin/stats")
async def get_checkin_stats():
    """获取全局签到统计"""
    from app.services.checkin_service import get_checkin_stats
    return get_checkin_stats()


# ============== 宠物养成 API ==============

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

def get_or_create_pet_memory(user_id: str):
    """获取或创建用户宠物（内存版）"""
    if user_id not in pets_db:
        pet_type_data = PET_TYPES[0]  # 默认选择第一个类型
        pet = {
            "user_id": user_id,
            "name": f"{pet_type_data['name']}",
            "pet_type": pet_type_data["id"],
            "avatar_url": None,
            "level": 1,
            "experience": 0,
            "experience_to_next_level": 100,
            "happiness": 50,
            "energy": 100,
            "health": 100,
            "total_interactions": 0,
            "consecutive_days": 0,
            "created_at": datetime.now().isoformat(),
            "last_interaction_at": datetime.now().isoformat(),
            "total_study_time": 0,
            "checkin_days": 0
        }
        pets_db[user_id] = pet
    return pets_db[user_id]

def get_pet_status_memory(user_id: str):
    """获取宠物状态（内存版）"""
    pet = get_or_create_pet_memory(user_id)
    
    level_info = PET_LEVELS.get(pet["level"], PET_LEVELS[max(PET_LEVELS.keys())])
    pet_type_data = next((p for p in PET_TYPES if p["id"] == pet["pet_type"]), PET_TYPES[0])
    
    # 生成宠物消息
    messages = []
    if pet["happiness"] < 30:
        messages.append(f"{pet_type_data['icon']} 看起来有点不开心，来陪陪我吧...😢")
    elif pet["happiness"] > 80:
        messages.append(f"{pet_type_data['icon']} 今天心情超好的！继续加油！😄")

    if pet["energy"] < 20:
        messages.append(f"{pet_type_data['icon']} 好累啊...让我休息一下吧😴")
    elif pet["energy"] > 80:
        messages.append(f"{pet_type_data['icon']} 精力充沛！一起学习吧！💪")

    if pet["level"] == 1:
        messages.append("我还在蛋里，需要更多学习才能孵化哦！🥚")
    elif pet["level"] < 5:
        messages.append(f"我会和你一起成长的！当前等级：{level_info['name']}")
    else:
        messages.append(f"我已经是{level_info['name']}了！继续变强吧！")

    if pet.get("last_interaction_at"):
        from datetime import datetime
        last_interaction = datetime.fromisoformat(pet["last_interaction_at"].replace('Z', '+00:00'))
        hours_since = (datetime.now(last_interaction.tzinfo) - last_interaction).total_seconds() / 3600
        if hours_since > 24:
            messages.append(f"你已经{int(hours_since)}小时没理我了...😢")
        if hours_since > 12 and pet["happiness"] > 50:
            messages.append("主人，今天还没学习哦~ 我等你很久了！📚")

    if not messages:
        messages.append(f"{pet_type_data['icon']} 随时准备和你一起学习！")

    return {
        "pet_type": pet["pet_type"],
        "pet_name": pet["name"],
        "icon": pet_type_data["icon"],
        "level": pet["level"],
        "level_name": level_info["name"],
        "exp": pet["experience"],
        "exp_to_next": pet["experience_to_next_level"],
        "happiness": pet["happiness"],
        "energy": pet["energy"],
        "health": pet["health"],
        "total_interactions": pet["total_interactions"],
        "consecutive_days": pet["consecutive_days"],
        "message": " ".join(messages),
        "created_at": pet["created_at"],
        "last_interaction": pet["last_interaction_at"],
        "total_study_time": pet.get("total_study_time", 0),
        "checkin_days": pet.get("checkin_days", 0)
    }

def add_exp_memory(user_id: str, exp: int, reason: str = "学习"):
    """增加宠物经验（内存版）"""
    pet = get_or_create_pet_memory(user_id)
    
    pet["experience"] += exp
    pet["total_interactions"] += 1
    pet["last_interaction_at"] = datetime.now().isoformat()

    # 检查升级
    level_ups = []
    while pet["experience"] >= pet["experience_to_next_level"] and pet["level"] < max(PET_LEVELS.keys()):
        pet["level"] += 1
        pet["experience"] -= pet["experience_to_next_level"]
        pet["experience_to_next_level"] = int(pet["experience_to_next_level"] * 1.5)

        level_info = PET_LEVELS.get(pet["level"], PET_LEVELS[max(PET_LEVELS.keys())])
        level_ups.append({
            "level": pet["level"],
            "name": level_info["name"],
            "icon": level_info["icon"]
        })

    return {
        "status": "success",
        "exp_added": exp,
        "reason": reason,
        "current_exp": pet["experience"],
        "exp_to_next": pet["experience_to_next_level"],
        "level": pet["level"],
        "level_ups": level_ups
    }

def interact_memory(user_id: str, action: str):
    """与宠物互动（内存版）"""
    pet = get_or_create_pet_memory(user_id)

    pet["last_interaction_at"] = datetime.now().isoformat()
    pet["total_interactions"] += 1

    if action == "feed":
        pet["happiness"] = min(100, pet["happiness"] + 15)
        pet["energy"] = min(100, pet["energy"] + 10)
        pet_type_data = next((p for p in PET_TYPES if p["id"] == pet["pet_type"]), PET_TYPES[0])
        message = f"{pet_type_data['icon']} 吃饱了，好开心！"
        exp_gain = 5
    elif action == "play":
        pet["happiness"] = min(100, pet["happiness"] + 20)
        pet["energy"] = max(0, pet["energy"] - 10)
        pet_type_data = next((p for p in PET_TYPES if p["id"] == pet["pet_type"]), PET_TYPES[0])
        message = f"{pet_type_data['icon']} 玩得很开心！"
        exp_gain = 10
    elif action == "rest":
        pet["energy"] = min(100, pet["energy"] + 30)
        pet["happiness"] = min(100, pet["happiness"] + 5)
        pet_type_data = next((p for p in PET_TYPES if p["id"] == pet["pet_type"]), PET_TYPES[0])
        message = f"{pet_type_data['icon']} 休息好了，精力充沛！"
        exp_gain = 5
    elif action == "study":
        pet["happiness"] = min(100, pet["happiness"] + 5)
        pet["energy"] = max(0, pet["energy"] - 5)
        pet_type_data = next((p for p in PET_TYPES if p["id"] == pet["pet_type"]), PET_TYPES[0])
        message = f"{pet_type_data['icon']} 陪你一起学习！"
        exp_gain = 20
    else:
        message = "未知的互动动作"
        exp_gain = 0

    return {
        "status": "success",
        "message": message,
        "happiness": pet["happiness"],
        "energy": pet["energy"],
        "exp_gain": exp_gain
    }

def check_in_bonus_memory(user_id: str):
    """签到奖励（内存版）"""
    pet = get_or_create_pet_memory(user_id)

    pet["consecutive_days"] += 1
    pet["happiness"] = min(100, pet["happiness"] + 10)
    pet["energy"] = min(100, pet["energy"] + 20)

    base_exp = 20
    streak_bonus = min(pet["consecutive_days"], 30)
    total_exp = base_exp + streak_bonus

    result = add_exp_memory(user_id, total_exp, "签到奖励")
    return result

@app.get("/api/v1/pet")
async def get_pet(user_id: str = "demo_user"):
    """获取用户宠物信息"""
    return get_pet_status_memory(user_id)


@app.post("/api/v1/pet/create")
async def create_pet(user_id: str = "demo_user", pet_type: str = None):
    """创建宠物"""
    pet = get_or_create_pet_memory(user_id)
    if pet_type:
        pet["pet_type"] = pet_type
        pet_type_data = next((p for p in PET_TYPES if p["id"] == pet_type), PET_TYPES[0])
        pet["name"] = f"{pet_type_data['name']}"
    return get_pet_status_memory(user_id)


@app.post("/api/v1/pet/exp")
async def add_pet_exp(user_id: str = "demo_user", exp: int = 10, reason: str = "学习"):
    """增加宠物经验"""
    result = add_exp_memory(user_id, exp, reason)
    result["pet"] = get_pet_status_memory(user_id)
    return result


@app.post("/api/v1/pet/interact")
async def pet_interact(user_id: str = "demo_user", action: str = "feed"):
    """与宠物互动"""
    result = interact_memory(user_id, action)
    result["pet"] = get_pet_status_memory(user_id)
    return result


@app.get("/api/v1/pet/types")
async def get_pet_types():
    """获取所有宠物类型"""
    return {"types": PET_TYPES}


@app.post("/api/v1/pet/checkin-bonus")
async def pet_checkin_bonus(user_id: str = "demo_user"):
    """签到后给宠物奖励"""
    result = check_in_bonus_memory(user_id)
    result["pet"] = get_pet_status_memory(user_id)
    return result


# ============== OpenClaw API ==============

@app.post("/api/v1/openclaw/process")
async def openclaw_process(request: Request):
    """处理OpenClaw请求"""
    data = await request.json()
    input_text = data.get("input_text", "")
    
    # 模拟处理结果
    result = {
        "response": f"OpenClaw处理了您的请求: {input_text}",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }
    
    return result


@app.post("/api/v1/openclaw/execute-skill")
async def openclaw_execute_skill(request: Request):
    """执行OpenClaw技能"""
    data = await request.json()
    skill_name = data.get("skill_name", "")
    params = data.get("params", {})
    
    # 模拟技能执行结果
    result = {
        "skill_name": skill_name,
        "result": f"技能'{skill_name}'执行完成",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "params_used": params
    }
    
    return result


@app.get("/api/v1/openclaw/skills")
async def openclaw_get_skills():
    """获取可用技能列表"""
    return {"skills": openclaw_skills}


@app.post("/api/v1/openclaw/chat")
async def openclaw_chat(request: Request):
    """OpenClaw聊天功能"""
    data = await request.json()
    message = data.get("message", "")
    conversation_id = data.get("conversation_id", "default")
    
    # 初始化对话历史
    if conversation_id not in openclaw_conversations:
        openclaw_conversations[conversation_id] = []
    
    # 添加用户消息到对话历史
    user_msg = {
        "role": "user",
        "content": message,
        "timestamp": datetime.now().isoformat()
    }
    openclaw_conversations[conversation_id].append(user_msg)
    
    # 生成AI回复
    ai_response = f"关于'{message}'，我可以为您提供帮助。"
    
    # 添加AI回复到对话历史
    ai_msg = {
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now().isoformat()
    }
    openclaw_conversations[conversation_id].append(ai_msg)
    
    return {
        "reply": ai_response,
        "conversation_id": conversation_id,
        "message_count": len(openclaw_conversations[conversation_id]),
        "status": "success"
    }


@app.get("/api/v1/openclaw/health")
async def openclaw_health():
    """OpenClaw健康检查"""
    return {"status": "healthy", "service": "openclaw", "version": "1.0.0"}


# ============== 多媒体AI API ==============

# 存储多媒体任务
multimedia_jobs = {}

@app.post("/api/v1/multimedia/text-to-image")
async def text_to_image(request: Request):
    """文本生成图像"""
    data = await request.json()
    prompt = data.get("prompt", "")
    negative_prompt = data.get("negative_prompt", "")
    width = data.get("width", 1024)
    height = data.get("height", 1024)
    num_images = data.get("num_images", 1)
    
    # 生成模拟图像URL
    job_id = f"img_{len(multimedia_jobs) + 1}"
    image_urls = [f"http://localhost:8001/generated/{job_id}_img_{i+1}.jpg" for i in range(num_images)]
    
    result = {
        "job_id": job_id,
        "status": "completed",
        "images": image_urls,
        "prompt": prompt,
        "dimensions": {"width": width, "height": height},
        "timestamp": datetime.now().isoformat()
    }
    
    multimedia_jobs[job_id] = result
    
    return result


@app.post("/api/v1/multimedia/image-to-image")
async def image_to_image(request: Request):
    """图像生成图像"""
    data = await request.json()
    prompt = data.get("prompt", "")
    image_url = data.get("image_url", "")
    strength = data.get("strength", 0.7)
    
    # 生成模拟图像URL
    job_id = f"i2i_{len(multimedia_jobs) + 1}"
    result_image_url = f"http://localhost:8001/generated/{job_id}_converted.jpg"
    
    result = {
        "job_id": job_id,
        "status": "completed",
        "original_image": image_url,
        "result_image": result_image_url,
        "prompt": prompt,
        "strength": strength,
        "timestamp": datetime.now().isoformat()
    }
    
    multimedia_jobs[job_id] = result
    
    return result


@app.post("/api/v1/multimedia/generate-video")
async def generate_video(request: Request):
    """生成视频"""
    data = await request.json()
    prompt = data.get("prompt", "")
    duration = data.get("duration", 5)
    
    # 生成模拟视频URL
    job_id = f"vid_{len(multimedia_jobs) + 1}"
    video_url = f"http://localhost:8001/generated/{job_id}_video.mp4"
    
    result = {
        "job_id": job_id,
        "status": "completed",
        "video_url": video_url,
        "prompt": prompt,
        "duration": duration,
        "timestamp": datetime.now().isoformat()
    }
    
    multimedia_jobs[job_id] = result
    
    return result


@app.post("/api/v1/multimedia/edit-image")
async def edit_image(request: Request):
    """编辑图像"""
    data = await request.json()
    image_url = data.get("image_url", "")
    instruction = data.get("instruction", "")
    
    # 生成模拟编辑后的图像URL
    job_id = f"edit_{len(multimedia_jobs) + 1}"
    edited_image_url = f"http://localhost:8001/generated/{job_id}_edited.jpg"
    
    result = {
        "job_id": job_id,
        "status": "completed",
        "original_image": image_url,
        "edited_image": edited_image_url,
        "instruction": instruction,
        "timestamp": datetime.now().isoformat()
    }
    
    multimedia_jobs[job_id] = result
    
    return result


@app.get("/api/v1/multimedia/styles")
async def get_styles():
    """获取可用样式"""
    styles = [
        {"id": "realistic", "name": "真实风格", "description": "逼真的图像效果"},
        {"id": "anime", "name": "动漫风格", "description": "日本动漫风格效果"},
        {"id": "oil-painting", "name": "油画风格", "description": "古典油画艺术效果"},
        {"id": "watercolor", "name": "水彩风格", "description": "清新水彩画效果"},
        {"id": "cyberpunk", "name": "赛博朋克", "description": "未来科技风格效果"},
        {"id": "pixel-art", "name": "像素艺术", "description": "复古像素风格效果"}
    ]
    return {"styles": styles}


@app.get("/api/v1/multimedia/job-status/{job_id}")
async def get_job_status(job_id: str):
    """获取任务状态"""
    if job_id in multimedia_jobs:
        return multimedia_jobs[job_id]
    else:
        return {"status": "not_found", "error": "Job not found"}


@app.get("/api/v1/multimedia/health")
async def multimedia_health():
    """多媒体服务健康检查"""
    return {"status": "healthy", "service": "multimedia", "version": "1.0.0"}


# ============== 图像去水印 API ==============

# 模拟去水印处理
watermark_removal_jobs = {}

def process_real_watermark_removal(image_url: str, mask_url: str = None, technique: str = "auto"):
    """
    实际的去水印处理
    调用图像处理模块进行真实处理
    """
    from app.image_processing import process_watermark_removal
    import time
    
    start_time = time.time()
    
    # 调用图像处理模块
    result = process_watermark_removal(image_url, mask_url, technique)
    
    processing_time = time.time() - start_time
    
    # 构建返回结果
    job_result = {
        "status": "completed",
        "original_image": image_url,
        "result_image": result["result_image"],  # base64编码的图像
        "mask_used": result["mask_used"],
        "technique_used": result["technique_used"],
        "processing_time": round(processing_time, 2),
        "quality_score": 0.9,  # 在真实实现中，可以计算图像质量指标
        "timestamp": datetime.now().isoformat(),
        "original_shape": result["original_shape"],
        "result_shape": result["result_shape"]
    }
    
    return job_result

@app.post("/api/v1/multimedia/remove-watermark")
async def remove_watermark(request: Request):
    """去除图像水印"""
    data = await request.json()
    image_url = data.get("image_url", "")
    mask_url = data.get("mask_url", "")  # 可选的遮罩，标识水印位置
    technique = data.get("technique", "auto")  # 去除技术: auto, inpainting, detection

    # 生成任务ID
    job_id = f"wm_{len(watermark_removal_jobs) + 1}"
    
    # 更新任务状态为处理中
    watermark_removal_jobs[job_id] = {
        "job_id": job_id,
        "status": "processing",
        "original_image": image_url,
        "mask_used": bool(mask_url),
        "technique_used": technique,
        "started_at": datetime.now().isoformat()
    }
    
    # 在实际应用中，这里应该启动后台任务
    # 为了简化，我们直接处理（在真实实现中应异步处理）
    try:
        result = process_real_watermark_removal(image_url, mask_url, technique)
        
        # 更新任务结果
        result["job_id"] = job_id
        watermark_removal_jobs[job_id] = result
        
        return result
    except Exception as e:
        # 处理错误情况
        error_result = {
            "job_id": job_id,
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        watermark_removal_jobs[job_id] = error_result
        return error_result


@app.get("/api/v1/multimedia/watermark-removal/{job_id}")
async def get_watermark_removal_result(job_id: str):
    """获取去水印结果"""
    if job_id in watermark_removal_jobs:
        return watermark_removal_jobs[job_id]
    else:
        return {"status": "not_found", "error": "Job not found"}


@app.get("/api/v1/multimedia/watermark-removal/techniques")
async def get_watermark_removal_techniques():
    """获取可用的去水印技术"""
    techniques = [
        {
            "id": "auto",
            "name": "自动检测",
            "description": "自动检测并移除水印",
            "recommended": True
        },
        {
            "id": "inpainting",
            "name": "图像修复",
            "description": "使用图像修复技术填充水印区域",
            "recommended": False
        },
        {
            "id": "detection",
            "name": "智能检测",
            "description": "先检测水印位置再进行精确移除",
            "recommended": False
        }
    ]
    return {"techniques": techniques}


# ============== 工作流 API ==============

class WorkflowExecute(BaseModel):
    nodes: list
    edges: list
    logic: str = "AND"
    input_data: Optional[Dict] = None

class WorkflowCreate(BaseModel):
    name: str
    nodes: list
    edges: list
    logic: str = "AND"

@app.post("/api/v1/workflows/execute")
async def execute_workflow(workflow: WorkflowExecute):
    """执行工作流"""
    from app.workflow_engine import workflow_engine
    
    workflow_id = f"wf_{datetime.now().timestamp()}"
    result = await workflow_engine.execute_workflow(
        workflow_id=workflow_id,
        nodes=workflow.nodes,
        edges=workflow.edges,
        logic=workflow.logic,
        input_data=workflow.input_data
    )
    
    return {
        "status": "success",
        "execution_id": result["execution_id"],
        "result": {"status": result["status"]},
        "nodes_executed": len(result["nodes"]),
        "execution_time": result.get("completed_at", "")
    }


@app.get("/api/v1/workflows/nodes")
async def get_workflow_nodes():
    """获取所有节点定义"""
    from app.workflow_engine import workflow_engine
    return {"nodes": workflow_engine.get_node_definitions()}


@app.get("/api/v1/workflows/executions/{execution_id}")
async def get_execution_status(execution_id: str):
    """获取执行状态"""
    from app.workflow_engine import workflow_engine
    result = workflow_engine.get_execution_status(execution_id)
    if result:
        return {"status": "success", "execution": result}
    return {"status": "error", "message": "Execution not found"}


# 工作流存储
workflows_db: Dict[str, Dict] = {}

class WorkflowCreate(BaseModel):
    name: str
    nodes: list
    edges: list
    logic: str = "AND"

@app.post("/api/v1/workflows")
async def save_workflow(workflow: WorkflowCreate):
    """保存工作流"""
    workflow_id = f"wf_{datetime.now().timestamp()}"
    workflows_db[workflow_id] = {
        "id": workflow_id,
        "name": workflow.name,
        "nodes": workflow.nodes,
        "edges": workflow.edges,
        "logic": workflow.logic,
        "created_at": datetime.now().isoformat()
    }
    return {"status": "success", "workflow_id": workflow_id}


@app.get("/api/v1/workflows")
async def list_workflows():
    """获取所有工作流"""
    return {"status": "success", "workflows": list(workflows_db.values())}


@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """获取单个工作流"""
    if workflow_id in workflows_db:
        return {"status": "success", "workflow": workflows_db[workflow_id]}
    return {"status": "error", "message": "Workflow not found"}


@app.delete("/api/v1/workflows/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """删除工作流"""
    if workflow_id in workflows_db:
        del workflows_db[workflow_id]
        return {"status": "success", "message": "Workflow deleted"}
    return {"status": "error", "message": "Workflow not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
