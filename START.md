# STUDY2026 启动指南

## 快速启动（推荐）

### Windows 一键启动

```bash
# 在项目根目录执行
.\start-all.bat
```

此脚本会自动：
1. 检查并安装依赖
2. 启动后端 API (端口 8001)
3. 等待后端就绪
4. 启动前端 Web (端口 3000)
5. 自动打开浏览器

---

## 手动启动

### 1. 启动后端 API

```bash
cd apps\api
python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8001 --reload
```

**验证后端启动成功：**
- 访问 http://localhost:8001/ 应返回 `{"status":"ok"}`
- API 文档：http://localhost:8001/docs

### 2. 启动前端 Web

```bash
cd apps\web
npm run dev
```

**验证前端启动成功：**
- 访问 http://localhost:3000/

---

## 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 Web | 3000 | Next.js 开发服务器 |
| 后端 API | 8001 | FastAPI 服务器 |
| API 文档 | 8001/docs | Swagger UI |

---

## 常见问题

### 端口被占用

```bash
# 查看占用端口的进程
netstat -ano | findstr :3000
netstat -ano | findstr :8001

# 终止进程（替换 PID）
taskkill /F /PID <进程 ID>
```

### 前端缓存问题

```bash
# 清除 .next 缓存
rmdir /s /q apps\web\.next

# 重新启动前端
cd apps\web
npm run dev
```

### 后端依赖缺失

```bash
cd apps\api
pip install -r requirements.txt
pip install python-multipart
```

### 前端依赖缺失

```bash
cd apps\web
npm install
```

---

## 完整启动检查清单

- [ ] Python 已安装 (3.8+)
- [ ] Node.js 已安装 (18+)
- [ ] 后端依赖已安装 (`pip install -r apps/api/requirements.txt`)
- [ ] 前端依赖已安装 (`cd apps/web && npm install`)
- [ ] 后端 API 可访问 (http://localhost:8001/)
- [ ] 前端 Web 可访问 (http://localhost:3000/)

---

## 工作流节点库

访问 http://localhost:3000/workflows 使用工作流编辑器

**可用节点分类：**
- 触发器 (5 个节点)
- 动作 (7 个节点)
- 条件 (4 个节点)
- AI 模型 (6 个节点)
- API 集成 (4 个节点)
- 数据处理 (6 个节点)
- 学习相关 (6 个节点)
- 通知消息 (5 个节点)
