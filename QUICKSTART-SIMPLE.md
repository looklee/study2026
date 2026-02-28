# 🚀 STUDY2026 简化版快速开始

无需 Docker，3 分钟快速启动！

---

## ⚡ 3 步启动

### 1️⃣ 运行启动脚本

```bash
# 在项目目录双击运行
start.bat
```

或手动执行：

```bash
# 安装 n8n（首次运行）
npm install -g n8n

# 复制环境变量
copy docker\.env.example .env

# 编辑 .env 文件，填入 API 密钥
notepad .env

# 启动 n8n
n8n start
```

### 2️⃣ 访问 n8n

打开浏览器：**http://localhost:5678**

### 3️⃣ 导入工作流

1. 点击 **Workflows** → **Add workflow**
2. 点击右上角 **⋮** → **Import from File**
3. 导入 `workflows/` 中的文件

---

## 📁 简化版工作流说明

由于没有 Docker 中的 Chroma 向量库，**05-knowledge-base.json** 暂时无法使用。

**可用的 4 个工作流**：

| 工作流 | 状态 | 说明 |
|--------|------|------|
| 01-learning-path-generator | ✅ | 学习路径生成 |
| 02-content-recommender | ✅ | 内容推荐 |
| 03-progress-tracker | ⚠️ | 需改为 SQLite |
| 04-ai-tutor | ✅ | AI 导师对话 |
| 05-knowledge-base | ❌ | 需要 Chroma |

---

## 🔧 配置 03-progress-tracker（SQLite）

1. 在 n8n 中打开 `03-Progress-Tracker` 工作流
2. 找到所有 **PostgreSQL** 节点
3. 编辑节点，将凭证改为 **SQLite**
4. SQLite 会自动创建数据库文件

或者暂时不使用这个工作流，先用其他 3 个。

---

## 🎯 立即测试

### 生成学习路径

```bash
curl -X POST http://localhost:5678/webhook/learning-path/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"currentLevel\": \"beginner\", \"targetGoal\": \"掌握机器学习基础\", \"availableHoursPerWeek\": 10}"
```

### 与 AI 导师对话

```bash
curl -X POST http://localhost:5678/webhook/ai-tutor/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"你好，我想学习 AI，从哪里开始？\", \"userId\": \"demo\"}"
```

---

## 🛠️ 常见问题

### 端口被占用
```bash
# 使用其他端口
n8n start --port 5679
```

### 找不到 n8n 命令
```bash
npm install -g n8n --force
```

### API 密钥错误
确保 `.env` 文件中配置了正确的 OpenAI API 密钥。

---

**需要完整功能？请安装 Docker 后使用 Docker 版本！**
