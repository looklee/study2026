# 🎯 Study2026 - AI 学习平台

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![CI/CD](https://github.com/looklee/study2026/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/looklee/study2026/actions/workflows/ci-cd.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-blue.svg)](https://dependabot.com/)
[![GitHub stars](https://img.shields.io/github/stars/looklee/study2026.svg?style=social&label=Star)](https://github.com/looklee/study2026)
[![GitHub issues](https://img.shields.io/github/issues/looklee/study2026.svg)](https://github.com/looklee/study2026/issues)
[![Last Commit](https://img.shields.io/github/last-commit/looklee/study2026.svg)](https://github.com/looklee/study2026/commits/main)

**个性化的 AI 驱动学习平台 | 可视化工作流引擎 | 智能学习路径生成**

[功能特性](#-功能特性) • [快速开始](#🚀-快速开始) • [文档](./docs) • [贡献指南](./CONTRIBUTING.md) • [更新日志](./CHANGELOG.md)

</div>

---

## 📖 项目简介

Study2026 是一个开源的 AI 驱动学习平台，旨在通过人工智能技术为用户提供个性化的学习体验。项目采用现代化的技术栈，支持可视化工作流编排、智能学习路径生成、学习进度追踪等功能。

### ✨ 核心亮点

- 🤖 **AI 驱动** - 基于大语言模型的智能学习路径生成
- 📊 **进度追踪** - 可视化学习进度和成就系统
- 💬 **AI 导师** - 7x24 小时在线答疑
- 🔄 **工作流引擎** - 可视化编排自定义学习流程
- 📚 **知识库** - RAG 检索增强的知识管理
- 🐾 **学习伴侣** - 虚拟宠物陪伴学习成长

---

## 🏗️ 技术架构

### 前端技术栈
| 技术 | 版本 | 说明 |
|------|------|------|
| Next.js | 14 | React 框架（App Router） |
| TypeScript | 5 | 类型安全 |
| TailwindCSS | 3 | 原子化 CSS |
| TanStack Query | 5 | 数据管理 |
| Zustand | 4 | 状态管理 |
| ReactFlow | 11 | 工作流可视化 |

### 后端技术栈
| 技术 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.100+ | Python API 框架 |
| SQLAlchemy | 2 | ORM |
| Pydantic | 2 | 数据验证 |
| Uvicorn | - | ASGI 服务器 |

### 数据库
| 数据库 | 用途 |
|--------|------|
| SQLite | 主数据库（默认） |
| PostgreSQL | 生产环境（可选） |
| Redis | 缓存（可选） |

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Node.js 18+
- npm 或 pnpm

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/study2026.git
cd study2026
```

### 2. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，填入您的 API 密钥
```

### 3. 安装依赖

**后端：**
```bash
cd apps/api
pip install -r requirements.txt
```

**前端：**
```bash
cd apps/web
npm install
```

### 4. 启动服务

**一键启动（推荐）：**
```bash
# Windows
.\start-all.bat

# Linux/Mac
./start-all.sh
```

**手动启动：**

```bash
# 终端 1 - 启动后端
cd apps/api
python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8001 --reload

# 终端 2 - 启动前端
cd apps/web
npm run dev
```

### 5. 访问应用

- **前端首页**: http://localhost:3000
- **工作流编辑器**: http://localhost:3000/workflows
- **后端 API**: http://localhost:8001
- **API 文档**: http://localhost:8001/docs

---

## 📦 功能模块

### 1. 工作流引擎

可视化工作流编排，支持 8 大类 40+ 节点类型：

| 分类 | 节点数 | 示例节点 |
|------|--------|----------|
| 触发器 | 5 | 定时触发、Webhook、进度更新 |
| 动作 | 7 | 发送邮件、生成报告、颁发徽章 |
| 条件 | 4 | 判断条件、数值比较、文本匹配 |
| AI 模型 | 6 | 调用 LLM、文本摘要、代码生成 |
| API 集成 | 4 | HTTP 请求、数据导入/导出 |
| 数据处理 | 6 | 保存/查询/更新数据、数据转换 |
| 学习相关 | 6 | 生成学习路径、推荐资源、测验评估 |
| 通知消息 | 5 | 邮件通知、钉钉通知、企业微信 |

### 2. 学习路径生成

AI 根据用户目标、水平和时间，生成个性化学习路径。

### 3. 学习伴侣

虚拟宠物系统，陪伴学习成长，增加学习趣味性。

### 4. 签到系统

每日签到获取奖励，激励持续学习。

### 5. 知识库

支持文档上传、RAG 检索、智能问答。

---

## 📁 项目结构

```
study2026/
├── apps/
│   ├── api/              # FastAPI 后端
│   │   ├── app/
│   │   │   ├── api/      # API 路由
│   │   │   ├── core/     # 核心配置
│   │   │   ├── models/   # 数据模型
│   │   │   ├── schemas/  # Pydantic 模型
│   │   │   ├── services/ # 业务逻辑
│   │   │   └── main_simple.py
│   │   └── requirements.txt
│   └── web/              # Next.js 前端
│       ├── src/
│       │   ├── app/      # 页面路由
│       │   ├── components/
│       │   ├── contexts/
│       │   └── lib/
│       └── package.json
├── docker/               # Docker 配置
├── docs/                 # 文档
├── scripts/              # 工具脚本
├── .gitignore
├── README.md
├── LICENSE
└── start-all.bat
```

---

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | 数据库连接 URL | `sqlite:///./study2026.db` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `QWEN_API_KEY` | 通义千问 API 密钥 | - |
| `JWT_SECRET_KEY` | JWT 密钥 | - |
| `NEXT_PUBLIC_API_URL` | 后端 API 地址 | `http://localhost:8001` |

### API 密钥配置

支持多种 AI 提供商：

- **通义千问** (推荐国内用户)
- **OpenAI GPT**
- **Anthropic Claude**

在 `.env` 文件中配置对应的 API 密钥即可。

---

## 📚 文档

- [安装指南](./INSTALL.md)
- [快速开始](./QUICKSTART-SIMPLE.md)
- [功能说明](./docs/FEATURES.md)
- [API 文档](http://localhost:8001/docs)
- [贡献指南](./CONTRIBUTING.md)

---

## 🤝 贡献

欢迎贡献代码、文档或建议！

### 贡献方式

1. 🐛 报告 Bug
2. 💡 提出新功能建议
3. 📝 改进文档
4. 🔧 提交代码修复或新功能

### 开发流程

```bash
# 1. Fork 项目
# 2. 创建功能分支
git checkout -b feature/amazing-feature

# 3. 提交更改
git commit -m 'Add amazing feature'

# 4. 推送到分支
git push origin feature/amazing-feature

# 5. 创建 Pull Request
```

详细指南请查看 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 📄 开源许可证

本项目采用 [MIT](./LICENSE) 许可证开放源代码。

---

## 👥 团队

- 创建者：Study2026 Team
- 主要贡献者：[查看贡献者列表](../../graphs/contributors)

---

## 🙏 致谢

感谢以下开源项目：

- [Next.js](https://nextjs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [ReactFlow](https://reactflow.dev/)
- [TailwindCSS](https://tailwindcss.com/)
- [TanStack Query](https://tanstack.com/query)

---

## 📬 联系方式

- 📧 Email: your-email@example.com
- 💬 Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/study2026/issues)

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star！**

[⬆️ 返回顶部](#-study2026---ai-学习平台)

</div>
