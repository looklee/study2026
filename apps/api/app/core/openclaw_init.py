"""
OpenClaw 初始化模块
用于在应用启动时初始化OpenClaw服务
"""
import logging
from typing import Optional
from app.services.openclaw_service import get_openclaw_service, OpenClawConfig


logger = logging.getLogger(__name__)


async def initialize_openclaw_service(api_key: Optional[str] = None, base_url: Optional[str] = None):
    """
    初始化OpenClaw服务
    :param api_key: API密钥
    :param base_url: API基础URL
    """
    logger.info("Initializing OpenClaw service...")
    
    try:
        # 获取服务实例
        service = get_openclaw_service()
        
        # 配置服务
        config = OpenClawConfig(
            api_key=api_key,
            base_url=base_url
        )
        service.config = config
        
        # 初始化服务
        await service.initialize()
        
        logger.info("OpenClaw service initialized successfully")
        return service
    except Exception as e:
        logger.error(f"Failed to initialize OpenClaw service: {e}")
        raise


async def shutdown_openclaw_service():
    """关闭OpenClaw服务"""
    logger.info("Shutting down OpenClaw service...")
    # 如果有需要清理的资源，在这里处理
    logger.info("OpenClaw service shut down completed")


# 便捷函数
async def get_configured_openclaw_service(api_key: Optional[str] = None, base_url: Optional[str] = None):
    """
    获取已配置的OpenClaw服务实例
    :param api_key: API密钥
    :param base_url: API基础URL
    """
    service = get_openclaw_service()
    
    if api_key or base_url:
        config = OpenClawConfig(
            api_key=api_key,
            base_url=base_url
        )
        service.config = config
    
    if not service.initialized:
        await service.initialize()
    
    return service