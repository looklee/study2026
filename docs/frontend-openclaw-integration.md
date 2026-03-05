# OpenClaw AI 助手前端集成说明

本文档记录了 OpenClaw AI 助手在 Study2026 前端项目中的集成详情。

## 集成内容

### 1. API 服务集成
- 文件: `src/lib/api.ts`
- 添加了 OpenClaw API 服务接口，包括：
  - `openclawApi.process`: 处理AI请求
  - `openclawApi.executeSkill`: 执行AI技能
  - `openclawApi.getSkills`: 获取可用技能列表
  - `openclawApi.chat`: AI对话接口
  - `openclawApi.health`: 健康检查接口

### 2. 页面集成

#### 主要聊天界面
- 文件: `src/app/openclaw/page.tsx`
- 功能: OpenClaw AI助手的主要交互界面
- 特性: 消息历史、快捷操作、技能显示、实时聊天

#### 布局配置
- 文件: `src/app/openclaw/layout.tsx`
- 功能: OpenClaw页面的布局组件

#### 工具中心
- 文件: `src/app/tools/openclaw/page.tsx`
- 文件: `src/app/tools/openclaw/hub.tsx`
- 功能: OpenClaw工具集的入口页面

#### 配置页面
- 文件: `src/app/integrations/openclaw/page.tsx`
- 功能: OpenClaw服务的配置和管理界面

### 3. 导航集成
- 文件: `src/components/Sidebar.tsx`
- 更新: 添加了 "OpenClaw 助手" 导航项，链接到 `/openclaw`

### 4. 工具库集成
- 文件: `src/lib/ai-tools-database.ts`
- 更新: 添加了 OpenClaw 工具条目 (id: '13')
- 特性: 在AI工具库中显示OpenClaw助手

### 5. 集成页面增强
- 文件: `src/app/integrations/page.tsx`
- 更新: 为OpenClaw提供专用配置链接，而非外部API密钥获取

## 使用方式

1. 通过侧边栏的 "OpenClaw 助手" 链接访问AI助手
2. 在 "AI 工具库" 中可以找到OpenClaw工具
3. 在 "API 集成" 页面可以配置OpenClaw服务
4. 在 "AI 工具库" -> "OpenClaw" 可以访问专门的工具中心

## 依赖

此集成依赖于后端提供的 OpenClaw API 服务，包括:
- `/api/v1/openclaw/process`
- `/api/v1/openclaw/execute-skill`
- `/api/v1/openclaw/skills`
- `/api/v1/openclaw/chat`
- `/api/v1/openclaw/health`

## 注意事项

- 确保后端服务已正确部署并启用了OpenClaw API端点
- 前端通过 `@tanstack/react-query` 管理API状态
- 所有API调用都通过 `axios` 配置的基地址进行