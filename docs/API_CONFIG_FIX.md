# 🔧 API 集成配置修复说明

## ✅ 已修复的问题

### 问题描述
之前配置 base_url 时无法保存，因为：
1. 前端在编辑模式下 API Key 显示为 `sk-...` 导致条件判断失败
2. 后端会无条件覆盖 api_key，即使传的是 undefined

### 修复内容

#### 前端修复
```typescript
// 修复前
const handleSave = () => {
  if (selectedProvider && apiKey && !apiKey.startsWith('sk-...')) {
    configureMutation.mutate({
      provider: selectedProvider,
      key: apiKey,
      url: baseUrl
    })
  }
}

// 修复后
const handleSave = () => {
  if (selectedProvider) {
    if ((apiKey && !apiKey.startsWith('sk-...')) || baseUrl) {
      configureMutation.mutate({
        provider: selectedProvider,
        key: apiKey.startsWith('sk-...') ? undefined : apiKey,
        url: baseUrl
      })
    }
  }
}
```

#### 后端修复
```python
# 修复前
keys[provider]["api_key"] = config.api_key  # 无条件覆盖

# 修复后
if config.api_key and config.api_key != "undefined":
    keys[provider]["api_key"] = config.api_key  # 只有新 key 才更新
if config.base_url:
    keys[provider]["base_url"] = config.base_url  # base_url 始终更新
```

---

## 📝 配置说明

### 首次配置 API

1. 点击 "配置" 按钮
2. 输入 API Key（必填）
3. Base URL 会自动填充（可选修改）
4. 点击 "保存配置"

### 只修改 Base URL

1. 点击 "配置" 按钮
2. **保持 API Key 为空**（会使用已保存的）
3. 修改 Base URL
4. 点击 "保存配置"

### 只修改 API Key

1. 点击 "配置" 按钮
2. 输入新的 API Key
3. Base URL 保持不变
4. 点击 "保存配置"

---

## 🧪 测试步骤

### 测试 1: 首次配置
1. 选择 "通义千问"
2. 点击 "配置"
3. 输入 API Key: `sk-test123456`
4. Base URL 保持默认
5. 保存
6. ✅ 应该显示 "配置已保存"

### 测试 2: 修改 Base URL
1. 再次点击 "通义千问" 的 "配置"
2. **不要输入 API Key**
3. 修改 Base URL 为：`https://custom-url.com`
4. 保存
5. ✅ 应该显示 "配置已保存"
6. ✅ Base URL 已更新，API Key 保持不变

### 测试 3: 修改 API Key
1. 再次点击 "配置"
2. 输入新的 API Key: `sk-newkey789`
3. Base URL 保持不变
4. 保存
5. ✅ 应该显示 "配置已保存"
6. ✅ API Key 已更新，Base URL 保持不变

---

## 📊 配置数据结构

保存后的配置存储在 `api_keys.json`：

```json
{
  "qwen": {
    "api_key": "sk-actual-key-here",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "enabled": true,
    "updated_at": "2026-02-27T10:00:00Z"
  },
  "openai": {
    "api_key": "sk-openai-key-here",
    "base_url": "https://api.openai.com/v1",
    "enabled": true,
    "updated_at": "2026-02-27T10:00:00Z"
  }
}
```

---

## 🛠️ 手动编辑配置

如果前端配置有问题，可以直接编辑 `api_keys.json` 文件：

位置：`C:\Users\Administrator\Documents\TRAEproject\STUDY2026\api_keys.json`

```json
{
  "qwen": {
    "api_key": "你的实际密钥",
    "base_url": "自定义 Base URL",
    "enabled": true,
    "updated_at": "2026-02-27T10:00:00Z"
  }
}
```

编辑后重启后端服务。

---

## ⚠️ 常见问题

### Q1: 保存后配置丢失
**A**: 检查 `api_keys.json` 文件是否有写入权限

### Q2: 修改 Base URL 后 API Key 没了
**A**: 这是之前的问题，已修复。如果还有问题，请手动编辑 `api_keys.json`

### Q3: 配置保存成功但测试失败
**A**: 
1. 检查 API Key 是否正确
2. 检查 Base URL 是否正确
3. 检查网络连接
4. 查看后端日志

---

## 🔧 后端日志

启动后端时查看详细日志：

```bash
cd apps/api
python -m uvicorn app.main_v3:app --reload --log-level debug
```

---

**修复完成时间**: 2026-02-27  
**版本**: v2.2.1
