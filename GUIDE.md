# 🎯 STUDY2026 - 完整项目指南

完全自研的 AI 学习平台，集成了 AI 工具聚合、学习资源、工作流自动化等功能。

## 🚀 快速启动

### Windows 用户
```bash
# 双击运行
run.bat
```

### 手动启动
```bash
# 1. 启动后端
cd apps/api
python -m uvicorn app.main_v2:app --reload

# 2. 启动前端
cd apps/web
npm run dev
```

### 访问地址
- **前端**: http://localhost:3000
- **后端 API**: http://localhost:8001
- **API 文档**: http://localhost:8001/docs

---

## 📁 项目结构

```
STUDY2026/
├── apps/
│   ├── api/                    # FastAPI 后端
│   │   ├── app/
│   │   │   ├── main_v2.py      # API 主文件
│   │   │   ├── core/           # 核心配置
│   │   │   ├── models/         # 数据模型
│   │   │   └── services/       # 业务逻辑
│   │   └── requirements.txt    # Python 依赖
│   │
│   └── web/                    # Next.js 前端
│       ├── src/
│       │   ├── app/            # 页面路由
│       │   │   ├── dashboard/  # 仪表板
│       │   │   ├── paths/      # 学习路径
│       │   │   ├── chat/       # AI 对话
│       │   │   ├── progress/   # 进度追踪
│       │   │   ├── tools/      # AI 工具库
│       │   │   ├── resources/  # 学习资源
│       │   │   ├── workflows/  # 工作流
│       │   │   └── integrations/ # API 集成
│       │   ├── components/     # React 组件
│       │   └── lib/            # 工具函数
│       └── package.json        # 前端依赖
│
├── docs/                       # 项目文档
├── docker/                     # Docker 配置
├── .env.example                # 环境变量模板
├── package.json                # 根配置
└── run.bat                     # 启动脚本
```

---

## ✨ 核心功能

### 1. AI 工具库 (12+ 工具)
访问 `/tools` 查看：
- 💬 语言模型：ChatGPT, Claude
- 💻 编程开发：GitHub Copilot, Cursor
- 🎨 图像生成：Midjourney
- 🎬 视频编辑：Runway ML
- 🎵 语音合成：ElevenLabs
- ⚡ 生产力：Notion AI, Gamma, Tome
- 🔍 搜索研究：Perplexity AI

### 2. 学习资源
访问 `/resources` 查看：
- 📺 B 站 AI 教程视频
- 🎓 在线课程（Coursera, edX）
- 📚 热门 UP 主推荐

### 3. 工作流自动化
访问 `/workflows` 使用：
- 🎨 可视化编辑器
- 📦 4 个预置模板
- 🔧 节点配置面板
- 📊 执行历史监控

### 4. 学习路径
访问 `/paths` 使用：
- 🤖 AI 生成学习路径
- 📈 进度可视化
- 🏆 成就系统

### 5. AI 导师
访问 `/chat` 使用：
- 💬 智能问答
- 💡 学习建议
- 📝 代码示例

### 6. API 集成
访问 `/integrations` 配置：
- 🔌 第三方 API 接入
- 🔑 API 密钥管理
- ✅ 连接测试

---

## 🛠️ 技术栈

### 前端
- **Next.js 14** - React 框架
- **TypeScript** - 类型安全
- **TailwindCSS** - 样式
- **TanStack Query** - 数据管理
- **ReactFlow** - 工作流编辑器

### 后端
- **FastAPI** - Python API 框架
- **Pydantic** - 数据验证
- **HTTPX** - HTTP 客户端

---

## 📊 API 端点

### 学习路径
```
POST /api/v1/paths/generate  - 生成学习路径
GET  /api/v1/paths           - 获取路径列表
```

### AI 对话
```
POST /api/v1/chat/message - 发送消息
```

### AI 工具
```
GET  /api/v1/ai-tools           - 获取工具列表
POST /api/v1/ai-tools/suggest   - 推荐工具
```

### 学习资源
```
GET  /api/v1/bilibili/videos    - 获取 B 站视频
GET  /api/v1/recommendations    - 获取推荐
```

### 工作流
```
GET    /api/v1/workflows        - 获取工作流列表
POST   /api/v1/workflows        - 创建工作流
POST   /api/v1/workflows/{id}/execute - 执行工作流
```

### API 集成
```
GET    /api/v1/integrations     - 获取集成列表
POST   /api/v1/integrations/{id}/configure - 配置
POST   /api/v1/integrations/{id}/test - 测试
```

---

## 🔧 配置说明

### 环境变量 (.env)
```env
# AI API 密钥
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-key-here

# 应用配置
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### 配置步骤
1. 复制 `.env.example` 为 `.env`
2. 填入你的 API 密钥（可选）
3. 重启服务

---

## 📝 使用示例

### 1. 生成学习路径
```bash
curl -X POST http://localhost:8001/api/v1/paths/generate \
  -H "Content-Type: application/json" \
  -d '{"targetGoal": "学习机器学习", "currentLevel": "beginner"}'
```

### 2. AI 对话
```bash
curl -X POST http://localhost:8001/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "什么是机器学习？", "userId": 1}'
```

### 3. 获取 AI 工具
```bash
curl http://localhost:8001/api/v1/ai-tools
```

### 4. 执行工作流
```bash
curl -X POST http://localhost:8001/api/v1/workflows/1/execute
```

---

## 🐛 故障排除

### 问题 1: 端口被占用
```bash
# Windows - 查找占用端口的进程
netstat -ano | findstr :3000
netstat -ano | findstr :8001

# 终止进程
taskkill /F /PID <进程 ID>
```

### 问题 2: 前端构建错误
```bash
cd apps/web
rm -rf node_modules .next
npm install
npm run dev
```

### 问题 3: 后端导入错误
```bash
cd apps/api
pip install -r requirements.txt
```

---

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| [功能文档](./docs/FUNCTIONS.md) | 所有功能详细说明 |
| [API 集成](./docs/INTEGRATIONS.md) | 第三方 API 接入指南 |
| [工作流](./docs/WORKFLOWS.md) | 工作流系统文档 |
| [安装指南](./INSTALL.md) | 详细安装步骤 |

---

## 🎯 项目亮点

1. **完全自研** - 不依赖 n8n 等第三方服务
2. **AI 工具聚合** - 12+ 个主流 AI 工具
3. **可视化工作流** - 拖拽式自动化编排
4. **学习资源** - B 站 + 在线课程聚合
5. **API 集成** - 支持第三方 API 接入

---

## 📈 数据统计

| 指标 | 数量 |
|------|------|
| 页面数量 | 14 |
| API 端点 | 35+ |
| AI 工具 | 12 |
| 工作流模板 | 4 |
| 代码文件 | 50+ |

---

**版本**: v2.0.0  
**更新时间**: 2026 年 2 月 27 日
