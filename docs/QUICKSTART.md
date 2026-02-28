# 🚀 STUDY2026 快速入门指南

欢迎使用 STUDY2026 AI 学习路径平台！本指南将帮助你在 5 分钟内完成首次配置和使用。

---

## ⚡ 5 分钟快速开始

### 步骤 1：启动服务 (1 分钟)

**Windows 用户**:
```bash
# 双击运行
scripts\start.bat
```

**Mac/Linux 用户**:
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

选择 `1. 开发环境` 启动服务。

### 步骤 2：配置 API 密钥 (2 分钟)

如果是首次运行，系统会提示你配置 `.env` 文件。

编辑 `docker/.env` 文件，填入你的 API 密钥：

```env
# OpenAI API 密钥（必需）
OPENAI_API_KEY=sk-your-actual-openai-api-key

# Anthropic API 密钥（可选）
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key

# GitHub Token（可选，用于资源搜索）
GITHUB_TOKEN=ghp_your-github-token
```

获取 API 密钥：
- [OpenAI](https://platform.openai.com/api-keys)
- [Anthropic](https://console.anthropic.com/)
- [GitHub](https://github.com/settings/tokens)

### 步骤 3：访问 n8n (1 分钟)

打开浏览器访问：http://localhost:5678

默认登录信息：
- 用户名：`admin`
- 密码：`admin`

**⚠️ 首次登录后请立即修改密码！**

### 步骤 4：导入工作流 (1 分钟)

1. 在 n8n 左侧菜单点击 **Workflows**
2. 点击 **Add workflow**
3. 点击右上角 **⋮** → **Import from File**
4. 依次导入 `workflows/` 目录中的 5 个工作流文件：
   - `01-learning-path-generator.json`
   - `02-content-recommender.json`
   - `03-progress-tracker.json`
   - `04-ai-tutor.json`
   - `05-knowledge-base.json`

### 步骤 5：配置凭证 (2 分钟)

在 n8n 中配置以下凭证：

1. 点击左侧 **Credentials**
2. 点击 **Add Credential**
3. 添加以下凭证：

#### PostgreSQL
```
Name: PostgreSQL
Host: postgres
Port: 5432
Database: n8n
User: n8n
Password: 你的密码（在 .env 文件中）
```

#### OpenAI
```
Name: OpenAI
API Key: 你的 OpenAI API 密钥
```

#### Chroma
```
Name: Chroma API
Host: chroma
Port: 8000
```

---

## 🎯 开始使用

### 1️⃣ 生成你的第一个学习路径

**方法 A：通过 Webhook**

```bash
curl -X POST http://localhost:5678/webhook/learning-path/generate \
  -H "Content-Type: application/json" \
  -d '{
    "currentLevel": "beginner",
    "targetGoal": "掌握机器学习基础",
    "availableHoursPerWeek": 10
  }'
```

**方法 B：在 n8n 中手动执行**

1. 打开 `01-Learning-Path-Generator` 工作流
2. 点击右上角 **Execute**
3. 在 Webhook 节点输入测试数据
4. 查看执行结果

### 2️⃣ 与 AI 导师对话

1. 打开 `04-AI-Tutor` 工作流
2. 点击 **Chat** 按钮（如果有 Chat Trigger）
3. 或使用 Webhook：

```bash
curl -X POST http://localhost:5678/webhook/ai-tutor/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好，我想学习机器学习，应该从哪里开始？",
    "userId": "demo_user"
  }'
```

### 3️⃣ 上传知识文档

```bash
curl -X POST http://localhost:5678/webhook/knowledge/upload \
  -F "file=@/path/to/your/document.pdf" \
  -F "category=course-material" \
  -F "tags=[\"machine-learning\", \"notes\"]" \
  -F "userId=demo_user"
```

### 4️⃣ 查询知识

```bash
curl -X POST http://localhost:5678/webhook/knowledge/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "什么是监督学习？",
    "filters": {
      "limit": 5
    }
  }'
```

---

## 📱 常用操作速查

### 查看服务状态

```bash
docker-compose -f docker/docker-compose.dev.yml ps
```

### 查看日志

```bash
docker-compose -f docker/docker-compose.dev.yml logs -f
```

### 重启服务

```bash
docker-compose -f docker/docker-compose.dev.yml restart
```

### 停止服务

```bash
docker-compose -f docker/docker-compose.dev.yml down
```

---

## 🎓 学习路径示例

### 示例 1：机器学习入门

```json
{
  "currentLevel": "beginner",
  "targetGoal": "掌握机器学习基础，能够独立完成简单的 ML 项目",
  "availableHoursPerWeek": 10,
  "preferredLearningStyle": "hands-on",
  "priorExperience": ["Python 编程基础"],
  "deadline": "2026-06-01"
}
```

### 示例 2：深度学习进阶

```json
{
  "currentLevel": "intermediate",
  "targetGoal": "掌握深度学习，理解 CNN、RNN、Transformer 等架构",
  "availableHoursPerWeek": 15,
  "preferredLearningStyle": "mixed",
  "priorExperience": ["机器学习基础", "线性代数", "Python"],
  "deadline": "2026-09-01"
}
```

### 示例 3：LLM 应用开发

```json
{
  "currentLevel": "advanced",
  "targetGoal": "能够开发基于 LLM 的生产级应用",
  "availableHoursPerWeek": 20,
  "preferredLearningStyle": "hands-on",
  "priorExperience": ["深度学习", "Python", "API 开发"],
  "deadline": "2026-05-01"
}
```

---

## 🛠️ 常见问题

### Q1: 服务启动失败

**解决方案**:
```bash
# 查看日志
docker-compose -f docker/docker-compose.dev.yml logs

# 检查端口占用
netstat -ano | findstr :5678

# 重启服务
docker-compose -f docker/docker-compose.dev.yml restart
```

### Q2: AI 响应慢或失败

- 检查 API 密钥是否正确
- 检查网络连接
- 确认 API 配额是否用完

### Q3: 数据库连接失败

```bash
# 检查 PostgreSQL 是否运行
docker-compose -f docker/docker-compose.dev.yml ps postgres

# 重启数据库
docker-compose -f docker/docker-compose.dev.yml restart postgres
```

---

## 📚 下一步

完成快速入门后，你可以：

1. 📖 阅读 [完整文档](./docs/)
2. 🔧 自定义工作流
3. 🎨 创建自己的学习路径
4. 🤝 贡献代码到项目

---

## 🎉 开始你的 AI 学习之旅！

现在你已经完成了所有配置，可以开始使用 STUDY2026 平台了！

祝你学习愉快！🚀

---

**需要帮助？**
- 📖 [安装指南](./installation.md)
- 🔄 [工作流文档](./workflows.md)
- 📡 [API 文档](./api.md)
- 📝 [项目 README](../README.md)
