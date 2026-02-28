# 🤖 Qwen & Coding Plan API 配置指南

## 目录

1. [通义千问 (Qwen) 配置](#通义千问-qwen-配置)
2. [Coding Plan API 配置](#coding-plan-api-配置)
3. [API 使用示例](#api 使用示例)

---

## 通义千问 (Qwen) 配置

### 1. 获取 API 密钥

**步骤**:

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/apiKey)
2. 登录阿里云账号
3. 点击 "API Key 管理"
4. 点击 "创建新的 API Key"
5. 复制生成的 API Key

**免费额度**:
- 新用户赠送 ¥18 体验金
- qwen-plus: ¥0.012/千 tokens
- qwen-turbo: ¥0.008/千 tokens

### 2. 配置到项目

**方法一：环境变量**

编辑 `.env` 文件：
```env
QWEN_API_KEY=sk-your-qwen-api-key-here
```

**方法二：运行时配置**

在 API 集成页面配置：
1. 访问 `/integrations`
2. 找到 "通义千问 (Qwen)"
3. 点击 "配置"
4. 输入 API Key
5. 保存

### 3. 测试连接

```bash
# 测试 API
curl -X POST http://localhost:8001/api/v1/ai/qwen/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好，请介绍一下自己",
    "api_key": "sk-your-qwen-api-key-here"
  }'
```

**响应示例**:
```json
{
  "status": "success",
  "message": "你好！我是通义千问（Qwen），是阿里云研发的大语言模型...",
  "model": "qwen-plus",
  "timestamp": "2026-02-27T10:30:00Z"
}
```

---

## Coding Plan API 配置

### 1. 获取 API 密钥

**步骤**:

1. 访问 [Coding Plan 官网](https://codingplan.example.com)
2. 注册账号
3. 进入 "API 设置"
4. 创建 API Key
5. 复制保存

### 2. 配置到项目

**环境变量**:
```env
CODING_PLAN_API_KEY=your-coding-plan-api-key
```

### 3. 测试连接

```bash
curl -X POST http://localhost:8001/api/v1/coding-plan/test \
  -H "Content-Type: application/json" \
  -d '{"api_key": "your-api-key"}'
```

---

## API 使用示例

### Qwen - 聊天对话

```bash
curl -X POST http://localhost:8001/api/v1/ai/qwen/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "什么是机器学习？",
    "system_prompt": "你是一位专业的 AI 导师"
  }'
```

### Qwen - 生成学习路径

```bash
curl -X POST http://localhost:8001/api/v1/ai/qwen/generate-path \
  -H "Content-Type: application/json" \
  -d '{
    "currentLevel": "beginner",
    "targetGoal": "学习 Python 编程",
    "availableHoursPerWeek": 10,
    "preferredLearningStyle": "hands-on"
  }'
```

**响应示例**:
```json
{
  "status": "success",
  "path": {
    "pathName": "学习 Python 编程之路",
    "description": "个性化定制：学习 Python 编程",
    "totalDuration": "12 周",
    "phases": [
      {
        "phaseNumber": 1,
        "phaseName": "基础准备",
        "duration": "2 周",
        "objectives": ["掌握基础概念", "熟悉工具和环境"],
        "topics": ["Python 语法", "环境搭建", "Hello World"]
      }
    ]
  }
}
```

### Qwen - 推荐 AI 工具

```bash
curl -X POST "http://localhost:8001/api/v1/ai/qwen/recommend-tools?task=我想写一篇文章"
```

### Coding Plan - 生成编程计划

```bash
curl -X POST http://localhost:8001/api/v1/coding-plan/generate \
  -H "Content-Type: application/json" \
  -d '{
    "language": "Python",
    "level": "beginner",
    "duration": "12 weeks",
    "goal": "Web 开发"
  }'
```

**响应示例**:
```json
{
  "status": "success",
  "plan": {
    "plan_id": "plan_python_beginner",
    "language": "Python",
    "level": "beginner",
    "duration": "12 weeks",
    "goal": "Web 开发",
    "phases": [
      {
        "phase": 1,
        "name": "Python 基础",
        "duration": "2 周",
        "topics": [
          "Python 语法基础",
          "变量和数据类型",
          "控制流（条件/循环）",
          "函数和模块"
        ],
        "project": "编写一个简单的计算器"
      }
    ]
  }
}
```

### Coding Plan - 获取学习资源

```bash
curl "http://localhost:8001/api/v1/coding-plan/resources?topic=Python"
```

---

## 前端集成

### React Hook 示例

```typescript
// 使用 Qwen 聊天
const qwenChat = async (message: string) => {
  const response = await fetch('/api/v1/ai/qwen/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      system_prompt: '你是一位专业的 AI 导师'
    })
  })
  const data = await response.json()
  return data.message
}

// 生成学习路径
const generatePath = async (userData: any) => {
  const response = await fetch('/api/v1/ai/qwen/generate-path', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  })
  const data = await response.json()
  return data.path
}
```

---

## 故障排除

### 问题 1: API Key 无效

**解决**: 
- 检查 API Key 是否正确复制
- 确认账户余额充足
- 检查 API Key 是否过期

### 问题 2: 连接超时

**解决**:
- 检查网络连接
- 增加超时时间
- 使用国内服务器

### 问题 3: 额度不足

**解决**:
- 访问控制台充值
- 申请免费试用
- 使用本地模型替代

---

## 相关资源

- [Qwen 官方文档](https://help.aliyun.com/zh/dashscope/)
- [Qwen GitHub](https://github.com/QwenLM)
- [DashScope 控制台](https://dashscope.console.aliyun.com/)

---

**配置完成后，访问 `/integrations` 页面测试连接！**
