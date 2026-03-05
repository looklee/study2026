#!/usr/bin/env python3
"""
数据库初始化脚本
创建所有表并初始化默认数据
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import init_db, async_engine, Base
from app.core.config import settings
from sqlalchemy import text


async def check_db_connection():
    try:
        async with async_engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ 数据库连接成功")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败：{e}")
        return False


async def create_tables():
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ 数据表创建成功")
        return True
    except Exception as e:
        print(f"❌ 数据表创建失败：{e}")
        return False


async def main():
    print("=" * 50)
    print("🗄️  Study2026 数据库初始化")
    print("=" * 50)
    print(f"数据库 URL: {settings.DATABASE_URL}")
    print()
    
    print("📡 检查数据库连接...")
    if not await check_db_connection():
        print("\n❌ 初始化失败：无法连接数据库")
        return False
    
    print("\n📊 创建数据表...")
    if not await create_tables():
        return False
    
    print("\n📋 已创建的表:")
    async with async_engine.begin() as conn:
        if settings.DATABASE_URL.startswith("sqlite"):
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        else:
            result = await conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename"))
        tables = [row[0] for row in result]
        for table in sorted(tables):
            print(f"  - {table}")
    
    print()
    print("=" * 50)
    print("✅ 数据库初始化完成!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
