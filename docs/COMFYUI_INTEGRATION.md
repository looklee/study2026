# ComfyUI 集成说明

## 概述

本项目集成了 ComfyUI，这是一个基于节点的 Stable Diffusion GUI，允许用户通过本地部署的 ComfyUI 实例进行高级AI图像生成。

## 架构

ComfyUI 集成包括以下组件：

1. **后端服务** (`app/services/comfyui_service.py`)
   - 提供与 ComfyUI API 的交互
   - 包括连接检查、队列管理、图像生成等功能

2. **工作流管理器** (`app/services/comfyui_workflow_manager.py`)
   - 管理预定义的工作流模板
   - 提供快速生成方法（文生图、图生图、局部重绘）

3. **API路由** (`app/api/routes/comfyui_routes.py`)
   - 提供 RESTful API 接口
   - 支持各种 ComfyUI 操作

4. **前端界面** (`apps/web/src/components/comfyui-integration/ComfyUIIntegration.tsx`)
   - 提供用户友好的界面
   - 支持多种生成模式

## 安装 ComfyUI

要使用此集成，您需要在本地安装 ComfyUI：

```bash
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
```

然后启动 ComfyUI：

```bash
python main.py
```

默认情况下，ComfyUI 会在 `http://127.0.0.1:8188` 上运行。

## 配置

在 `.env` 文件中配置 ComfyUI 地址：

```env
COMFYUI_BASE_URL=http://127.0.0.1:8188
```

## API 端点

### 健康检查
- `GET /api/v1/comfyui/health` - 检查 ComfyUI 服务状态

### 队列管理
- `GET /api/v1/comfyui/queue-status` - 获取队列状态
- `POST /api/v1/comfyui/interrupt` - 中断当前任务

### 模型管理
- `GET /api/v1/comfyui/models` - 获取已安装模型列表

### 快速生成
- `POST /api/v1/comfyui/quick/text-to-image` - 快速文生图
- `POST /api/v1/comfyui/quick/image-to-image` - 快速图生图
- `POST /api/v1/comfyui/quick/inpainting` - 快速局部重绘

### 工作流管理
- `GET /api/v1/comfyui/workflow-templates` - 获取工作流模板列表
- `GET /api/v1/comfyui/workflow-templates/{template_name}` - 获取特定模板
- `POST /api/v1/comfyui/generate` - 使用自定义工作流生成

## 前端访问

在前端应用中，可以通过以下路径访问 ComfyUI 工具：

- `/tools/comfyui` - ComfyUI 集成界面

## 使用示例

### 文生图
```python
# 使用快速文生图 API
response = requests.post("http://localhost:8001/api/v1/comfyui/quick/text-to-image", json={
    "prompt": "a beautiful landscape",
    "negative_prompt": "low quality, blurry",
    "width": 1024,
    "height": 1024,
    "steps": 20,
    "cfg": 8.0
})
```

### 图生图
```python
# 使用快速图生图 API
response = requests.post("http://localhost:8001/api/v1/comfyui/quick/image-to-image", json={
    "image_name": "input_image.png",  # 已上传到 ComfyUI 的图像
    "prompt": "change the weather to sunny",
    "width": 512,
    "height": 512,
    "denoise": 0.7
})
```

## 注意事项

1. 确保 ComfyUI 在指定地址上运行
2. 检查防火墙设置，确保端口可访问
3. 确保有足够的 GPU 内存处理图像生成任务
4. 工作流模板存储在 `workflows/templates/` 目录中