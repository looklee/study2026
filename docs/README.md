# 📁 STUDY2026 项目结构说明

```
STUDY2026/
│
├── 📄 README.md                          # 项目主文档
├── 📄 .gitignore                         # Git 忽略配置
│
├── 📁 docker/                            # Docker 配置目录
│   ├── docker-compose.yml                # 生产环境编排文件
│   ├── docker-compose.dev.yml            # 开发环境编排文件
│   ├── .env.example                      # 环境变量模板
│   └── init-db.sql                       # 数据库初始化脚本
│
├── 📁 workflows/                         # n8n 工作流目录
│   ├── 01-learning-path-generator.json   # 学习路径生成器
│   ├── 02-content-recommender.json       # 内容推荐引擎
│   ├── 03-progress-tracker.json          # 进度追踪器
│   ├── 04-ai-tutor.json                  # AI 导师
│   └── 05-knowledge-base.json            # 知识库管理
│
├── 📁 docs/                              # 文档目录
│   ├── README.md                         # 文档索引
│   ├── installation.md                   # 安装指南
│   ├── workflows.md                      # 工作流文档
│   ├── api.md                            # API 文档
│   └── QUICKSTART.md                     # 快速入门指南
│
├── 📁 scripts/                           # 脚本目录
│   ├── start.bat                         # Windows 启动脚本
│   └── start.sh                          # Linux/Mac 启动脚本
│
└── 📁 frontend/                          # 前端应用目录（可选）
    ├── dist/                             # 构建输出
    └── nginx.conf                        # Nginx 配置
```

---

## 📂 目录说明

### `/docker` - 容器编排

包含所有 Docker 相关配置文件：

| 文件 | 说明 |
|------|------|
| `docker-compose.yml` | 生产环境配置，包含所有服务 |
| `docker-compose.dev.yml` | 开发环境配置，额外包含 pgAdmin |
| `.env.example` | 环境变量模板，复制后修改使用 |
| `init-db.sql` | PostgreSQL 初始化脚本，自动创建表和视图 |

**启动的服务**:
- `n8n` - 工作流引擎
- `postgres` - 主数据库
- `redis` - 缓存层
- `chroma` - 向量数据库
- `clickhouse` - Chroma 后端存储
- `pgadmin` - 数据库管理工具（仅开发环境）
- `frontend` - 前端应用（可选）

---

### `/workflows` - n8n 工作流

包含 5 个核心工作流定义：

#### 01-learning-path-generator.json
**功能**: 学习路径生成

**节点**:
- Webhook Trigger
- 数据验证与处理（Code）
- AI 路径生成（LangChain LLM）
- 路径数据增强（Code）
- 保存到数据库（PostgreSQL）
- 返回响应（Webhook Response）
- 错误处理

**API**: `POST /webhook/learning-path/generate`

---

#### 02-content-recommender.json
**功能**: 内容推荐引擎

**节点**:
- Webhook Trigger
- 查询构建器（Code）
- GitHub 资源搜索（HTTP Request）
- AI 资源策展（LangChain LLM）
- 结果处理（Code）
- 返回响应
- 定时触发器（Schedule）
- 热门资源更新

**API**: `POST /webhook/content/recommend`

---

#### 03-progress-tracker.json
**功能**: 进度追踪与分析

**节点**:
- Webhook Trigger
- 数据处理（Code）
- 保存进度（PostgreSQL）
- 获取用户进度（PostgreSQL）
- 分析引擎（Code）
- 检查里程碑（If）
- 发送通知（HTTP Request）
- 返回响应
- 定时检查（Schedule）
- 提醒检查（Code）
- 获取不活跃用户（PostgreSQL）
- 发送邮件提醒（HTTP Request）

**API**: `POST /webhook/progress/track`

---

#### 04-ai-tutor.json
**功能**: AI 导师对话系统

**节点**:
- Chat Trigger
- Chat Model（OpenAI）
- Chat Memory（PostgreSQL）
- 代码解释器（Tool）
- 知识库检索（Tool）
- 计算器（Tool）
- 学习路径查询（Tool）
- AI 导师 Agent（LangChain Agent）
- 响应处理（Code）
- 对话日志（Code）
- 保存日志（PostgreSQL）

**API**: `POST /webhook/ai-tutor/chat`

---

#### 05-knowledge-base.json
**功能**: RAG 知识库管理

**节点**:
- Upload Webhook
- 文件处理（Code）
- 文本分割（LangChain Text Splitter）
- 内容分析（LangChain LLM）
- 保存元数据（PostgreSQL）
- Chroma 向量库（LangChain Vector Store）
- 返回响应
- Query Webhook
- 查询处理（Code）
- Query Embeddings（OpenAI）
- 向量检索（LangChain Vector Store Retriever）
- 元数据检索（PostgreSQL）
- 答案生成（LangChain LLM）
- 返回查询结果

**API**: 
- `POST /webhook/knowledge/upload`
- `POST /webhook/knowledge/query`

---

### `/docs` - 文档

| 文件 | 内容 |
|------|------|
| `README.md` | 文档索引 |
| `installation.md` | 详细安装步骤、配置说明、故障排除 |
| `workflows.md` | 每个工作流的详细说明、输入输出示例 |
| `api.md` | 完整的 API 参考文档 |
| `QUICKSTART.md` | 5 分钟快速入门指南 |

---

### `/scripts` - 启动脚本

#### start.bat (Windows)
- 检查 Docker 安装
- 创建环境变量文件
- 提供交互式菜单
- 支持开发/生产环境切换
- 支持服务状态查看、停止、重置

#### start.sh (Linux/Mac)
- 功能与 Windows 版本相同
- Bash 脚本格式

---

## 🔧 配置层次

### 1. 环境变量（`.env`）
最外层配置，包含敏感信息：
- API 密钥
- 数据库密码
- 服务端口

### 2. Docker Compose
服务编排配置：
- 容器定义
- 网络配置
- 卷挂载
- 依赖关系

### 3. 数据库初始化（`init-db.sql`）
数据库结构：
- 表定义
- 索引
- 视图
- 触发器
- 示例数据

### 4. 工作流配置
业务逻辑：
- 节点定义
- 连接关系
- 执行设置
- 标签

---

## 📊 数据流

```
用户请求
   ↓
Webhook Trigger
   ↓
工作流处理
   ↓
┌──────────────────────────────────────┐
│              n8n 引擎                │
│  ┌────────┐  ┌────────┐  ┌────────┐ │
│  │  Code  │  │  LLM   │  │  HTTP  │ │
│  └────────┘  └────────┘  └────────┘ │
└──────────────────────────────────────┘
   ↓         ↓         ↓
PostgreSQL  Chroma  外部 API
   ↓
返回响应
```

---

## 🚀 部署模式

### 开发模式
```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```
- 包含 pgAdmin
- 调试日志开启
- 卷挂载工作流文件

### 生产模式
```bash
docker-compose -f docker/docker-compose.yml up -d
```
- 最小化服务
- 性能优化
- 安全配置

---

## 📈 扩展方向

### 添加新工作流
1. 在 `/workflows` 创建新的 JSON 文件
2. 在 n8n 中导入并测试
3. 更新文档

### 添加新服务
1. 在 `docker-compose.yml` 添加服务定义
2. 配置网络和卷
3. 更新环境变量

### 添加新数据库表
1. 在 `init-db.sql` 添加表定义
2. 创建迁移脚本
3. 更新工作流中的 SQL 查询

---

## 🔐 安全考虑

| 层级 | 措施 |
|------|------|
| 网络 | 内部网络隔离，仅暴露必要端口 |
| 认证 | n8n 基础认证，API Key 验证 |
| 数据 | 敏感信息使用环境变量 |
| 备份 | 定期备份数据卷 |
| 更新 | 定期更新镜像版本 |

---

**这就是 STUDY2026 项目的完整结构！**

每个目录和文件都有其明确的职责，遵循关注点分离原则，便于维护和扩展。
