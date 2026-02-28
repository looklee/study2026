# 📖 STUDY2026 安装指南

本指南将帮助你快速部署和配置 STUDY2026 AI 学习路径平台。

## 📋 目录

1. [前置要求](#前置要求)
2. [快速开始](#快速开始)
3. [配置说明](#配置说明)
4. [验证安装](#验证安装)
5. [故障排除](#故障排除)

---

## 🔧 前置要求

### 必需软件

| 软件 | 版本 | 说明 |
|------|------|------|
| Docker | 20.10+ | 容器运行时 |
| Docker Compose | 2.0+ | 容器编排 |
| Git | 2.30+ | 版本控制 |

### API 密钥（可选但推荐）

| 服务 | 用途 | 获取链接 |
|------|------|----------|
| OpenAI | LLM 模型、Embeddings | https://platform.openai.com/api-keys |
| Anthropic | Claude 模型 | https://console.anthropic.com/ |
| GitHub | GitHub API 访问 | https://github.com/settings/tokens |

---

## 🚀 快速开始

### 步骤 1：克隆项目

```bash
cd C:\Users\Administrator\Documents\TRAEproject
git clone <repository-url> STUDY2026
cd STUDY2026
```

### 步骤 2：配置环境变量

```bash
# Windows PowerShell
Copy-Item docker\.env.example docker\.env

# 或者手动复制
# 编辑 docker\.env 文件，填入你的 API 密钥
```

编辑 `docker\.env` 文件：

```env
# n8n 配置
N8N_HOST=http://localhost
N8N_PORT=5678

# 数据库配置
POSTGRES_USER=n8n
POSTGRES_PASSWORD=你的安全密码
POSTGRES_DB=n8n

# AI API 密钥
OPENAI_API_KEY=sk-your-actual-openai-api-key
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key

# GitHub Token（用于资源搜索）
GITHUB_TOKEN=ghp_your-github-token
```

### 步骤 3：启动服务

#### 开发环境（推荐初次使用）

```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```

#### 生产环境

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### 步骤 4：检查服务状态

```bash
docker-compose -f docker/docker-compose.dev.yml ps
```

所有服务应显示 `Up` 状态。

---

## 🔐 配置说明

### n8n 配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `N8N_HOST` | http://localhost | n8n 访问地址 |
| `N8N_PORT` | 5678 | n8n 端口 |
| `N8N_BASIC_AUTH_ACTIVE` | false | 是否启用基础认证 |
| `N8N_BASIC_AUTH_USER` | admin | 管理员用户名 |
| `N8N_BASIC_AUTH_PASSWORD` | admin | 管理员密码 |

### 数据库配置

| 服务 | 端口 | 访问地址 |
|------|------|----------|
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |
| Chroma | 8000 | localhost:8000 |
| pgAdmin | 5050 | localhost:5050 |

### AI 模型配置

支持的模型提供商：

1. **OpenAI**
   - GPT-4o（推荐）
   - GPT-3.5-turbo
   - text-embedding-3-small

2. **Anthropic**
   - Claude 3.5 Sonnet
   - Claude 3 Opus

3. **本地模型**（通过 Ollama）
   - llama2
   - mistral
   - 其他兼容模型

---

## ✅ 验证安装

### 1. 访问 n8n 界面

打开浏览器访问：http://localhost:5678

如果启用了认证，使用配置的用户名密码登录。

### 2. 导入工作流

1. 在 n8n 界面，点击左侧菜单的 **Workflows**
2. 点击 **Add workflow**
3. 点击右上角的 **⋮** 菜单，选择 **Import from File**
4. 选择 `workflows/` 目录中的工作流文件

### 3. 配置凭证

在 n8n 中配置以下凭证：

#### PostgreSQL 凭证
```
Host: postgres
Port: 5432
Database: n8n
User: n8n
Password: 你的密码
```

#### OpenAI 凭证
```
API Key: 你的 OpenAI API 密钥
```

#### Chroma 凭证
```
Host: chroma
Port: 8000
```

### 4. 测试工作流

#### 测试学习路径生成

```bash
curl -X POST http://localhost:5678/webhook/learning-path/generate \
  -H "Content-Type: application/json" \
  -d '{
    "currentLevel": "beginner",
    "targetGoal": "掌握机器学习基础",
    "availableHoursPerWeek": 10,
    "preferredLearningStyle": "hands-on"
  }'
```

#### 测试 AI 导师

访问：http://localhost:5678/chat/ai-tutor

---

## 🐛 故障排除

### 常见问题

#### 1. 容器无法启动

```bash
# 查看日志
docker-compose -f docker/docker-compose.dev.yml logs

# 重启服务
docker-compose -f docker/docker-compose.dev.yml restart
```

#### 2. 数据库连接失败

```bash
# 检查 PostgreSQL 是否运行
docker-compose -f docker/docker-compose.dev.yml ps postgres

# 查看数据库日志
docker-compose -f docker/docker-compose.dev.yml logs postgres
```

#### 3. API 密钥错误

确保在 `.env` 文件中正确配置了 API 密钥，没有多余的空格或引号。

#### 4. 端口冲突

如果端口被占用，修改 `.env` 文件中的端口配置：

```env
N8N_PORT=5679  # 改为其他可用端口
```

### 重置环境

```bash
# 停止所有服务
docker-compose -f docker/docker-compose.dev.yml down

# 删除数据卷（⚠️ 会删除所有数据）
docker-compose -f docker/docker-compose.dev.yml down -v

# 重新启动
docker-compose -f docker/docker-compose.dev.yml up -d
```

---

## 📱 访问地址汇总

| 服务 | 地址 | 说明 |
|------|------|------|
| n8n | http://localhost:5678 | 工作流编辑器 |
| pgAdmin | http://localhost:5050 | 数据库管理 |
| Chroma | http://localhost:8000 | 向量数据库 API |
| PostgreSQL | localhost:5432 | 数据库连接 |
| Redis | localhost:6379 | 缓存服务 |

---

## 🔄 更新项目

```bash
# 拉取最新代码
git pull origin main

# 重启服务
docker-compose -f docker/docker-compose.dev.yml up -d --force-recreate
```

---

## 📞 获取帮助

- 📖 [官方文档](./docs/)
- 🐛 [提交 Issue](https://github.com/your-username/STUDY2026/issues)
- 💬 [讨论区](https://github.com/your-username/STUDY2026/discussions)

---

**安装完成后，请继续阅读 [工作流文档](./docs/workflows.md) 了解如何使用各个工作流。**
