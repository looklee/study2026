from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import os

# 检测数据库类型
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

# 同步引擎（用于迁移）
if is_sqlite:
    sync_engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    sync_engine = create_engine(settings.DATABASE_URL)

# 异步引擎（用于应用）
if is_sqlite:
    async_engine = create_async_engine(
        settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"),
        echo=False,
        connect_args={"check_same_thread": False}
    )
else:
    try:
        async_engine = create_async_engine(
            settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
    except Exception:
        # Fallback to sqlite if postgres fails
        async_engine = create_async_engine(
            "sqlite+aiosqlite:///./study2026.db",
            echo=False,
            connect_args={"check_same_thread": False}
        )

# 会话工厂
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base 类
Base = declarative_base()


async def get_db() -> AsyncSession:
    """获取数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """初始化数据库"""
    async with async_engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
