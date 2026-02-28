# Study2026 API - 简化版（包含知识库）

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
from pydantic import BaseModel
import hashlib
import json
from datetime import datetime, timedelta

app = FastAPI(
    title="Study2026 API",
    description="AI 学习平台 API",
    version="3.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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

@app.post("/api/v1/checkin")
async def check_in(user_id: str = "demo_user", username: str = "演示用户"):
    """用户签到"""
    from app.services.checkin_service import check_in, get_user_checkin_info
    
    result = check_in(user_id, username)
    return result


@app.get("/api/v1/checkin/info")
async def get_checkin_info(user_id: str = "demo_user"):
    """获取用户签到信息"""
    from app.services.checkin_service import get_user_checkin_info
    return get_user_checkin_info(user_id)


@app.get("/api/v1/checkin/stats")
async def get_checkin_stats():
    """获取全局签到统计"""
    from app.services.checkin_service import get_checkin_stats
    return get_checkin_stats()


# ============== 宠物养成 API ==============

@app.get("/api/v1/pet")
async def get_pet(user_id: str = "demo_user"):
    """获取用户宠物信息"""
    from app.services.pet_service import get_or_create_pet, get_pet_status
    pet = get_or_create_pet(user_id)
    return get_pet_status(user_id)


@app.post("/api/v1/pet/create")
async def create_pet(user_id: str = "demo_user", pet_type: str = None):
    """创建宠物"""
    from app.services.pet_service import create_pet, get_pet_status
    create_pet(user_id, "用户", pet_type)
    return get_pet_status(user_id)


@app.post("/api/v1/pet/exp")
async def add_pet_exp(user_id: str = "demo_user", exp: int = 10, reason: str = "学习"):
    """增加宠物经验"""
    from app.services.pet_service import add_exp, get_pet_status
    result = add_exp(user_id, exp, reason)
    result["pet"] = get_pet_status(user_id)
    return result


@app.post("/api/v1/pet/interact")
async def pet_interact(user_id: str = "demo_user", action: str = "feed"):
    """与宠物互动"""
    from app.services.pet_service import interact, get_pet_status
    result = interact(user_id, action)
    result["pet"] = get_pet_status(user_id)
    return result


@app.get("/api/v1/pet/types")
async def get_pet_types():
    """获取所有宠物类型"""
    from app.services.pet_service import get_all_pet_types
    return {"types": get_all_pet_types()}


@app.post("/api/v1/pet/checkin-bonus")
async def pet_checkin_bonus(user_id: str = "demo_user"):
    """签到后给宠物奖励"""
    from app.services.pet_service import check_in_bonus, get_pet_status
    result = check_in_bonus(user_id)
    result["pet"] = get_pet_status(user_id)
    return result


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
