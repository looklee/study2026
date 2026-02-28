from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, HttpUrl
import httpx
import datetime
import random
import os

# 导入 AI 服务
from app.services.qwen_service import get_qwen_service, get_coding_plan_service

app = FastAPI(
    title="Study2026 API",
    description="AI 学习平台 API - 支持第三方 API 接入",
    version="2.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== 数据模型 ==============

class APIIntegration(BaseModel):
    """API 集成配置"""
    id: str
    name: str
    description: str
    base_url: str
    api_key: Optional[str] = None
    status: str = "active"
    category: str
    endpoints: List[Dict[str, Any]]

class AITool(BaseModel):
    """AI 工具"""
    id: str
    name: str
    description: str
    url: str
    category: str
    tags: List[str]
    rating: float
    isFree: bool
    features: List[str]

class BilibiliVideo(BaseModel):
    """B 站视频"""
    id: str
    title: str
    author: str
    url: str
    cover: str
    duration: str
    views: int
    pubdate: str
    description: str

# ============== 内存数据存储 ==============

# API 集成配置
api_integrations = {
    "qwen": {
        "id": "qwen",
        "name": "通义千问 (Qwen)",
        "description": "阿里云通义千问大模型",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key": os.getenv("QWEN_API_KEY"),
        "status": "active" if os.getenv("QWEN_API_KEY") else "pending",
        "category": "AI",
        "icon": "🤖",
        "endpoints": [
            {"method": "POST", "path": "/chat/completions", "description": "聊天对话"},
            {"method": "POST", "path": "/generate", "description": "内容生成"}
        ]
    },
    "coding_plan": {
        "id": "coding_plan",
        "name": "Coding Plan API",
        "description": "编程学习计划生成 API",
        "base_url": "https://api.codingplan.example.com",
        "api_key": os.getenv("CODING_PLAN_API_KEY"),
        "status": "active" if os.getenv("CODING_PLAN_API_KEY") else "pending",
        "category": "education",
        "icon": "📚",
        "endpoints": [
            {"method": "GET", "path": "/plans", "description": "获取学习计划"},
            {"method": "POST", "path": "/plans/generate", "description": "生成学习计划"}
        ]
    },
    "github": {
        "id": "github",
        "name": "GitHub API",
        "description": "GitHub 代码仓库和项目管理",
        "base_url": "https://api.github.com",
        "api_key": os.getenv("GITHUB_TOKEN"),
        "status": "active" if os.getenv("GITHUB_TOKEN") else "pending",
        "category": "development",
        "icon": "💻",
        "endpoints": [
            {"method": "GET", "path": "/search/repositories", "description": "搜索仓库"},
            {"method": "GET", "path": "/users/{user}/repos", "description": "获取用户仓库"}
        ]
    },
    "openai": {
        "id": "openai",
        "name": "OpenAI API",
        "description": "GPT-4、ChatGPT 等 AI 模型",
        "base_url": "https://api.openai.com/v1",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "status": "active" if os.getenv("OPENAI_API_KEY") else "pending",
        "category": "AI",
        "icon": "🧠",
        "endpoints": [
            {"method": "POST", "path": "/chat/completions", "description": "聊天对话"}
        ]
    },
    "anthropic": {
        "id": "anthropic",
        "name": "Anthropic API",
        "description": "Claude AI 助手",
        "base_url": "https://api.anthropic.com",
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
        "status": "active" if os.getenv("ANTHROPIC_API_KEY") else "pending",
        "category": "AI",
        "icon": "🤖",
        "endpoints": [
            {"method": "POST", "path": "/v1/messages", "description": "聊天对话"}
        ]
    }
}

# AI 工具数据库
ai_tools = [
    {
        "id": "1",
        "name": "ChatGPT",
        "description": "OpenAI 的大型语言模型，支持对话、写作、编程等多种任务",
        "url": "https://chat.openai.com",
        "category": "language",
        "tags": ["chatbot", "writing", "coding", "general"],
        "rating": 4.8,
        "isFree": False,
        "features": ["对话", "写作辅助", "代码生成", "翻译"]
    },
    {
        "id": "2",
        "name": "Claude",
        "description": "Anthropic 的 AI 助手，擅长长文本理解和分析",
        "url": "https://claude.ai",
        "category": "language",
        "tags": ["chatbot", "analysis", "writing"],
        "rating": 4.7,
        "isFree": True,
        "features": ["长文本处理", "文档分析", "对话"]
    },
    {
        "id": "3",
        "name": "Midjourney",
        "description": "AI 图像生成工具，创建高质量艺术作品",
        "url": "https://midjourney.com",
        "category": "image",
        "tags": ["image-generation", "art", "design"],
        "rating": 4.6,
        "isFree": False,
        "features": ["图像生成", "艺术创作", "风格转换"]
    },
    {
        "id": "4",
        "name": "GitHub Copilot",
        "description": "AI 编程助手，自动完成代码",
        "url": "https://github.com/features/copilot",
        "category": "coding",
        "tags": ["coding", "autocomplete", "productivity"],
        "rating": 4.5,
        "isFree": False,
        "features": ["代码补全", "函数生成", "注释生成"]
    },
    {
        "id": "5",
        "name": "Notion AI",
        "description": "Notion 内置的 AI 助手，帮助写作和整理",
        "url": "https://notion.so",
        "category": "productivity",
        "tags": ["writing", "notes", "productivity"],
        "rating": 4.4,
        "isFree": False,
        "features": ["写作辅助", "摘要生成", "翻译"]
    },
    {
        "id": "6",
        "name": "Runway ML",
        "description": "AI 视频编辑和生成工具",
        "url": "https://runwayml.com",
        "category": "video",
        "tags": ["video", "editing", "generation"],
        "rating": 4.3,
        "isFree": False,
        "features": ["视频编辑", "绿幕抠图", "视频生成"]
    },
    {
        "id": "7",
        "name": "ElevenLabs",
        "description": "AI 语音合成，生成自然的人声",
        "url": "https://elevenlabs.io",
        "category": "audio",
        "tags": ["voice", "speech", "audio"],
        "rating": 4.5,
        "isFree": True,
        "features": ["语音合成", "声音克隆", "多语言"]
    },
    {
        "id": "8",
        "name": "Perplexity AI",
        "description": "AI 搜索引擎，提供准确的答案和引用",
        "url": "https://perplexity.ai",
        "category": "search",
        "tags": ["search", "research", "qa"],
        "rating": 4.6,
        "isFree": True,
        "features": ["智能搜索", "引用来源", "实时信息"]
    },
    {
        "id": "9",
        "name": "Cursor",
        "description": "AI 驱动的代码编辑器",
        "url": "https://cursor.sh",
        "category": "coding",
        "tags": ["editor", "coding", "ide"],
        "rating": 4.7,
        "isFree": True,
        "features": ["AI 对话", "代码生成", "智能补全"]
    },
    {
        "id": "10",
        "name": "Gamma",
        "description": "AI 演示文稿生成工具",
        "url": "https://gamma.app",
        "category": "productivity",
        "tags": ["presentation", "slides", "design"],
        "rating": 4.4,
        "isFree": True,
        "features": ["PPT 生成", "设计模板", "内容优化"]
    },
    {
        "id": "11",
        "name": "Tome",
        "description": "AI 故事叙述和演示工具",
        "url": "https://tome.app",
        "category": "productivity",
        "tags": ["storytelling", "presentation"],
        "rating": 4.3,
        "isFree": True,
        "features": ["故事生成", "演示创建", "图像生成"]
    },
    {
        "id": "12",
        "name": "Jasper",
        "description": "AI 内容创作平台",
        "url": "https://jasper.ai",
        "category": "writing",
        "tags": ["writing", "marketing", "content"],
        "rating": 4.2,
        "isFree": False,
        "features": ["博客写作", "营销文案", "社交媒体"]
    }
]

# B 站 AI 教程视频（模拟数据）
bilibili_videos = [
    {
        "id": "BV1xx411c7mD",
        "title": "【吴恩达】机器学习 2022 完整版",
        "author": "AI 学习社",
        "url": "https://www.bilibili.com/video/BV1xx411c7mD",
        "cover": "https://i0.hdslb.com/bfs/archive/example1.jpg",
        "duration": "11:23:45",
        "views": 1250000,
        "pubdate": "2024-01-15",
        "description": "吴恩达教授机器学习课程完整中文版"
    },
    {
        "id": "BV1xx411c7mE",
        "title": "PyTorch 深度学习入门教程",
        "author": "深度学习学院",
        "url": "https://www.bilibili.com/video/BV1xx411c7mE",
        "cover": "https://i0.hdslb.com/bfs/archive/example2.jpg",
        "duration": "8:15:30",
        "views": 850000,
        "pubdate": "2024-02-10",
        "description": "从零开始学习 PyTorch 深度学习框架"
    },
    {
        "id": "BV1xx411c7mF",
        "title": "Transformer 模型详解",
        "author": "NLP 讲堂",
        "url": "https://www.bilibili.com/video/BV1xx411c7mF",
        "cover": "https://i0.hdslb.com/bfs/archive/example3.jpg",
        "duration": "2:45:20",
        "views": 620000,
        "pubdate": "2024-02-20",
        "description": "深入理解 Transformer 架构和注意力机制"
    },
    {
        "id": "BV1xx411c7mG",
        "title": "LLM 大语言模型实战",
        "author": "AI 实战派",
        "url": "https://www.bilibili.com/video/BV1xx411c7mG",
        "cover": "https://i0.hdslb.com/bfs/archive/example4.jpg",
        "duration": "5:30:15",
        "views": 980000,
        "pubdate": "2024-02-25",
        "description": "大语言模型应用开发完整教程"
    }
]

# ============== API 端点 ==============

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Study2026 API v2.0 - 支持第三方 API 接入",
        "version": "2.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# ============== 第三方 API 集成 ==============

@app.get("/api/v1/integrations")
async def list_integrations():
    """获取所有 API 集成"""
    return list(api_integrations.values())


@app.get("/api/v1/integrations/{integration_id}")
async def get_integration(integration_id: str):
    """获取特定 API 集成"""
    if integration_id not in api_integrations:
        raise HTTPException(status_code=404, detail="集成不存在")
    return api_integrations[integration_id]


@app.post("/api/v1/integrations/{integration_id}/configure")
async def configure_integration(integration_id: str, config: Dict[str, Any]):
    """配置 API 集成"""
    if integration_id not in api_integrations:
        raise HTTPException(status_code=404, detail="集成不存在")
    
    integration = api_integrations[integration_id]
    if "api_key" in config:
        integration["api_key"] = config["api_key"]
    if "status" in config:
        integration["status"] = config["status"]
    
    return {"status": "success", "integration": integration}


@app.post("/api/v1/integrations/{integration_id}/test")
async def test_integration(integration_id: str):
    """测试 API 集成连接"""
    if integration_id not in api_integrations:
        raise HTTPException(status_code=404, detail="集成不存在")
    
    integration = api_integrations[integration_id]
    
    # 模拟测试连接
    try:
        # 实际应该发起真实请求
        return {
            "status": "success",
            "message": f"成功连接到 {integration['name']}",
            "response_time": random.randint(50, 200)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/api/v1/integrations/{integration_id}/proxy/{path:path}")
async def proxy_request(integration_id: str, path: str, request_data: Dict[str, Any]):
    """代理请求到第三方 API"""
    if integration_id not in api_integrations:
        raise HTTPException(status_code=404, detail="集成不存在")
    
    integration = api_integrations[integration_id]
    
    if not integration.get("api_key"):
        raise HTTPException(status_code=400, detail="请先配置 API 密钥")
    
    # 构建请求
    url = f"{integration['base_url']}/{path}"
    headers = {
        "Authorization": f"Bearer {integration['api_key']}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=request_data, headers=headers)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"请求失败：{str(e)}")


# ============== AI 工具 ==============

@app.get("/api/v1/ai-tools")
async def list_ai_tools(category: Optional[str] = None, tag: Optional[str] = None):
    """获取 AI 工具列表"""
    tools = ai_tools
    
    if category:
        tools = [t for t in tools if t["category"] == category]
    if tag:
        tools = [t for t in tools if tag in t["tags"]]
    
    return {
        "total": len(tools),
        "categories": list(set(t["category"] for t in ai_tools)),
        "tools": tools
    }


@app.get("/api/v1/ai-tools/{tool_id}")
async def get_ai_tool(tool_id: str):
    """获取 AI 工具详情"""
    for tool in ai_tools:
        if tool["id"] == tool_id:
            return tool
    raise HTTPException(status_code=404, detail="工具不存在")


@app.post("/api/v1/ai-tools/suggest")
async def suggest_ai_tool(task: str):
    """根据任务推荐 AI 工具"""
    task_lower = task.lower()
    
    # 简单关键词匹配
    if any(word in task_lower for word in ["写", "文章", "内容"]):
        recommendations = [t for t in ai_tools if t["category"] in ["writing", "language"]]
    elif any(word in task_lower for word in ["图", "设计", "画"]):
        recommendations = [t for t in ai_tools if t["category"] == "image"]
    elif any(word in task_lower for word in ["代码", "编程", "开发"]):
        recommendations = [t for t in ai_tools if t["category"] == "coding"]
    elif any(word in task_lower for word in ["视频", "剪辑"]):
        recommendations = [t for t in ai_tools if t["category"] == "video"]
    elif any(word in task_lower for word in ["语音", "声音", "朗读"]):
        recommendations = [t for t in ai_tools if t["category"] == "audio"]
    else:
        recommendations = ai_tools[:5]
    
    return {
        "task": task,
        "recommendations": recommendations[:5],
        "reason": "根据您的任务需求推荐"
    }


# ============== B 站资源 ==============

@app.get("/api/v1/bilibili/videos")
async def get_bilibili_videos(keyword: Optional[str] = None, limit: int = 10):
    """获取 B 站 AI 教程视频"""
    videos = bilibili_videos
    
    if keyword:
        videos = [v for v in videos if keyword.lower() in v["title"].lower() or keyword.lower() in v["description"].lower()]
    
    return {
        "total": len(videos),
        "videos": videos[:limit]
    }


@app.get("/api/v1/bilibili/search")
async def search_bilibili(keyword: str):
    """搜索 B 站视频（模拟）"""
    # 实际应该调用 B 站 API
    results = [v for v in bilibili_videos if keyword in v["title"] or keyword in v["description"]]
    return {
        "keyword": keyword,
        "total": len(results),
        "results": results
    }


# ============== 工作流 API ==============

workflows_db = []

@app.get("/api/v1/workflows")
async def list_workflows():
    """获取工作流列表"""
    return workflows_db or [
        {"id": 1, "name": "每日学习提醒", "description": "每天早上 9 点发送学习提醒", "status": "active", "executions": 15, "lastRun": "2 小时前"},
        {"id": 2, "name": "进度达标通知", "description": "当学习进度超过 50% 时发送通知", "status": "active", "executions": 3, "lastRun": "1 天前"},
        {"id": 3, "name": "周报生成", "description": "每周日生成学习周报", "status": "paused", "executions": 8, "lastRun": "3 天前"}
    ]


@app.post("/api/v1/workflows")
async def create_workflow(workflow: Dict[str, Any]):
    """创建工作流"""
    new_id = len(workflows_db) + 1
    workflow["id"] = new_id
    workflow["status"] = "active"
    workflows_db.append(workflow)
    return {"id": new_id, "status": "created", "message": "工作流创建成功"}


@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: int):
    """获取工作流详情"""
    return {"id": workflow_id, "name": f"工作流{workflow_id}", "nodes": [], "edges": []}


@app.post("/api/v1/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: int, data: Optional[Dict[str, Any]] = None):
    """执行工作流"""
    return {
        "execution_id": f"exec_{random.randint(1, 1000)}",
        "workflow_id": workflow_id,
        "status": "running",
        "started_at": datetime.datetime.utcnow().isoformat(),
        "message": "工作流开始执行"
    }


@app.delete("/api/v1/workflows/{workflow_id}")
async def delete_workflow(workflow_id: int):
    """删除工作流"""
    return {"status": "success", "message": "工作流已删除"}


@app.get("/api/v1/workflows/{workflow_id}/executions")
async def get_workflow_executions(workflow_id: int):
    """获取工作流执行历史"""
    return {
        "workflow_id": workflow_id,
        "executions": [
            {"id": 1, "status": "success", "time": "2 分钟前", "duration": "1.2s"},
            {"id": 2, "status": "success", "time": "1 小时前", "duration": "3.5s"},
            {"id": 3, "status": "error", "time": "3 小时前", "duration": "0.5s"},
        ]
    }


# ============== 原有 API 保持兼容 ==============

@app.get("/api/v1/users/me")
async def get_current_user():
    return {
        "id": 1,
        "username": "demo_user",
        "email": "demo@example.com",
        "full_name": "演示用户",
        "current_level": "beginner",
        "learning_style": "mixed"
    }


@app.post("/api/v1/paths/generate")
async def generate_path(data: Dict[str, Any]):
    target_goal = data.get("targetGoal", "学习机器学习")
    return {
        "id": random.randint(1, 1000),
        "path_name": f"{target_goal}之路",
        "description": f"个性化定制：{target_goal}",
        "total_duration": "12 周",
        "status": "active",
        "progress": 0
    }


@app.get("/api/v1/paths")
async def list_paths():
    return [
        {"id": 1, "path_name": "机器学习入门", "progress": 45, "status": "active"},
        {"id": 2, "path_name": "深度学习进阶", "progress": 20, "status": "active"},
        {"id": 3, "path_name": "LLM 应用开发", "progress": 0, "status": "not_started"}
    ]


@app.post("/api/v1/chat/message")
async def chat_message(data: Dict[str, Any]):
    message = data.get("message", "").lower()
    responses = {
        "你好": "你好！我是你的 AI 导师！😊",
        "机器学习": "机器学习是 AI 的分支，让计算机从数据中学习。",
        "工具": "我们集成了 10+ 个 AI 工具，访问/tools 查看",
        "推荐": "推荐试试 ChatGPT、Claude、GitHub Copilot"
    }
    response = next((v for k, v in responses.items() if k in message), "这是个很好的问题！")
    return {
        "message": response,
        "conversationId": f"conv_{datetime.datetime.utcnow().timestamp()}",
        "suggestions": ["什么是机器学习？", "推荐什么 AI 工具？", "如何开始学习？"],
        "responseTime": random.randint(100, 500)
    }


@app.get("/api/v1/progress/user/{user_id}")
async def get_user_progress(user_id: int):
    return {
        "userId": user_id,
        "overallProgress": 35,
        "studyStreak": 7,
        "totalStudyTime": 42
    }


# ============== Qwen & Coding Plan API ==============

class QwenChatRequest(BaseModel):
    """Qwen 聊天请求"""
    message: str
    system_prompt: Optional[str] = None
    api_key: Optional[str] = None

class CodingPlanRequest(BaseModel):
    """Coding Plan 请求"""
    language: str
    level: str
    duration: str
    goal: str
    api_key: Optional[str] = None

@app.post("/api/v1/ai/qwen/chat")
async def qwen_chat(request: QwenChatRequest):
    """通义千问聊天对话"""
    try:
        qwen = get_qwen_service(request.api_key)
        response = await qwen.chat(request.message, request.system_prompt)
        return {
            "status": "success",
            "message": response,
            "model": "qwen-plus",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Qwen API 错误：{str(e)}",
            "fallback_message": "Qwen 服务暂时不可用，请使用备用 AI 服务。"
        }

@app.post("/api/v1/ai/qwen/generate-path")
async def qwen_generate_path(user_data: Dict[str, Any], api_key: Optional[str] = None):
    """通义千问生成学习路径"""
    try:
        qwen = get_qwen_service(api_key)
        path = await qwen.generate_learning_path(user_data)
        return {
            "status": "success",
            "path": path,
            "model": "qwen-plus"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Qwen API 错误：{str(e)}"
        }

@app.post("/api/v1/ai/qwen/recommend-tools")
async def qwen_recommend_tools(task: str, api_key: Optional[str] = None):
    """通义千问推荐 AI 工具"""
    try:
        qwen = get_qwen_service(api_key)
        tools = await qwen.recommend_tools(task)
        return {
            "status": "success",
            "tools": tools,
            "model": "qwen-plus"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Qwen API 错误：{str(e)}"
        }

@app.post("/api/v1/coding-plan/generate")
async def coding_plan_generate(request: CodingPlanRequest):
    """生成编程学习计划"""
    try:
        coding_plan = get_coding_plan_service(request.api_key)
        plan = await coding_plan.generate_plan(
            request.language,
            request.level,
            request.duration,
            request.goal
        )
        return {
            "status": "success",
            "plan": plan,
            "source": "coding_plan_api"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Coding Plan API 错误：{str(e)}"
        }

@app.get("/api/v1/coding-plan/resources")
async def coding_plan_resources(topic: str, api_key: Optional[str] = None):
    """获取编程学习资源"""
    try:
        coding_plan = get_coding_plan_service(api_key)
        resources = await coding_plan.get_resources(topic)
        return {
            "status": "success",
            "resources": resources,
            "topic": topic
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Coding Plan API 错误：{str(e)}"
        }

@app.post("/api/v1/coding-plan/test")
async def coding_plan_test(api_key: Optional[str] = None):
    """测试 Coding Plan API 连接"""
    coding_plan = get_coding_plan_service(api_key)
    result = await coding_plan.test_connection()
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
