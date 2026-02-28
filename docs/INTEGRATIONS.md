# 🔌 第三方 API 集成指南

Study2026 支持接入各种第三方 API，包括 AI 服务、学习资源平台等。

---

## 📋 目录

1. [API 集成架构](#api-集成架构)
2. [Coding Plan API 接入](#coding-plan-api-接入)
3. [B 站资源接入](#b 站资源接入)
4. [自定义 API 接入](#自定义 api 接入)

---

## 🏗️ API 集成架构

### 架构图

```
┌─────────────────┐
│   Study2026     │
│     前端        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Study2026     │
│     后端        │
│   (FastAPI)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Coding  │ │GitHub  │ │OpenAI  │ │ Bilibili│
│ Plan   │ │ API    │ │ API    │ │ API    │
└────────┘ └────────┘ └────────┘ └────────┘
```

### 集成方式

1. **代理模式** - 通过后端代理请求，隐藏 API 密钥
2. **直连模式** - 前端直接调用公开 API
3. **混合模式** - 敏感操作走后端，公开数据前端获取

---

## 📚 Coding Plan API 接入

### 1. 获取 API 密钥

访问 [Coding Plan 官网](https://codingplan.example.com) 注册并获取 API Key。

### 2. 配置 API

在 Study2026 中：

1. 访问 `/integrations` 页面
2. 找到 "Coding Plan API"
3. 点击 "配置"
4. 输入 API Key
5. 保存

### 3. API 使用示例

#### 生成学习计划

```javascript
// 前端调用示例
const response = await fetch('/api/v1/integrations/coding_plan/proxy/plans/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    language: 'Python',
    level: 'beginner',
    duration: '12 weeks',
    goal: 'Web 开发'
  })
})

const plan = await response.json()
```

#### 后端代理实现

```python
# apps/api/app/integrations/coding_plan.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter()

CODING_PLAN_BASE_URL = "https://api.codingplan.example.com"

class PlanRequest(BaseModel):
    language: str
    level: str
    duration: str
    goal: str

@router.post("/plans/generate")
async def generate_plan(request: PlanRequest):
    """生成编程学习计划"""
    api_key = get_api_key("coding_plan")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CODING_PLAN_BASE_URL}/plans/generate",
            headers={"Authorization": f"Bearer {api_key}"},
            json=request.dict()
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="请求失败")
        
        return response.json()
```

### 4. 响应格式

```json
{
  "plan_id": "plan_123",
  "language": "Python",
  "level": "beginner",
  "duration": "12 weeks",
  "phases": [
    {
      "phase": 1,
      "name": "基础语法",
      "duration": "2 weeks",
      "topics": ["变量", "数据类型", "控制流", "函数"]
    },
    {
      "phase": 2,
      "name": "Web 框架",
      "duration": "4 weeks",
      "topics": ["Flask", "Django", "REST API"]
    }
  ],
  "resources": [
    {
      "title": "Python 官方教程",
      "url": "https://docs.python.org/3/tutorial/",
      "type": "documentation"
    }
  ]
}
```

---

## 📺 B 站资源接入

### 1. B 站 API 说明

B 站开放平台：https://open.bilibili.com/

### 2. 获取视频列表

```python
# 调用 B 站 API 获取 AI 教程视频
async def get_bilibili_ai_videos(keyword: str = "AI 教程"):
    url = "https://api.bilibili.com/x/web-interface/search/type"
    params = {
        "search_type": "video",
        "keyword": keyword,
        "page": 1,
        "pagesize": 20
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        
        videos = []
        for result in data["data"]["result"]:
            videos.append({
                "id": result["bvid"],
                "title": result["title"],
                "author": result["author"],
                "url": f"https://www.bilibili.com/video/{result['bvid']}",
                "cover": result["pic"],
                "duration": result["duration"],
                "views": result["play"],
                "pubdate": result["pubdate"],
                "description": result["description"]
            })
        
        return videos
```

### 3. 热门 AI UP 主

| UP 主 | 专区 | 订阅 |
|------|------|------|
| 吴恩达 AI 学习社 | 机器学习 | 120w+ |
| 深度学习学院 | 深度学习 | 85w+ |
| NLP 讲堂 | 自然语言处理 | 62w+ |
| AI 实战派 | 大模型 | 98w+ |

---

## 🌐 自定义 API 接入

### 1. 创建集成配置

在 `api_integrations` 字典中添加：

```python
api_integrations = {
    # ... 现有集成
    "my_custom_api": {
        "id": "my_custom_api",
        "name": "我的自定义 API",
        "description": "自定义服务描述",
        "base_url": "https://api.example.com",
        "api_key": None,
        "status": "pending",
        "category": "custom",
        "endpoints": [
            {"method": "GET", "path": "/data", "description": "获取数据"},
            {"method": "POST", "path": "/process", "description": "处理数据"}
        ]
    }
}
```

### 2. 添加 API 路由

```python
@app.get("/api/v1/integrations/my_custom_api/data")
async def get_custom_data():
    """获取自定义数据"""
    integration = api_integrations["my_custom_api"]
    
    if not integration.get("api_key"):
        raise HTTPException(status_code=400, detail="请先配置 API 密钥")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{integration['base_url']}/data",
            headers={"Authorization": f"Bearer {integration['api_key']}"}
        )
        return response.json()
```

### 3. 前端调用

```javascript
// 在 React 组件中
const { data } = useQuery({
  queryKey: ['custom-data'],
  queryFn: async () => {
    const response = await fetch('/api/v1/integrations/my_custom_api/data')
    return response.json()
  }
})
```

---

## 🔐 安全最佳实践

### 1. API 密钥管理

```python
# 使用环境变量存储密钥
import os
API_KEY = os.getenv("CODING_PLAN_API_KEY")

# 或使用加密存储
from cryptography.fernet import Fernet
cipher = Fernet(generate_key())
encrypted_key = cipher.encrypt(api_key.encode())
```

### 2. 请求限流

```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.get("/api/v1/integrations/{id}/proxy/{path:path}", 
         dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def proxy_request(...):
    ...
```

### 3. 错误处理

```python
try:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()
except httpx.TimeoutException:
    raise HTTPException(status_code=504, detail="请求超时")
except httpx.ConnectError:
    raise HTTPException(status_code=503, detail="服务不可用")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"请求失败：{str(e)}")
```

---

## 📊 已支持的 API

| API | 类别 | 状态 | 文档 |
|-----|------|------|------|
| Coding Plan | 教育 | ✅ 支持 | [文档](#coding-plan-api-接入) |
| GitHub | 开发 | ✅ 支持 | https://docs.github.com/en/rest |
| OpenAI | AI | ✅ 支持 | https://platform.openai.com/docs |
| Anthropic | AI | ✅ 支持 | https://docs.anthropic.com |
| Hugging Face | AI | 🔄 计划中 | https://huggingface.co/docs |
| Replicate | AI | 🔄 计划中 | https://replicate.com/docs |
| Bilibili | 视频 | ✅ 支持 | https://open.bilibili.com |

---

## 🛠️ 故障排除

### 问题 1: API 密钥无效

**解决**: 检查密钥是否正确，确认账户状态正常

### 问题 2: 跨域错误

**解决**: 确保后端配置了正确的 CORS 设置

### 问题 3: 请求超时

**解决**: 增加超时时间或实现重试机制

```python
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url)
```

---

**需要集成新的 API？请查看我们的贡献指南！**
