from fastapi import APIRouter
from app.api.routes import (
    users,
    paths,
    progress,
    chat,
    workflows,
    recommendations,
    knowledge,
    device,
    openclaw_routes,
    multimedia_routes,
    comfyui_routes,
    advanced_watermark_removal_routes
)

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(paths.router, prefix="/paths", tags=["学习路径"])
api_router.include_router(progress.router, prefix="/progress", tags=["进度追踪"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI 对话"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["工作流"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["内容推荐"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["知识库"])
api_router.include_router(device.router, prefix="/device", tags=["设备识别"])
api_router.include_router(openclaw_routes.router, prefix="/openclaw", tags=["OpenClaw AI助手"])
api_router.include_router(multimedia_routes.router, prefix="/multimedia", tags=["多媒体AI处理"])
api_router.include_router(comfyui_routes.router, prefix="/comfyui", tags=["ComfyUI集成"])
api_router.include_router(advanced_watermark_removal_routes.router, prefix="/advanced-watermark-removal", tags=["高级去水印"])
