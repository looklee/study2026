# ⚠️ API Key 无效

## 错误信息

**错误**: `401 Incorrect API key provided`

**提供的 Key**: `sk-sp-6154c73e2c5948d2b9a430731489b8ed`

**问题**: 这个 API Key 格式不正确或已失效

---

## 🔑 获取正确的 API Key

### 步骤 1: 登录阿里云
访问：https://dashscope.console.aliyun.com/apiKey

### 步骤 2: 创建 API Key
1. 登录阿里云账号
2. 点击 "API Key 管理"
3. 点击 "创建新的 API Key"
4. 复制生成的密钥

### 步骤 3: 正确格式
正确的 API Key 格式：
```
sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**注意**: 不是 `sk-sp-` 开头

---

## 📝 更新配置

获取新的 API Key 后，更新配置文件：

### 方法 1: 编辑文件
编辑 `C:\Users\Administrator\Documents\TRAEproject\STUDY2026\apps\api\api_keys.json`

```json
{
  "qwen": {
    "api_key": "sk-你的新 API 密钥",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "enabled": true,
    "updated_at": "2026-02-27T18:30:00Z"
  }
}
```

### 方法 2: 在网页配置
1. 访问 http://localhost:3000/integrations
2. 点击 "通义千问" 的 "配置" 按钮
3. 输入新的 API Key
4. 保存

---

## 🆓 免费额度

- 新用户赠送 ¥18 体验金
- qwen-plus: ¥0.012/千 tokens
- 可用约 1500 次对话

---

## 🧪 测试

配置新密钥后测试：

```bash
# 测试配置
curl http://localhost:8001/api/v1/api-keys

# 测试对话
curl -X POST http://localhost:8001/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"你好\"}"
```

---

## 📞 需要帮助？

如果还有问题：
1. 检查阿里云控制台确认密钥状态
2. 确认账户有余额
3. 查看 https://help.aliyun.com/zh/model-studio/error-code

---

**更新时间**: 2026-02-27
