# 🔑 通义灵码 API Key 获取指南

## ⚠️ 当前 API Key 无效

**错误**: `InvalidApiKey.Invalid API-key provided.`

**提供的 Key**: `sk-sp-6154c73e2c5948d2b9a430731489b8ed`

这个 Key 格式是旧的测试密钥，已经失效。

---

## ✅ 获取有效的 API Key

### 步骤 1: 访问阿里云百炼平台

**地址**: https://bailian.console.aliyun.com/

### 步骤 2: 登录/注册

1. 使用阿里云账号登录
2. 如果没有账号，先注册

### 步骤 3: 创建 API Key

1. 进入"API-KEY 管理"页面
2. 点击"创建新的 API-KEY"
3. 复制生成的密钥

**正确的格式**: `sk-xxxxxxxxxxxxxxxxxxxxxxxx`
（不是 `sk-sp-` 开头）

### 步骤 4: 开通服务

确保开通以下服务：
- ✅ 通义千问（通用对话）
- ✅ 通义灵码（编程专用）

---

## 📝 配置 API Key

### 方法 1: 网页配置

1. 访问 http://localhost:3000/integrations
2. 点击"通义千问"的"配置"
3. 输入新的 API Key
4. Base URL 选择：
   - 通用 API: `https://dashscope.aliyuncs.com/compatible-mode/v1`
   - 通义灵码：`https://coding.dashscope.aliyuncs.com/v1`
5. 保存

### 方法 2: 编辑配置文件

编辑 `api_keys.json`:

```json
{
  "qwen": {
    "api_key": "sk-你的新密钥",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "enabled": true
  }
}
```

---

## 🆓 免费额度

- 新用户赠送 ¥18 体验金
- qwen-plus: ¥0.012/千 tokens
- qwen-coder-plus: ¥0.02/千 tokens
- 可用约 1000-1500 次对话

---

## 🧪 测试

配置后测试：

```bash
# 测试配置
curl http://localhost:8001/api/v1/api-keys

# 测试对话
curl -X POST http://localhost:8001/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"你好\"}"
```

**预期响应**:
```json
{
  "message": "你好！我是你的 AI 导师...",
  "provider": "qwen",
  "conversationId": "conv_xxx"
}
```

---

## 📊 支持的模型

### 通用 API
- qwen-plus（推荐）
- qwen-max
- qwen-turbo

### 通义灵码（编程专用）
- qwen-coder-plus（推荐）
- qwen-coder-turbo

---

## 🔗 相关链接

| 服务 | 链接 |
|------|------|
| 百炼控制台 | https://bailian.console.aliyun.com/ |
| API Key 管理 | https://bailian.console.aliyun.com/api-key |
| 通义千问文档 | https://help.aliyun.com/zh/dashscope/ |
| 通义灵码文档 | https://help.aliyun.com/zh/model-studio/ |

---

**更新时间**: 2026-02-27
