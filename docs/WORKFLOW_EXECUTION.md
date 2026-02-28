# 🔄 工作流执行引擎

可实际运行的工作流执行系统，支持可视化编排和实时执行。

---

## 🎯 功能特点

### 1. 真实执行
- ✅ 节点按顺序执行
- ✅ 支持 AND/OR 逻辑
- ✅ 实时返回执行结果
- ✅ 错误处理和日志

### 2. 节点执行类型
| 类型 | 执行内容 |
|------|----------|
| 触发器 | 激活工作流，接收输入数据 |
| 动作 | 发送邮件/通知（模拟） |
| 条件 | 条件判断（模拟） |
| API | HTTP 请求（模拟） |
| LLM | 调用大模型（模拟） |
| 数据 | 保存数据（模拟） |

### 3. 执行历史
- ✅ 记录每次执行
- ✅ 显示执行状态
- ✅ 记录执行耗时
- ✅ 节点执行详情

---

## 🚀 使用教程

### 1. 创建工作流

**步骤**:
1. 从左侧节点库添加节点
2. 拖拽连接节点
3. 配置节点参数
4. 选择逻辑模式（AND/OR）
5. 点击"运行"按钮

### 2. 查看执行结果

**执行时会显示**:
- 执行状态（running/success/error）
- 开始时间
- 执行的节点数
- 每个节点的执行结果

### 3. 查看执行历史

**执行历史包含**:
- 工作流名称
- 执行状态
- 节点数量
- 执行时间
- 耗时

---

## 📊 执行流程

### AND 逻辑（与）
```
[触发器] → [节点 1] → [节点 2] → [节点 3]
          ↓         ↓         ↓
       执行完成  执行完成  执行完成
```
所有节点按顺序执行，全部成功才返回成功。

### OR 逻辑（或）
```
[触发器] → [节点 1] → 成功即返回
          ↓
       [节点 2] (不执行)
```
第一个节点成功就返回，后续节点不执行。

---

## 🔧 节点执行逻辑

### 触发器节点
```python
{
  "success": True,
  "message": "触发器已激活：定时触发",
  "input_data": {...},
  "triggered_at": "2026-02-27T12:00:00Z"
}
```

### 动作节点
```python
{
  "success": True,
  "message": "邮件已发送：发送邮件",
  "template": "daily_reminder",
  "sent_at": "2026-02-27T12:00:01Z"
}
```

### 条件节点
```python
{
  "success": True,
  "condition_met": True,
  "message": "条件判断：判断进度 (>= 50)",
  "result": True
}
```

### API 节点
```python
{
  "success": True,
  "message": "API 请求已发送：HTTP 请求",
  "method": "GET",
  "endpoint": "/api/data",
  "response": {"status": "ok"}
}
```

### LLM 节点
```python
{
  "success": True,
  "message": "LLM 已调用：调用 LLM",
  "model": "qwen-plus",
  "response": "这是一个模拟的 LLM 响应",
  "tokens_used": 100
}
```

### 数据节点
```python
{
  "success": True,
  "message": "数据已保存：保存数据",
  "table": "learning_paths",
  "operation": "insert",
  "rows_affected": 1
}
```

---

## 📝 API 端点

### 执行工作流
```bash
POST /api/v1/workflows/execute
Content-Type: application/json

{
  "nodes": [...],
  "edges": [...],
  "logic": "AND",
  "input_data": {}
}
```

**响应**:
```json
{
  "status": "success",
  "execution_id": "exec_workflow_xxx",
  "workflow_id": "workflow_123",
  "started_at": "2026-02-27T12:00:00Z",
  "nodes_executed": 4,
  "result": {
    "status": "success",
    "nodes": [...]
  }
}
```

### 获取执行状态
```bash
GET /api/v1/workflows/executions/{execution_id}
```

### 获取执行历史
```bash
GET /api/v1/workflows/{workflow_id}/executions
```

---

## 🎯 执行示例

### 示例 1: 每日学习提醒

**工作流结构**:
```
[定时触发 09:00] → [发送邮件]
```

**执行结果**:
```json
{
  "status": "success",
  "nodes": [
    {
      "node_id": "1",
      "node_type": "trigger",
      "label": "定时触发",
      "status": "success",
      "result": {
        "message": "触发器已激活：定时触发"
      }
    },
    {
      "node_id": "2",
      "node_type": "action",
      "label": "发送邮件",
      "status": "success",
      "result": {
        "message": "邮件已发送：发送邮件"
      }
    }
  ]
}
```

### 示例 2: AI 学习路径生成

**工作流结构**:
```
[Webhook] → [调用 LLM] → [保存路径] → [返回结果]
```

**执行结果**:
```json
{
  "status": "success",
  "nodes_executed": 4,
  "nodes": [
    {
      "node_type": "trigger",
      "label": "Webhook",
      "status": "success"
    },
    {
      "node_type": "llm",
      "label": "调用 LLM",
      "status": "success",
      "result": {
        "model": "qwen-plus",
        "response": "学习路径已生成"
      }
    },
    {
      "node_type": "data",
      "label": "保存路径",
      "status": "success",
      "result": {
        "table": "learning_paths",
        "rows_affected": 1
      }
    },
    {
      "node_type": "action",
      "label": "返回结果",
      "status": "success"
    }
  ]
}
```

---

## ⚙️ 配置说明

### 逻辑模式

**AND (与)**
- 所有节点按顺序执行
- 一个失败则全部失败
- 适合线性流程

**OR (或)**
- 第一个成功就返回
- 后续节点不执行
- 适合并行触发

### 输入数据

执行时可以传入输入数据：
```json
{
  "input_data": {
    "user_id": 1,
    "target_goal": "学习机器学习",
    "timestamp": "2026-02-27T12:00:00Z"
  }
}
```

---

## 🐛 错误处理

### 执行失败
```json
{
  "status": "error",
  "error": "节点执行失败：未知节点类型",
  "nodes": [
    {
      "node_type": "trigger",
      "status": "success"
    },
    {
      "node_type": "unknown",
      "status": "error",
      "error": "未知节点类型"
    }
  ]
}
```

### 节点执行超时
```json
{
  "status": "error",
  "error": "执行超时",
  "nodes": [...]
}
```

---

## 📊 执行统计

### 成功率
- 总执行次数
- 成功次数
- 失败次数
- 成功率百分比

### 性能指标
- 平均执行时间
- 最快执行
- 最慢执行
- 节点平均耗时

---

**访问地址**: http://localhost:3000/workflows  
**API 文档**: http://localhost:8001/docs  
**更新时间**: 2026-02-27
