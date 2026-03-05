# OpenClaw AI助手集成指南

本指南介绍了如何在Study2026项目中使用集成的OpenClaw AI助手功能。

## 架构概览

OpenClaw已集成到Study2026后端API中，通过以下组件提供服务：

- `app/services/openclaw_service.py` - OpenClaw服务适配器
- `app/api/routes/openclaw_routes.py` - OpenClaw API路由
- `app/core/openclaw_init.py` - OpenClaw服务初始化
- `app/services/ai_assistant_service.py` - 高级AI助手服务

## 配置

### 环境变量

在`.env`文件中添加以下配置：

```env
OPENCLAW_API_KEY=your_openclaw_api_key
OPENCLAW_BASE_URL=https://api.openai.com/v1  # 或其他兼容的API端点
```

## API端点

### 基础功能

#### 处理请求
```
POST /api/v1/openclaw/process
Content-Type: application/json

{
  "input_text": "你的请求内容",
  "context": {
    "user_id": "用户ID",
    "session_id": "会话ID"
  }
}
```

#### 执行技能
```
POST /api/v1/openclaw/execute-skill
Content-Type: application/json

{
  "skill_name": "技能名称",
  "params": {
    "参数键": "参数值"
  }
}
```

#### 获取可用技能
```
GET /api/v1/openclaw/skills
```

#### 带记忆的对话
```
POST /api/v1/openclaw/chat
Content-Type: application/json

{
  "message": "你的消息",
  "conversation_id": "会话ID（可选）"
}
```

#### 健康检查
```
GET /api/v1/openclaw/health
```

## Python服务调用

### 使用OpenClaw服务

```python
from app.services.openclaw_service import get_openclaw_service

# 获取服务实例
openclaw_service = get_openclaw_service()

# 处理请求
result = await openclaw_service.process_request(
    user_input="你好，OpenClaw！",
    context={"user_id": "test_user"}
)

# 执行技能
result = await openclaw_service.execute_skill(
    skill_name="web_search",
    params={"query": "Python编程"}
)
```

### 使用AI助手服务

```python
from app.services.ai_assistant_service import (
    process_learning_request,
    execute_educational_skill,
    get_personalized_learning_advice,
    chat_with_ai_tutor
)

# 处理学习请求
result = await process_learning_request(
    user_query="如何学习Python？",
    user_context={"level": "beginner"}
)

# 执行教育技能
result = await execute_educational_skill(
    skill_name="course_recommendation",
    params={"subject": "mathematics", "level": "intermediate"}
)

# 获取个性化学习建议
advice = await get_personalized_learning_advice(
    user_profile={"age": 25, "experience": "beginner"},
    learning_history=[{"course": "Python基础", "score": 85}]
)

# 与AI导师对话
reply = await chat_with_ai_tutor(
    message="我不理解这个概念",
    conversation_context={"topic": "Python函数"}
)
```

## 部署说明

1. 确保环境变量已正确设置
2. 依赖项会自动安装（通过requirements.txt）
3. 服务会在应用启动时自动初始化

## 故障排除

- 如果遇到API密钥错误，请检查`OPENCLAW_API_KEY`环境变量
- 如果服务未启动，请检查日志中的错误信息
- 确保网络可以访问OpenClaw API端点