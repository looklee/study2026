from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from app.models import Conversation
from app.schemas import ChatMessage, ChatResponse
import json


class ChatService:
    """聊天服务"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.DEFAULT_AI_MODEL,
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )
    
    async def send_message(
        self, db: AsyncSession, message_data: ChatMessage
    ) -> ChatResponse:
        """发送消息并获取回复"""
        
        # 构建系统提示
        system_prompt = """你是一位专业、耐心、友善的 AI 导师，专注于帮助学生掌握 AI 和机器学习知识。

你的特点：
1. 善于用简单易懂的语言解释复杂概念
2. 鼓励学生思考，而不是直接给出答案
3. 根据学生的水平调整讲解深度
4. 提供实用的代码示例和最佳实践
5. 指出常见错误和注意事项

请用中文回答，除非用户特别要求使用英文。"""

        # 调用 LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=message_data.message)
        ]
        
        import time
        start_time = time.time()
        response = await self.llm.ainvoke(messages)
        response_time = int((time.time() - start_time) * 1000)
        
        # 生成后续问题建议
        suggestions = generate_follow_up_questions(message_data.message)
        
        # 保存对话记录
        conversation = Conversation(
            user_id=message_data.userId,
            conversation_id=message_data.conversationId or f"conv_{int(time.time())}",
            user_message=message_data.message,
            bot_response=response.content,
            response_time_ms=response_time,
            model_used=settings.DEFAULT_AI_MODEL
        )
        
        db.add(conversation)
        await db.commit()
        
        return ChatResponse(
            message=response.content,
            conversationId=conversation.conversation_id,
            topics=["AI 学习"],
            suggestions=suggestions,
            responseTime=response_time
        )


async def get_conversation(db: AsyncSession, conversation_id: str) -> List[dict]:
    """获取对话历史"""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.conversation_id == conversation_id)
        .order_by(Conversation.created_at.asc())
    )
    conversations = result.scalars().all()
    
    return [
        {
            "role": "user",
            "content": c.user_message,
            "timestamp": c.created_at.isoformat()
        }
        if i % 2 == 0
        else {
            "role": "assistant",
            "content": c.bot_response,
            "timestamp": c.created_at.isoformat()
        }
        for i, c in enumerate(conversations)
    ]


async def list_conversations(
    db: AsyncSession, user_id: int, limit: int = 20
) -> List[dict]:
    """获取对话列表"""
    # 实现获取对话列表逻辑
    return []


def generate_follow_up_questions(topic: str) -> List[str]:
    """生成后续问题"""
    questions = {
        "概念": ["能举个具体的例子吗？", "这个概念在实际中怎么应用？"],
        "代码": ["这段代码的时间复杂度是多少？", "有没有更优化的写法？"],
        "学习": ["我应该先学什么？", "每天需要花多少时间？"],
    }
    
    for key, qs in questions.items():
        if key in topic:
            return qs
    
    return ["能详细解释一下吗？", "有什么学习资源推荐？"]


# 全局服务实例
chat_service = ChatService()
