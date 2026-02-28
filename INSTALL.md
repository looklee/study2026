# 🚀 STUDY2026 自主应用安装指南

完全自研的 AI 学习平台，不依赖 n8n。

---

## 📋 目录

1. [快速开始](#快速开始)
2. [环境要求](#环境要求)
3. [安装步骤](#安装步骤)
4. [配置说明](#配置说明)
5. [运行应用](#运行应用)

---

## 🔧 环境要求

| 软件 | 版本 | 说明 |
|------|------|------|
| Node.js | 18+ | 前端运行环境 |
| Python | 3.11+ | 后端运行环境 |
| pnpm | 8+ | 包管理器（推荐） |
| Docker | 20+ | 可选，用于容器化部署 |

---

## 🚀 快速开始

### 方案 A：本地开发（推荐初次使用）

```bash
# 1. 安装依赖
pnpm install

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 API 密钥

# 3. 启动数据库（使用 Docker）
docker-compose -f docker/docker-compose.yml up -d postgres redis chromadb

# 4. 启动后端
cd apps/api
pip install -r requirements.txt
uvicorn app.main:app --reload

# 5. 启动前端（新终端）
cd apps/web
npm install
npm run dev
```

访问：
- **前端**: http://localhost:3000
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

---

### 方案 B：Docker 一键启动

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 2. 启动所有服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

---

## 📝 配置说明

### 环境变量（.env）

```env
# 数据库配置
DATABASE_URL=postgresql://n8n:n8n@localhost:5432/study2026

# Redis 配置
REDIS_URL=redis://localhost:6379

# ChromaDB 配置
CHROMA_URL=http://localhost:8000

# AI API 密钥（必需 - 至少配置一个）
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# JWT 配置
JWT_SECRET=your-secret-key-change-in-production

# 应用配置
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 🎯 功能测试

### 1. 测试后端 API

```bash
# 健康检查
curl http://localhost:8000/health

# 生成学习路径
curl -X POST http://localhost:8000/api/v1/paths/generate \
  -H "Content-Type: application/json" \
  -d '{
    "currentLevel": "beginner",
    "targetGoal": "掌握机器学习基础",
    "availableHoursPerWeek": 10
  }'
```

### 2. 访问前端

打开浏览器访问 http://localhost:3000

点击"新建学习路径"，填写表单测试 AI 生成功能。

### 3. 测试 AI 对话

访问 http://localhost:3000/chat，输入问题测试 AI 导师。

---

## 🏗️ 项目架构

```
┌─────────────────┐
│   Next.js 14    │  ← 前端 (端口 3000)
│   React 18      │
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐
│   FastAPI       │  ← 后端 (端口 8000)
│   Python 3.11   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│Postgres│ │Redis │ │ChromaDB│ │ OpenAI │
│:5432   │ │:6379 │ │:8000   │ │  API   │
└────────┘ └──────┘ └────────┘ └────────┘
```

---

## 📁 目录结构

```
STUDY2026/
├── apps/
│   ├── api/              # FastAPI 后端
│   │   ├── app/
│   │   │   ├── api/      # API 路由
│   │   │   ├── core/     # 核心配置
│   │   │   ├── models/   # 数据模型
│   │   │   ├── schemas/  # Pydantic 模式
│   │   │   └── services/ # 业务逻辑
│   │   └── requirements.txt
│   │
│   └── web/              # Next.js 前端
│       └── src/
│           ├── app/      # 页面
│           ├── components/
│           ├── lib/
│           └── stores/
│
├── docker/
│   └── docker-compose.yml
│
├── package.json          # 根配置（Turbo）
├── turbo.json            # Turbo 配置
└── .env.example          # 环境变量模板
```

---

## 🔧 常见问题

### 问题 1：Python 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 清除缓存重新安装
pip cache purge
pip install -r requirements.txt
```

### 问题 2：端口被占用

```bash
# 查看端口占用
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000

# 修改 .env 中的端口
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### 问题 3：数据库连接失败

```bash
# 检查 PostgreSQL 是否运行
docker-compose ps

# 重启数据库
docker-compose restart postgres
```

### 问题 4：前端无法连接后端

确保 `.env` 文件中配置了正确的 API 地址：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/paths/generate` | POST | 生成学习路径 |
| `/api/v1/paths` | GET | 获取路径列表 |
| `/api/v1/progress/track` | POST | 追踪进度 |
| `/api/v1/chat/message` | POST | AI 对话 |
| `/api/v1/recommendations` | POST | 获取推荐 |
| `/api/v1/workflows` | POST | 创建工作流 |

完整 API 文档：http://localhost:8000/docs

---

## 🎉 开始使用

1. 访问 http://localhost:3000
2. 点击"新建学习路径"
3. 填写学习目标，AI 自动生成路径
4. 在学习路径页面查看详情
5. 使用 AI 导师解答疑问
6. 在进度页面查看学习统计

---

**祝你学习愉快！** 🚀
