# FFmpeg 和高级去水印功能集成文档

## 概述

本项目已成功集成 FFmpeg 和高级去水印功能，提供了多种图像和视频处理能力，特别是增强了去水印功能，支持涂抹选择等多种方式。

## 功能特性

### 1. FFmpeg 集成功能
- **视频格式转换** - 支持多种视频格式之间的转换
- **帧提取** - 从视频中提取指定帧
- **水印添加/去除** - 为视频和图像添加或去除水印
- **媒体信息获取** - 获取视频和图像的详细信息
- **视频裁剪和缩放** - 调整视频尺寸和裁剪区域

### 2. 高级去水印功能
- **涂抹选择模式** - 在图像上直接涂抹要去除的水印区域
- **矩形选择模式** - 拖拽选择精确的水印区域
- **自动检测模式** - 智能检测常见的水印位置
- **多种算法支持**:
  - 基于坐标的去除
  - 基于颜色范围的去除
  - 基于边缘检测的去除
  - 基于图像分割的去除
  - 基于点击位置的去除

## 架构组件

### 后端服务
1. **FFmpeg服务** (`app/services/ffmpeg_service.py`)
   - 提供FFmpeg命令行工具的封装
   - 支持异步处理
   - 实现多种媒体处理功能

2. **高级去水印服务** (`app/services/advanced_watermark_removal_service.py`)
   - 集成OpenCV和图像处理算法
   - 提供多种去水印方法
   - 支持智能检测

3. **API路由** (`app/api/routes/advanced_watermark_removal_routes.py`)
   - 提供RESTful API接口
   - 支持文件上传和处理

### 前端界面
1. **去水印工具页面** (`apps/web/src/app/tools/advanced-watermark-removal/page.tsx`)
2. **交互式组件** (`apps/web/src/components/advanced-watermark-removal/AdvancedWatermarkRemoval.tsx`)
   - 涂抹选择界面
   - 实时预览功能
   - 多种处理模式

## API 端点

### FFmpeg 相关
- `GET /api/v1/advanced-watermark-removal/health` - 健康检查

### 高级去水印端点
- `POST /api/v1/advanced-watermark-removal/by-coordinates` - 通过坐标去除水印
- `POST /api/v1/advanced-watermark-removal/by-color-range` - 通过颜色范围去除水印
- `POST /api/v1/advanced-watermark-removal/by-edge-detection` - 通过边缘检测去除水印
- `POST /api/v1/advanced-watermark-removal/detect-areas` - 检测水印区域
- `POST /api/v1/advanced-watermark-removal/by-clicks` - 通过点击位置去除水印
- `POST /api/v1/advanced-watermark-removal/by-segmentation` - 通过分割技术去除水印

## 使用方法

### 前端使用
1. 访问 `http://localhost:3000/tools/advanced-watermark-removal`
2. 上传要处理的图像
3. 选择处理模式：
   - 涂抹模式：点击要移除的水印区域
   - 矩形模式：拖拽选择水印区域
   - 自动模式：智能检测水印
4. 调整参数（如笔刷大小）
5. 点击"去除水印"按钮
6. 下载处理后的图像

### API 使用示例

#### 通过坐标去除水印
```bash
curl -X POST "http://localhost:8001/api/v1/advanced-watermark-removal/by-coordinates" \
  -H "Content-Type: application/json" \
  -d '{
    "coordinates": [[100, 100, 200, 50], [300, 200, 100, 30]]
  }'
```

#### 通过点击位置去除水印
```bash
curl -X POST "http://localhost:8001/api/v1/advanced-watermark-removal/by-clicks" \
  -H "Content-Type: application/json" \
  -d '{
    "clicks": [[150, 125], [350, 215]],
    "brush_radius": 20
  }'
```

## 依赖要求

### 系统依赖
- **FFmpeg** - 必须安装在系统PATH中
- **Python库**:
  - opencv-python
  - Pillow
  - numpy

### 安装FFmpeg
Windows:
```bash
# 使用Chocolatey
choco install ffmpeg

# 或手动下载并添加到PATH
```

## 配置

项目会自动检测系统中的FFmpeg，无需额外配置。

## 注意事项

1. **性能考虑** - 图像处理可能消耗较多计算资源
2. **图像质量** - 复杂的水印去除可能影响图像质量
3. **文件大小限制** - 大文件可能需要较长时间处理
4. **浏览器兼容性** - 涂抹功能需要现代浏览器支持Canvas

## 故障排除

### FFmpeg未找到
- 确保FFmpeg已安装并添加到系统PATH
- 检查`ffmpeg -version`命令是否正常工作

### 处理失败
- 检查输入文件格式是否支持
- 确认有足够的磁盘空间
- 查看服务日志获取详细错误信息

## 扩展功能

该集成提供了良好的扩展性，可以轻松添加：
- 更多图像处理算法
- 批量处理功能
- 自定义水印检测规则
- 云端处理支持