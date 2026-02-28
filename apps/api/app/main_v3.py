# Study2026 API - 主应用入口

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入 API 路由
from app.api.api_router import api_router

app = FastAPI(
    title="Study2026 API",
    description="AI 学习平台 API",
    version="3.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Study2026 API v3.0 - 设备识别免登录系统",
        "version": "3.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
