# 🚀 STUDY2026 简化版安装指南

无需 Docker！使用 npm 直接运行 n8n。

---

## 📋 前置要求

- ✅ Node.js v18+（你已安装 v22.20.0）
- ✅ npm v8+（你已安装 v11.6.2）

---

## 🔧 快速安装（3 步）

### 步骤 1：安装 n8n

```bash
# 全局安装 n8n
npm install -g n8n
```

等待安装完成（约 2-5 分钟）。

### 步骤 2：配置环境变量

创建 `.env` 文件在项目根目录：

```bash
# 复制示例文件
copy docker\.env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```env
# AI API 密钥（必需 - 至少配置一个）
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# n8n 配置
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http

# 基础认证（可选）
N8N_BASIC_AUTH_ACTIVE=false
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin
```

### 步骤 3：启动 n8n

```bash
# 在项目目录中
npm start
```

或者直接使用：

```bash
n8n start
```

---

## 🌐 访问 n8n

打开浏览器访问：**http://localhost:5678**

---

## 📥 导入工作流

1. 在 n8n 界面，点击左侧 **Workflows**
2. 点击 **Add workflow**
3. 点击右上角 **⋮** → **Import from File**
4. 依次导入 `workflows/` 目录中的文件：
   - `01-learning-path-generator.json`
   - `02-content-recommender.json`
   - `03-progress-tracker.json`
   - `04-ai-tutor.json`
   - `05-knowledge-base.json`

---

## ⚙️ 配置凭证

在 n8n 中配置以下凭证：

### 1. OpenAI

1. 点击左侧 **Credentials**
2. 点击 **Add Credential**
3. 选择 **OpenAI API**
4. 填入你的 API Key
5. 保存为 `OpenAI`

### 2. SQLite（用于数据存储）

简化版使用 SQLite，无需额外配置，n8n 会自动创建。

---

## 🎯 测试工作流

### 测试学习路径生成

```bash
curl -X POST http://localhost:5678/webhook/learning-path/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"currentLevel\": \"beginner\", \"targetGoal\": \"学习机器学习\", \"availableHoursPerWeek\": 10}"
```

### 测试 AI 导师

```bash
curl -X POST http://localhost:5678/webhook/ai-tutor/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"你好，我想学习 AI\", \"userId\": \"test\"}"
```

---

## 🛠️ 常用命令

```bash
# 启动 n8n
n8n start

# 启动并开启隧道（用于外部访问）
n8n start --tunnel

# 调试模式
n8n start --debug

# 查看帮助
n8n --help

# 停止 n8n
# 按 Ctrl + C
```

---

## 📝 简化版限制

| 功能 | Docker 版 | 简化版 |
|------|-----------|--------|
| n8n 工作流 | ✅ | ✅ |
| AI 集成 | ✅ | ✅ |
| 数据库 | PostgreSQL | SQLite |
| 向量库 | Chroma | ❌（需额外配置） |
| 容器管理 | ✅ | ❌ |
| 生产部署 | ✅ | ⚠️（需额外配置） |

**说明**：
- 简化版适合**开发测试**和**个人使用**
- 如果需要完整的 RAG 知识库功能，建议使用 Docker 版或单独部署 Chroma

---

## ⚠️ 工作流调整

简化版中，部分工作流需要调整：

### 03-progress-tracker.json
将 PostgreSQL 节点改为 SQLite：

1. 在 n8n 中编辑工作流
2. 点击 PostgreSQL 节点
3. 更改凭证为 SQLite

### 05-knowledge-base.json
向量库功能需要：
- 单独部署 Chroma，或
- 使用 n8n Cloud 的内置向量库

**临时方案**：先跳过这个工作流，使用其他 4 个工作流。

---

## 🔄 更新 n8n

```bash
# 更新到最新版本
npm update -g n8n
```

---

## 📞 故障排除

### 问题 1：端口被占用

**错误**: `EADDRINUSE: address already in use :::5678`

**解决**:
```bash
# 使用其他端口
n8n start --port 5679
```

### 问题 2：找不到 n8n 命令

**解决**:
```bash
# 重新安装
npm install -g n8n --force
```

### 问题 3：工作流导入失败

**解决**:
1. 确保 n8n 是最新版本
2. 手动创建工作流，复制节点配置

---

## 🎉 开始使用

安装完成后，继续阅读 [`docs/QUICKSTART.md`](./docs/QUICKSTART.md) 了解如何使用各个功能！

---

## 📚 更多资源

- [n8n 官方文档](https://docs.n8n.io/)
- [n8n 工作流模板](https://n8n.io/workflows/)
- [本项目文档](./docs/)
