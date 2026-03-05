from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # 项目配置
    PROJECT_NAME: str = "Study2026"
    API_V1_PREFIX: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://n8n:n8n@localhost:5432/study2026"
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379"
    
    # ChromaDB 配置
    CHROMA_URL: str = "http://localhost:8000"
    
    # AI 配置
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_AI_MODEL: str = "gpt-4o"

    # OpenClaw 配置
    OPENCLAW_API_KEY: str = ""
    OPENCLAW_BASE_URL: str = "https://api.openai.com/v1"

    # ComfyUI 配置
    COMFYUI_BASE_URL: str = "http://127.0.0.1:8188"
    
    # JWT 配置
    JWT_SECRET: str = Field(default_factory=lambda: os.environ.get('JWT_SECRET', 'change-this-secret-in-production'), description="JWT 密钥，生产环境中必须设置强密钥")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天
    
    # CORS 配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5678"]
    
    # Celery 配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
