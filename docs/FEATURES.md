# 🎯 STUDY2026 功能文档

完全自研的 AI 学习平台，包含 7 个核心模块。

---

## 📱 页面列表

| 页面 | 路由 | 功能 |
|------|------|------|
| 仪表板 | `/dashboard` | 总览学习进度和统计 |
| 学习路径 | `/paths` | 查看和管理学习路径 |
| 路径详情 | `/paths/[id]` | 查看路径详情和进度 |
| 新建路径 | `/paths/new` | AI 生成学习路径 |
| AI 导师 | `/chat` | 与 AI 导师对话 |
| 学习进度 | `/progress` | 可视化学习数据 |
| 内容推荐 | `/recommendations` | 获取学习资源推荐 |
| 知识库 | `/knowledge` | 管理学习文档 |
| 工作流 | `/workflows` | 创建自动化流程 |
| 个人设置 | `/profile` | 管理账户和偏好 |

---

## 🎨 核心功能

### 1. 学习路径系统

#### 功能特点
- ✅ AI 驱动的个性化路径生成
- ✅ 分阶段学习规划
- ✅ 进度追踪和可视化
- ✅ 里程碑和成就系统

#### 使用流程
1. 访问 `/paths/new`
2. 填写学习目标、当前水平、可用时间
3. AI 生成详细学习路径
4. 在路径详情页查看各阶段内容
5. 完成阶段后标记为已完成

#### API 端点
```
POST /api/v1/paths/generate - 生成学习路径
GET  /api/v1/paths          - 获取路径列表
GET  /api/v1/paths/{id}     - 获取路径详情
```

---

### 2. AI 导师对话

#### 功能特点
- ✅ 智能问答
- ✅ 代码示例生成
- ✅ 学习建议
- ✅ 上下文记忆
- ✅ 后续问题推荐

#### 支持主题
- 机器学习概念解释
- 深度学习原理
- Python 编程指导
- 学习资源推荐
- 职业发展规划

#### API 端点
```
POST /api/v1/chat/message - 发送消息
GET  /api/v1/chat/conversation/{id} - 获取对话历史
```

---

### 3. 进度追踪系统

#### 功能特点
- ✅ 总体进度可视化
- ✅ 学习活跃度图表
- ✅ 成就徽章系统
- ✅ 连续学习天数统计
- ✅ 学习活动时间线

#### 统计数据
- 总体完成百分比
- 已完成项目数量
- 学习时长统计
- 每周平均学习时间
- 当前连续学习天数

#### API 端点
```
POST /api/v1/progress/track      - 更新进度
GET  /api/v1/progress/user/{id}  - 获取进度统计
GET  /api/v1/progress/streak/{id} - 获取连续天数
```

---

### 4. 内容推荐引擎

#### 功能特点
- ✅ 多平台资源聚合
- ✅ AI 智能策展
- ✅ 个性化推荐
- ✅ 热门主题追踪

#### 资源类型
- 📚 在线课程（Coursera、edX）
- 📖 技术书籍
- 🎬 视频教程（YouTube）
- 💻 实践项目（Kaggle）
- 📝 技术文章

#### API 端点
```
GET  /api/v1/recommendations        - 获取推荐
GET  /api/v1/recommendations/trending - 热门主题
```

---

### 5. 知识库管理

#### 功能特点
- ✅ 文档上传和分类
- ✅ 标签管理
- ✅ 全文搜索
- ✅ 智能摘要生成

#### 支持的文档类型
- 课程笔记
- 教程文档
- 技术文章
- 参考手册

#### API 端点
```
POST /api/v1/knowledge/upload   - 上传文档
GET  /api/v1/knowledge/documents - 获取文档列表
POST /api/v1/knowledge/query    - 查询知识
```

---

### 6. 工作流自动化

#### 功能特点
- ✅ 可视化工作流编辑
- ✅ 触发器配置
- ✅ 条件分支
- ✅ 定时任务

#### 预置工作流
- 每日学习提醒
- 进度达标通知
- 周报自动生成
- 里程碑庆祝

#### API 端点
```
GET    /api/v1/workflows         - 获取工作流列表
POST   /api/v1/workflows         - 创建工作流
POST   /api/v1/workflows/{id}/execute - 执行工作流
DELETE /api/v1/workflows/{id}    - 删除工作流
```

---

### 7. 用户个人中心

#### 功能特点
- ✅ 账户信息管理
- ✅ 学习偏好设置
- ✅ 通知设置
- ✅ 隐私和安全

#### 可配置项
- 当前水平（初学者/中级/高级）
- 学习风格（理论/实践/混合）
- 时区设置
- 邮件通知开关
- 每日提醒设置

#### API 端点
```
GET  /api/v1/users/me - 获取当前用户
PUT  /api/v1/users/me - 更新用户信息
```

---

## 🏗️ 技术架构

### 前端技术栈
```
Next.js 14 (App Router)
├── React 18
├── TypeScript
├── TailwindCSS
├── TanStack Query
└── Zustand
```

### 后端技术栈
```
FastAPI + Python 3.11
├── SQLAlchemy (ORM)
├── Pydantic (验证)
├── LangChain (AI)
└── Uvicorn (服务器)
```

### 数据库
```
SQLite (开发) / PostgreSQL (生产)
├── 用户表
├── 学习路径表
├── 进度记录表
├── 对话记录表
├── 工作流表
└── 知识文档表
```

---

## 📊 API 完整列表

### 认证
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/v1/users/register | 用户注册 |
| GET | /api/v1/users/me | 获取当前用户 |
| PUT | /api/v1/users/me | 更新用户 |

### 学习路径
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/v1/paths/generate | AI 生成路径 |
| GET | /api/v1/paths | 获取路径列表 |
| GET | /api/v1/paths/{id} | 获取路径详情 |

### 进度追踪
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/v1/progress/track | 更新进度 |
| GET | /api/v1/progress/user/{id} | 获取统计 |
| GET | /api/v1/progress/streak/{id} | 连续天数 |

### AI 对话
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/v1/chat/message | 发送消息 |
| GET | /api/v1/chat/conversation/{id} | 对话历史 |

### 推荐
| 方法 | 端点 | 说明 |
|------|------|------|
| GET | /api/v1/recommendations | 获取推荐 |
| GET | /api/v1/recommendations/trending | 热门主题 |

### 工作流
| 方法 | 端点 | 说明 |
|------|------|------|
| GET | /api/v1/workflows | 获取列表 |
| POST | /api/v1/workflows | 创建工作流 |
| POST | /api/v1/workflows/{id}/execute | 执行 |
| DELETE | /api/v1/workflows/{id} | 删除 |

### 知识库
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/v1/knowledge/upload | 上传文档 |
| GET | /api/v1/knowledge/documents | 文档列表 |
| POST | /api/v1/knowledge/query | 查询 |

---

## 🚀 快速开始

### 启动应用
```bash
# 前端（端口 3000）
cd apps/web
npm run dev

# 后端（端口 8001）
cd apps/api
python -m uvicorn app.main_simple:app --reload
```

### 访问应用
- 前端：http://localhost:3000
- 后端 API: http://localhost:8001
- API 文档：http://localhost:8001/docs

---

## 📝 使用示例

### 1. 生成学习路径
```bash
curl -X POST http://localhost:8001/api/v1/paths/generate \
  -H "Content-Type: application/json" \
  -d '{
    "targetGoal": "掌握机器学习",
    "currentLevel": "beginner",
    "availableHoursPerWeek": 10
  }'
```

### 2. 与 AI 导师对话
```bash
curl -X POST http://localhost:8001/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "什么是机器学习？",
    "userId": 1
  }'
```

### 3. 更新学习进度
```bash
curl -X POST http://localhost:8001/api/v1/progress/track \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "pathId": 1,
    "action": "complete",
    "itemType": "phase",
    "itemId": "phase_1"
  }'
```

---

## 🎯 下一步计划

- [ ] 真实 AI 集成（OpenAI/Claude）
- [ ] 数据库迁移系统
- [ ] 用户认证和授权
- [ ] 文件上传功能
- [ ] 邮件通知系统
- [ ] 移动端适配
- [ ] 暗黑模式
- [ ] 多语言支持

---

**版本**: v1.0.0  
**更新时间**: 2026 年 2 月 27 日
