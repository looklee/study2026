"""
AI助手服务 - 集成OpenClaw能力
"""
from typing import Dict, Any, Optional
from app.services.openclaw_service import get_openclaw_service
from app.core.openclaw_init import get_configured_openclaw_service


async def process_learning_request(user_query: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    处理学习相关的用户请求
    :param user_query: 用户查询
    :param user_context: 用户上下文
    :return: 处理结果
    """
    openclaw_service = get_openclaw_service()
    
    # 添加学习平台特定的上下文
    context = user_context or {}
    context.update({
        "domain": "education",
        "platform": "study2026",
        "features": ["learning_paths", "progress_tracking", "ai_tutoring"]
    })
    
    result = await openclaw_service.process_request(
        user_input=user_query,
        context=context
    )
    
    return result


async def execute_educational_skill(skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行教育相关的技能
    :param skill_name: 技能名称
    :param params: 参数
    :return: 执行结果
    """
    openclaw_service = get_openclaw_service()
    
    # 确保技能名称符合教育场景
    if not skill_name.startswith("edu_"):
        skill_name = f"edu_{skill_name}"
    
    result = await openclaw_service.execute_skill(
        skill_name=skill_name,
        params=params
    )
    
    return result


async def get_personalized_learning_advice(user_profile: Dict[str, Any], learning_history: list) -> Dict[str, Any]:
    """
    获取个性化学习建议
    :param user_profile: 用户档案
    :param learning_history: 学习历史
    :return: 个性化建议
    """
    openclaw_service = get_openclaw_service()
    
    context = {
        "user_profile": user_profile,
        "learning_history": learning_history,
        "request_type": "personalized_learning_advice"
    }
    
    advice_request = f"""
    基于以下用户资料和学习历史，请提供个性化的学习建议：
    
    用户资料: {str(user_profile)}
    学习历史: {str(learning_history)}
    
    请提供具体的学习路径建议、时间安排和资源推荐。
    """
    
    result = await openclaw_service.process_request(
        user_input=advice_request,
        context=context
    )
    
    return result


async def chat_with_ai_tutor(message: str, conversation_context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    与AI导师对话
    :param message: 用户消息
    :param conversation_context: 对话上下文
    :return: 导师回复
    """
    openclaw_service = get_openclaw_service()
    
    context = conversation_context or {}
    context.update({"conversation_type": "ai_tutoring"})
    
    result = await openclaw_service.chat_with_memory(
        user_message=message,
        conversation_id=context.get("conversation_id")
    )
    
    return result