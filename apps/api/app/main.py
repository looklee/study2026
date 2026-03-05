# Study2026 API 主入口

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import init_db
from app.api import auth, users, chat, knowledge, progress, workflows, recommendations, files, pet, checkin
from app.services.scheduler import get_scheduler
from app.core.openclaw_init import initialize_openclaw_service, shutdown_openclaw_service
from app.services.comfyui_service import initialize_comfyui_service, shutdown_comfyui_service

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 Study2026 API 启动中...")

    # 初始化数据库
    await init_db()
    logger.info("✅ 数据库初始化完成")

    # 启动任务调度器
    scheduler = get_scheduler()
    logger.info("✅ 任务调度器已启动")

    # 初始化OpenClaw服务
    await initialize_openclaw_service(
        api_key=settings.OPENCLAW_API_KEY,
        base_url=settings.OPENCLAW_BASE_URL
    )
    logger.info("✅ OpenClaw服务初始化完成")

    # 初始化ComfyUI服务
    await initialize_comfyui_service()
    logger.info("✅ ComfyUI服务初始化完成")

    yield

    # 关闭时执行
    logger.info("👋 Study2026 API 关闭中...")
    scheduler.shutdown()
    logger.info("✅ 任务调度器已关闭")

    # 关闭OpenClaw服务
    await shutdown_openclaw_service()
    logger.info("✅ OpenClaw服务已关闭")

    # 关闭ComfyUI服务
    await shutdown_comfyui_service()
    logger.info("✅ ComfyUI服务已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI 驱动的学习平台 API",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异常：{exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误", "error": str(exc) if settings.DEBUG else "请稍后重试"}
    )


# 健康检查
@app.get("/health", tags=["健康检查"])
async def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "database": "connected"
    }


# 注册路由
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)
app.include_router(chat.router, prefix=settings.API_PREFIX)
app.include_router(knowledge.router, prefix=settings.API_PREFIX)
app.include_router(progress.router, prefix=settings.API_PREFIX)
app.include_router(workflows.router, prefix=settings.API_PREFIX)
app.include_router(recommendations.router, prefix=settings.API_PREFIX)
app.include_router(files.router, prefix=settings.API_PREFIX)
app.include_router(pet.router, prefix=settings.API_PREFIX)
app.include_router(checkin.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG
    )
