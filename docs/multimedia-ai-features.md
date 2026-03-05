# AI 多媒体创作功能模块

本模块实现了多种AI驱动的多媒体内容生成功能，包括文生图、图生图、视频生成和图片编辑。

## 功能特性

### 1. 文生图 (Text-to-Image)
- 根据文本描述生成高质量图像
- 支持自定义尺寸（最小256x256，最大1536x1536）
- 支持多种艺术风格（现实主义、动漫、数字艺术等）
- 可设置负面提示词以避免不需要的元素
- 支持批量生成多张图像

### 2. 图生图 (Image-to-Image)
- 基于参考图像和文本描述生成新图像
- 可调节变换强度（0.1-1.0）
- 支持上传参考图片进行风格转换
- 可指定目标艺术风格

### 3. 视频生成 (Video Generation)
- 根据文本描述生成视频内容
- 可自定义视频时长（1-30秒）
- 支持调整分辨率和帧率
- 适用于创意视频制作

### 4. 图片编辑 (Image Editing)
- 智能编辑和修复图片内容
- 支持蒙版指定编辑区域
- 通过自然语言指令进行编辑

## 技术架构

### 后端 (Python/FastAPI)
- `app/services/multimedia_service.py`: 核心业务逻辑
- `app/api/routes/multimedia_routes.py`: API路由定义
- 集成到主API路由器 (`app/api/api_router.py`)

### 前端 (React/Next.js)
- `src/components/multimedia/`: UI组件库
- `src/app/multimedia/page.tsx`: 主页面
- `src/lib/api.ts`: API服务接口
- 集成到侧边栏导航和工具库

## API 端点

- `POST /api/v1/multimedia/text-to-image` - 文生图
- `POST /api/v1/multimedia/image-to-image` - 图生图
- `POST /api/v1/multimedia/generate-video` - 视频生成
- `POST /api/v1/multimedia/edit-image` - 图片编辑
- `GET /api/v1/multimedia/styles` - 获取支持的样式
- `GET /api/v1/multimedia/job-status/{job_id}` - 获取任务状态
- `POST /api/v1/multimedia/upload-image` - 图片上传
- `GET /api/v1/multimedia/health` - 健康检查

## 用户界面

- 导航: 侧边栏中的 "AI 创作" 链接
- 工具库: 在AI工具库中可找到 "AI 多媒体创作" 工具
- 功能标签页: 包含四个主要功能的切换标签

## 扩展性

本模块设计为可扩展架构，可以轻松添加新的多媒体AI功能：
- 添加新的请求模型到 `multimedia_service.py`
- 添加新的API端点到 `multimedia_routes.py`
- 创建新的前端组件
- 在主页面中添加标签页

## 未来发展方向

- 集成更多AI模型（如DALL-E、Stable Diffusion、Runway ML等）
- 添加音频生成功能
- 实现3D模型生成功能
- 增加更多的编辑工具和滤镜