# 📡 API 文档

本文档介绍 STUDY2026 项目提供的所有 API 端点。

---

## 📋 目录

1. [认证](#认证)
2. [学习路径 API](#学习路径-api)
3. [内容推荐 API](#内容推荐-api)
4. [进度追踪 API](#进度追踪-api)
5. [AI 导师 API](#ai 导师-api)
6. [知识库 API](#知识库-api)

---

## 🔐 认证

### API Key 认证

在请求头中添加 API Key：

```http
Authorization: Bearer YOUR_API_KEY
```

### 会话认证

使用 n8n 内置的用户认证系统。

---

## 🎯 学习路径 API

### 生成学习路径

**端点**: `POST /webhook/learning-path/generate`

**请求示例**:

```bash
curl -X POST http://localhost:5678/webhook/learning-path/generate \
  -H "Content-Type: application/json" \
  -d '{
    "currentLevel": "beginner",
    "targetGoal": "掌握机器学习基础",
    "availableHoursPerWeek": 10,
    "preferredLearningStyle": "hands-on",
    "priorExperience": ["Python 基础"],
    "deadline": "2026-12-31",
    "budget": "free"
  }'
```

**响应示例**:

```json
{
  "status": "success",
  "learningPath": {
    "pathName": "机器学习入门之路",
    "description": "从零开始掌握机器学习基础",
    "totalDuration": "12 周",
    "phases": [
      {
        "phaseNumber": 1,
        "phaseName": "基础准备",
        "duration": "3 周",
        "objectives": ["理解机器学习基本概念", "掌握 Python 编程基础"],
        "topics": ["什么是机器学习", "Python 基础", "NumPy 和 Pandas"],
        "resources": [
          {
            "type": "video",
            "title": "机器学习简介",
            "url": "https://youtube.com/...",
            "estimatedHours": 2
          }
        ],
        "milestone": "完成第一个线性回归项目",
        "assessment": "小测验 + 代码审查"
      }
    ],
    "weeklySchedule": {
      "monday": "理论学习 2 小时",
      "wednesday": "代码练习 2 小时",
      "weekend": "项目实践 4 小时"
    },
    "tips": ["每天坚持学习", "多做实践项目"]
  },
  "metadata": {
    "generatedAt": "2026-02-27T10:00:00Z",
    "userId": "anonymous",
    "pathVersion": "1.0",
    "aiModel": "gpt-4o"
  }
}
```

**错误响应**:

```json
{
  "status": "error",
  "error": {
    "message": "缺少必需字段：targetGoal",
    "timestamp": "2026-02-27T10:00:00Z",
    "suggestion": "请检查输入数据格式，确保包含所有必需字段"
  }
}
```

---

## 📚 内容推荐 API

### 获取推荐内容

**端点**: `POST /webhook/content/recommend`

**请求示例**:

```bash
curl -X POST http://localhost:5678/webhook/content/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "topics": ["machine-learning", "python", "deep-learning"],
    "languages": ["Python"],
    "minStars": 100,
    "level": "beginner",
    "pricePreference": "free"
  }'
```

**响应示例**:

```json
{
  "status": "success",
  "recommendations": [
    {
      "id": "rec_1234567890_0",
      "title": "Machine Learning Course by Andrew Ng",
      "type": "course",
      "url": "https://www.coursera.org/learn/machine-learning",
      "description": "史上最受欢迎的机器学习课程",
      "difficulty": "beginner",
      "estimatedHours": 20,
      "rating": 4.9,
      "reason": "课程内容系统全面，适合初学者入门",
      "tags": ["machine-learning", "coursera", "andrew-ng"],
      "prerequisites": ["基础线性代数", "Python 编程基础"],
      "metadata": {
        "recommendedAt": "2026-02-27T10:00:00Z",
        "recommendationId": "rec_1234567890",
        "aiModel": "gpt-4o"
      },
      "tracking": {
        "viewed": false,
        "saved": false,
        "completed": false
      }
    }
  ],
  "learningPath": "建议按以下顺序学习：1. Python 基础 → 2. 数学复习 → 3. 机器学习理论 → 4. 实战项目",
  "tips": "建议每天学习 1-2 小时，周末进行项目实践",
  "totalResults": 15,
  "generatedAt": "2026-02-27T10:00:00Z"
}
```

---

## 📊 进度追踪 API

### 更新学习进度

**端点**: `POST /webhook/progress/track`

**请求示例**:

```bash
curl -X POST http://localhost:5678/webhook/progress/track \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "pathId": "path-uuid-123",
    "action": "complete",
    "itemType": "topic",
    "itemId": "topic-001",
    "metadata": {
      "timeSpent": 45,
      "notes": "理解得很好，掌握了基本概念"
    }
  }'
```

**响应示例**:

```json
{
  "status": "success",
  "progress": {
    "overall": 45,
    "completedItems": 18,
    "totalItems": 40,
    "byType": {
      "topic": {"total": 20, "completed": 10},
      "resource": {"total": 20, "completed": 8}
    }
  },
  "statistics": {
    "startDate": "2026-01-01T00:00:00Z",
    "totalDays": 30,
    "averagePerWeek": 5,
    "estimatedCompletionDate": "2026-04-01T00:00:00Z",
    "remainingDays": 35
  },
  "achievements": [
    {"id": "first_step", "name": "第一步", "unlocked": true},
    {"id": "quarter_way", "name": "四分之一", "unlocked": true},
    {"id": "halfway", "name": "半途", "unlocked": false},
    {"id": "almost_there", "name": "指日可待", "unlocked": false},
    {"id": "champion", "name": "冠军", "unlocked": false}
  ],
  "motivation": "💪 不错的开始，继续保持！",
  "streak": 7
}
```

### 获取学习进度

**端点**: `GET /api/progress/:userId`

**响应示例**:

```json
{
  "userId": "user123",
  "activePaths": 2,
  "completedPaths": 1,
  "totalStudyTime": 120,
  "currentStreak": 7,
  "longestStreak": 14,
  "lastStudyDate": "2026-02-26"
}
```

---

## 🤖 AI 导师 API

### 发送消息

**端点**: `POST /webhook/ai-tutor/chat`

**请求示例**:

```bash
curl -X POST http://localhost:5678/webhook/ai-tutor/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "什么是梯度下降？请用简单易懂的方式解释。",
    "userId": "user123",
    "conversationId": "conv_123"
  }'
```

**响应示例**:

```json
{
  "message": "**梯度下降**是一种优化算法，用于找到函数的最小值。\n\n## 通俗解释\n\n想象你在山上，想要找到最低点。但是天很黑，你看不清整条路。这时你会怎么做？\n\n1. **感受脚下**：用手或脚感受哪个方向最陡\n2. **往下走一步**：沿着最陡的方向走一小步\n3. **重复**：继续感受，继续走\n\n这就是梯度下降的核心思想！\n\n## 数学原理\n\n```\nθ = θ - α * ∇J(θ)\n```\n\n- θ：模型参数\n- α：学习率（步长）\n- ∇J(θ)：梯度（最陡的方向）\n\n## 代码示例\n\n```python\ndef gradient_descent(X, y, lr=0.01, iterations=1000):\n    m, n = X.shape\n    theta = np.zeros(n)\n    \n    for i in range(iterations):\n        gradient = (1/m) * X.T.dot(X.dot(theta) - y)\n        theta = theta - lr * gradient\n    \n    return theta\n```",
  "metadata": {
    "timestamp": "2026-02-27T10:30:00Z",
    "conversationId": "conv_1234567890",
    "userId": "user123",
    "responseTime": 1523,
    "analysis": {
      "topics": ["概念解释", "代码示例"],
      "mainTopic": "概念解释",
      "sentiment": "neutral",
      "complexity": "medium"
    }
  },
  "suggestions": [
    "能举个具体的例子吗？",
    "梯度下降有什么变体？",
    "如何选择合适的学习率？"
  ],
  "resources": []
}
```

### 对话历史

**端点**: `GET /api/conversations/:userId`

**响应示例**:

```json
{
  "conversations": [
    {
      "conversationId": "conv_123",
      "startTime": "2026-02-27T10:00:00Z",
      "endTime": "2026-02-27T10:30:00Z",
      "messageCount": 5,
      "topics": ["梯度下降", "优化算法"]
    }
  ]
}
```

---

## 📖 知识库 API

### 上传文档

**端点**: `POST /webhook/knowledge/upload`

**请求**: `multipart/form-data`

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 要上传的文件 |
| category | String | 否 | 分类，默认 general |
| tags | Array | 否 | 标签列表 |
| userId | String | 是 | 用户 ID |

**响应示例**:

```json
{
  "status": "success",
  "message": "知识文档处理完成",
  "document": {
    "fileName": "机器学习笔记.pdf",
    "summary": "本文档详细介绍了机器学习的基础概念，包括监督学习、非监督学习、常见算法等。",
    "keyPoints": [
      "什么是机器学习",
      "监督学习与非监督学习的区别",
      "常见算法分类"
    ],
    "keywords": ["机器学习", "AI", "算法", "深度学习"],
    "difficulty": "beginner",
    "vectorStored": true,
    "processedAt": "2026-02-27T10:00:00Z"
  }
}
```

### 查询知识

**端点**: `POST /webhook/knowledge/query`

**请求示例**:

```bash
curl -X POST http://localhost:5678/webhook/knowledge/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "什么是过拟合？如何避免？",
    "filters": {
      "category": "course-material",
      "difficulty": "beginner",
      "limit": 10
    }
  }'
```

**响应示例**:

```json
{
  "status": "success",
  "query": "什么是过拟合？如何避免？",
  "answer": "**过拟合**（Overfitting）是指模型在训练集上表现很好，但在新数据（测试集）上表现不佳的现象。\n\n## 原因\n\n1. 模型过于复杂\n2. 训练数据太少\n3. 训练时间太长\n\n## 避免方法\n\n### 1. 增加训练数据\n更多的数据可以帮助模型更好地泛化。\n\n### 2. 正则化\n- L1 正则化（Lasso）\n- L2 正则化（Ridge）\n\n### 3. 早停法（Early Stopping）\n在验证集性能开始下降时停止训练。\n\n### 4. Dropout\n在神经网络中随机丢弃部分神经元。\n\n### 5. 简化模型\n减少参数数量，降低模型复杂度。\n\n## 代码示例\n\n```python\n# L2 正则化\nfrom sklearn.linear_model import Ridge\nmodel = Ridge(alpha=1.0)\nmodel.fit(X_train, y_train)\n\n# Dropout (Keras)\nfrom tensorflow.keras import layers\nmodel.add(layers.Dropout(0.5))\n```",
  "sources": [
    {
      "fileName": "机器学习笔记.pdf",
      "summary": "机器学习基础概念...",
      "relevance": "high"
    },
    {
      "fileName": "深度学习实战.pdf",
      "summary": "神经网络优化技巧...",
      "relevance": "medium"
    }
  ],
  "timestamp": "2026-02-27T10:35:00Z"
}
```

---

## 📝 错误码说明

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |
| 503 | 服务暂时不可用 |

---

## 🔄 限流说明

| 端点类型 | 限制 |
|----------|------|
| AI 相关 API | 10 次/分钟 |
| 数据查询 API | 60 次/分钟 |
| 文件上传 API | 5 次/分钟 |

---

## 📞 支持

如有问题，请查阅：
- [安装指南](./installation.md)
- [工作流文档](./workflows.md)
- [项目 README](../README.md)
