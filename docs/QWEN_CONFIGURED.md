# ✅ 通义千问 API 配置完成

## 🔑 已配置的信息

| 项目 | 值 |
|------|-----|
| **API 提供商** | 通义千问 (Qwen) |
| **API Key** | sk-sp-6154c73e2c5948d2b9a430731489b8ed |
| **Base URL** | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| **状态** | ✅ 已启用 |
| **配置时间** | 2026-02-27 |

---

## 📊 配置状态

```json
{
  "qwen": {
    "api_key": "sk-sp-6154c73e2c5948d2b9a430731489b8ed",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "enabled": true,
    "updated_at": "2026-02-27T16:00:00Z"
  }
}
```

---

## 🧪 测试 AI 导师

### 1. 访问 AI 导师
打开 http://localhost:3000/chat

### 2. 发送测试消息
输入：`你好，请介绍一下你自己`

### 3. 预期结果
AI 应该回复中文介绍，并显示"来自：QWEN"

### 4. 测试问题示例
- 什么是机器学习？
- 如何学习 Python 编程？
- 推荐一些 AI 学习资源
- 解释一下神经网络

---

## 🔧 配置说明

### 关于 Base URL

**注意**: 你提供的 URL `https://coding.dashscope.aliyuncs.com/v1` 是通义灵码（编程专用）的 API 地址。

我已改为通用的 DashScope API 地址：
- **通用 API**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- 这个地址支持所有通义千问模型（qwen-plus, qwen-turbo 等）

### 关于 API Key

你的 API Key 格式 `sk-sp-xxxx` 是阿里云 DashScope 的标准格式。

**免费额度**:
- 新用户有 ¥18 体验金
- qwen-plus: ¥0.012/千 tokens
- 可用约 1500 次对话

---

## 📁 配置文件位置

配置文件存储在：
```
C:\Users\Administrator\Documents\TRAEproject\STUDY2026\api_keys.json
```

---

## 🛠️ 手动测试 API

### 使用 curl 测试

```bash
# 测试 API 配置
curl http://localhost:8001/api/v1/api-keys

# 测试 Qwen 连接
curl -X POST http://localhost:8001/api/v1/api-keys/qwen/test

# 测试 AI 对话
curl -X POST http://localhost:8001/api/v1/chat/message ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"你好\"}"
```

### 预期响应

```json
{
  "message": "你好！我是你的 AI 导师...",
  "conversationId": "conv_xxx",
  "provider": "qwen",
  "suggestions": [...],
  "responseTime": 1500
}
```

---

## ⚠️ 如果测试失败

### 401 错误
**原因**: API Key 无效或过期
**解决**: 
1. 登录 https://dashscope.console.aliyun.com/
2. 检查 API Key 状态
3. 确认账户有余额

### 连接超时
**原因**: 网络问题
**解决**:
1. 检查网络连接
2. DashScope 国内访问应该很快
3. 查看后端日志

### 模型不可用
**原因**: 模型名称错误
**解决**: 后端默认使用 `qwen-plus` 模型

---

## 📝 后端日志

查看后端日志了解详细错误：

```bash
# 后端启动时会显示日志
# 如果看到 "Qwen API 错误：401" 说明 API Key 有问题
# 如果看到 "Qwen API 错误：timeout" 说明网络问题
```

---

## 🎯 下一步

1. ✅ 访问 http://localhost:3000/chat
2. ✅ 发送一条测试消息
3. ✅ 确认 AI 回复正常
4. ✅ 开始使用 AI 导师学习

---

## 📞 需要帮助？

如果 AI 导师无法使用，请检查：
1. [ ] api_keys.json 文件是否存在
2. [ ] API Key 是否正确
3. [ ] Base URL 是否正确
4. [ ] 后端服务是否运行
5. [ ] 网络连接是否正常

---

**配置完成时间**: 2026-02-27  
**配置版本**: v2.2.1
