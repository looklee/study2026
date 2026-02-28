# 🔑 API 密钥真实配置指南

## ✅ 功能说明

现在 API 集成页面是**真实可配置**的，并且 AI 导师会**真正使用**你配置的 API 进行对话。

---

## 🚀 快速开始

### 1. 获取 API 密钥（三选一）

#### 推荐：通义千问 (Qwen)
**获取链接**: https://dashscope.console.aliyun.com/apiKey

1. 登录阿里云账号
2. 点击 "API Key 管理"
3. 创建新的 API Key
4. 复制保存（格式：`sk-xxxxxxxx`）

**优点**:
- ✅ 国内访问速度快
- ✅ 新用户送 ¥18 体验金
- ✅ 价格便宜（¥0.012/千 tokens）

#### OpenAI (GPT)
**获取链接**: https://platform.openai.com/api-keys

需要海外账号和支付方式

#### Anthropic (Claude)
**获取链接**: https://console.anthropic.com/settings/keys

擅长长文本理解

---

### 2. 配置到项目

#### 方法一：网页配置（推荐）

1. 访问 http://localhost:3000/integrations
2. 找到 "通义千问 (Qwen)"
3. 点击 "配置" 按钮
4. 粘贴 API Key（格式：`sk-xxxxxxxx`）
5. 点击 "保存配置"
6. 点击 "测试连接" 验证

#### 方法二：配置文件

在项目根目录创建 `api_keys.json`：

```json
{
  "qwen": {
    "api_key": "sk-your-actual-api-key-here",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "enabled": true,
    "updated_at": "2026-02-27T10:00:00Z"
  }
}
```

---

### 3. 使用 AI 导师

配置完成后：

1. 访问 http://localhost:3000/chat
2. 输入问题，如 "什么是机器学习？"
3. AI 会使用真实的 Qwen API 回答

---

## 📊 API 集成页面功能

### 配置状态

| 状态 | 说明 |
|------|------|
| 🟢 已启用 | API 已配置并启用，AI 导师会使用 |
| 🟡 已配置 | API 已配置但禁用，需要手动启用 |
| ⚪ 未配置 | 需要配置 API Key |

### 操作按钮

| 按钮 | 功能 |
|------|------|
| ⚙️ 配置 | 打开配置模态框，输入 API Key |
| 🔄 测试 | 测试 API 连接是否可用 |
| 👁️ 启用/禁用 | 切换 API 的启用状态 |
| 🗑️ 删除 | 删除已保存的 API Key |

### 多 API 支持

- 可以配置多个 API（Qwen + OpenAI + Anthropic）
- 系统会按优先级自动切换
- 当前启用的 API 会显示绿色标签

---

## 🔧 API 端点

### 获取配置列表
```bash
GET http://localhost:8001/api/v1/api-keys
```

**响应**:
```json
{
  "qwen": {
    "enabled": true,
    "configured": true,
    "last_4_digits": "abcd",
    "updated_at": "2026-02-27T10:00:00Z"
  }
}
```

### 配置 API Key
```bash
POST http://localhost:8001/api/v1/api-keys/{provider}/configure
Content-Type: application/json

{
  "api_key": "sk-your-api-key",
  "base_url": "https://...",",
  "enabled": true
}
```

### 测试 API Key
```bash
POST http://localhost:8001/api/v1/api-keys/{provider}/test
```

**响应**:
```json
{
  "status": "success",
  "message": "Qwen API 连接成功",
  "model": "qwen-plus"
}
```

### 切换启用状态
```bash
POST http://localhost:8001/api/v1/api-keys/{provider}/toggle
```

### 删除 API Key
```bash
DELETE http://localhost:8001/api/v1/api-keys/{provider}
```

---

## 💬 AI 导师 API

### 聊天对话
```bash
POST http://localhost:8001/api/v1/chat/message
Content-Type: application/json

{
  "message": "什么是机器学习？",
  "userId": 1,
  "system_prompt": "你是一位专业的 AI 导师..."
}
```

**响应**:
```json
{
  "message": "机器学习是 AI 的一个分支...",
  "conversationId": "conv_123456",
  "provider": "qwen",
  "suggestions": [
    "能举个具体的例子吗？",
    "这个概念在实际中怎么应用？"
  ],
  "responseTime": 1500
}
```

### 获取可用提供商
```bash
GET http://localhost:8001/api/v1/chat/providers
```

**响应**:
```json
{
  "providers": [
    {
      "id": "qwen",
      "name": "通义千问",
      "enabled": true,
      "configured": true
    }
  ]
}
```

---

## 🎯 工作流程

```
1. 用户在 /integrations 配置 API Key
          ↓
2. API Key 保存到 api_keys.json
          ↓
3. 用户在 /chat 发送消息
          ↓
4. 后端读取 api_keys.json
          ↓
5. 按优先级尝试可用的 API
   - Qwen → OpenAI → Anthropic
          ↓
6. 使用第一个可用的 API 调用
          ↓
7. 返回 AI 回复给前端
```

---

## 🛡️ 安全说明

### API Key 存储
- ✅ 存储在本地 `api_keys.json` 文件
- ✅ 不会上传到任何服务器
- ✅ 仅后端可读取
- ⚠️ 不要提交到 Git（已添加到 .gitignore）

### API Key 显示
- ✅ 前端只显示尾号 4 位
- ✅ 密码输入框默认隐藏
- ✅ 可点击眼睛图标查看

### 最佳实践
1. 定期更新 API Key
2. 不要分享 API Key
3. 监控 API 使用量
4. 设置使用限额

---

## 📊 使用监控

### 查看使用量

访问各 API 提供商的控制台：

- **Qwen**: https://dashscope.console.aliyun.com/usage
- **OpenAI**: https://platform.openai.com/usage
- **Anthropic**: https://console.anthropic.com/settings/usage

### 费用估算

**Qwen 定价**:
- qwen-plus: ¥0.012/千 tokens
- 1000 次对话约 ¥1-2 元

**免费额度**:
- Qwen 新用户送 ¥18
- 可用约 1500 次对话

---

## 🐛 故障排除

### 问题 1: 配置后 AI 导师还是说"未配置"

**解决**:
1. 检查是否启用了 API（绿色标签）
2. 刷新 /chat 页面
3. 检查后端日志

### 问题 2: 测试连接失败

**解决**:
1. 检查 API Key 是否正确
2. 检查网络连接
3. 查看 API 控制台是否欠费

### 问题 3: api_keys.json 不存在

**解决**:
- 第一次配置后会自动创建
- 手动创建空文件：`{}`
- 检查文件权限

---

## 📝 示例配置

### api_keys.json 完整示例

```json
{
  "qwen": {
    "api_key": "sk-qwen-actual-key-1234",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "enabled": true,
    "updated_at": "2026-02-27T10:00:00Z"
  },
  "openai": {
    "api_key": "sk-openai-actual-key-5678",
    "base_url": "https://api.openai.com/v1",
    "enabled": false,
    "updated_at": "2026-02-27T11:00:00Z"
  }
}
```

---

## 🎉 配置完成检查清单

- [ ] 获取了至少一个 API Key
- [ ] 在 /integrations 页面配置了 API
- [ ] 测试连接成功（显示绿色成功消息）
- [ ] API 状态显示"已启用"（绿色标签）
- [ ] 在 /chat 页面看到 API 提供商标签
- [ ] 发送消息收到真实 AI 回复

---

**🎊 配置完成后，享受真实的 AI 对话体验！**

**支持页面**:
- API 集成：http://localhost:3000/integrations
- AI 导师：http://localhost:3000/chat
