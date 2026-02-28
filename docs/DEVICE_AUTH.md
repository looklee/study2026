# 🔐 机器码免登录系统文档

## 🎯 功能特点

### 1. 设备指纹识别
- ✅ 自动收集设备信息
- ✅ 生成唯一设备 ID
- ✅ 无需手动注册
- ✅ 首次访问自动创建账户

### 2. 会话管理
- ✅ 30 天自动续期
- ✅ LocalStorage 持久化
- ✅ 多设备支持
- ✅ 自动登录

### 3. 用户系统
- ✅ 设备关联用户
- ✅ 用户偏好设置
- ✅ 学习数据统计
- ✅ 多设备关联

---

## 🚀 工作原理

### 设备识别流程
```
1. 用户访问网站
   ↓
2. 前端收集设备信息
   - 操作系统
   - 浏览器
   - 语言
   - 时区
   - 屏幕分辨率
   - CPU 核心数
   - 内存大小
   ↓
3. 发送到后端
   ↓
4. 生成设备指纹 (SHA256)
   ↓
5. 检查设备是否存在
   ↓
6a. 新设备 → 创建用户 → 返回用户信息
6b. 老设备 → 更新最后登录 → 返回用户信息
   ↓
7. 创建会话 (30 天)
   ↓
8. 保存到 LocalStorage
```

### 自动登录流程
```
1. 页面加载
   ↓
2. 从 LocalStorage 读取 session_id
   ↓
3. 验证会话是否有效
   ↓
4a. 有效 → 恢复用户状态
4b. 无效 → 重新识别设备
   ↓
5. 完成登录
```

---

## 📊 API 端点

### 设备识别
```bash
POST /api/v1/device/identify
Content-Type: application/json

{
  "platform": "Win32",
  "browser": "Chrome120",
  "language": "zh-CN",
  "timezone": "Asia/Shanghai",
  "screen": "1920x1080",
  "cores": 8,
  "memory": 16
}
```

**响应**:
```json
{
  "status": "success",
  "device_id": "a1b2c3d4e5f6...",
  "session_id": "session_user_123...",
  "user": {
    "user_id": "user_a1b2c3d4",
    "username": "用户_a1b2c3d4",
    "email": "user_a1b2c3d4@local.device",
    "created_at": "2026-02-27T...",
    "last_login": "2026-02-27T...",
    "login_count": 1,
    "device_count": 1
  },
  "message": "设备已注册"
}
```

### 验证会话
```bash
GET /api/v1/device/verify/{session_id}
```

**响应**:
```json
{
  "status": "success",
  "session": {...},
  "user": {...}
}
```

### 获取用户信息
```bash
GET /api/v1/user/{user_id}
```

### 更新用户偏好
```bash
POST /api/v1/user/{user_id}/preferences
Content-Type: application/json

{
  "theme": "dark",
  "language": "zh-CN",
  "notifications": true
}
```

---

## 🔧 前端使用

### AuthContext

```typescript
import { useAuth } from '@/contexts/AuthContext'

function MyComponent() {
  const { user, deviceId, sessionId, isLoading, logout } = useAuth()

  if (isLoading) return <div>识别中...</div>

  return (
    <div>
      <p>欢迎，{user?.username}!</p>
      <p>设备 ID: {deviceId}</p>
      <button onClick={logout}>切换设备</button>
    </div>
  )
}
```

### 设备信息收集

```typescript
const getDeviceInfo = () => {
  return {
    platform: navigator.platform,
    browser: navigator.userAgent.split(' ').pop(),
    language: navigator.language,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    screen: `${screen.width}x${screen.height}`,
    cores: navigator.hardwareConcurrency,
    memory: (navigator as any).deviceMemory
  }
}
```

---

## 📱 侧边栏用户显示

### 已登录状态
```
┌─────────────────────────┐
│  👤 用户_a1b2           │
│  user_a1b2c3d4          │
│  [🚪 切换设备]          │
└─────────────────────────┘
```

### 识别中状态
```
┌─────────────────────────┐
│     识别中...           │
└─────────────────────────┘
```

---

## 🔐 安全特性

### 1. 设备指纹
- 使用 SHA256 哈希
- 32 位唯一标识
- 不可逆向破解

### 2. 会话管理
- 30 天自动续期
- 过期自动清理
- 单设备单会话

### 3. 数据隔离
- 用户数据独立
- 设备数据独立
- 会话数据独立

---

## 📊 数据存储

### 内存存储（演示）
```python
devices = {}      # 设备数据
users = {}        # 用户数据
sessions = {}     # 会话数据
```

### 持久化（生产环境建议）
```python
# 使用数据库存储
- PostgreSQL: 用户和设备
- Redis: 会话缓存
```

---

## 🎯 用户体验

### 首次访问
1. 自动识别设备（<1 秒）
2. 自动创建账户
3. 显示欢迎消息
4. 开始使用

### 再次访问
1. 自动恢复会话（<0.5 秒）
2. 无需任何操作
3. 直接使用

### 切换设备
1. 点击"切换设备"
2. 清除本地会话
3. 新设备重新识别
4. 数据独立保存

---

## 🔍 调试工具

### 查看所有用户
```bash
GET /api/v1/users
```

### 查看所有设备
```bash
GET /api/v1/devices
```

---

## 📈 数据统计

### 用户统计
- 总用户数
- 活跃用户数
- 平均登录次数
- 平均设备数

### 设备统计
- 总设备数
- 平台分布
- 浏览器分布
- 地域分布

---

## 🐛 故障排除

### 问题 1: 一直显示"识别中"
**解决**: 检查后端 API 是否运行，网络是否通畅

### 问题 2: 切换设备后数据丢失
**解决**: 数据按设备隔离是正常行为，每个设备有独立的学习数据

### 问题 3: 会话过期
**解决**: 30 天未访问会过期，重新访问会自动创建新会话

---

## 🎯 未来改进

### 1. 数据同步
- [ ] 多设备数据同步
- [ ] 云端备份
- [ ] 数据合并

### 2. 安全增强
- [ ] IP 限制
- [ ] 设备绑定
- [ ] 异常检测

### 3. 用户体验
- [ ] 设备管理界面
- [ ] 会话历史
- [ ] 登录通知

---

**访问地址**: http://localhost:3000  
**API 文档**: http://localhost:8001/docs  
**更新时间**: 2026-02-27
