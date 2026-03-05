from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from app.models import KnowledgeDocument
from app.schemas import RecommendationRequest, KnowledgeQuery
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings


async def get_recommendations(
    db: AsyncSession, request: RecommendationRequest
) -> Dict[str, Any]:
    """获取推荐内容"""
    
    # 使用 AI 生成推荐
    llm = ChatOpenAI(
        model=settings.DEFAULT_AI_MODEL,
        temperature=0.6,
        api_key=settings.OPENAI_API_KEY
    )
    
    system_prompt = """你是一位专业的学习内容策展人。
根据学习者的需求和水平，推荐高质量的学习资源。

输出格式：
{
  "recommendations": [
    {
      "id": "rec_1",
      "title": "资源标题",
      "type": "course|video|article|project",
      "url": "链接",
      "description": "描述",
      "difficulty": "beginner|intermediate|advanced",
      "estimatedHours": 5,
      "rating": 4.5,
      "reason": "推荐理由",
      "tags": ["标签"]
    }
  ],
  "learningPath": "学习顺序建议",
  "tips": "学习建议"
}"""

    user_prompt = f"""请为以下学习者推荐 {request.limit} 个资源：

主题：{', '.join(request.topics)}
水平：{request.level}
编程语言：{', '.join(request.languages)}
预算：{request.pricePreference}"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = await llm.ainvoke(messages)
    
    import json
    import re
    
    # 解析 JSON 响应
    json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
    if json_match:
        result = json.loads(json_match.group())
    else:
        result = {
            "recommendations": [],
            "learningPath": "按难度递增顺序学习",
            "tips": "每天坚持学习 1-2 小时"
        }
    
    return {
        "status": "success",
        "recommendations": result.get("recommendations", []),
        "learningPath": result.get("learningPath", ""),
        "tips": result.get("tips", "")
    }


async def upload_document(
    db: AsyncSession, file, category: str, tags: List[str]
) -> Dict[str, Any]:
    """上传文档"""
    
    # 读取文件内容
    content = await file.read()
    
    document = KnowledgeDocument(
        file_name=file.filename,
        file_size=len(content),
        mime_type=file.content_type,
        category=category,
        tags=tags,
        status="pending"
    )
    
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    # TODO: 处理文档（文本提取、向量化等）
    # 这里可以添加文档解析和向量化逻辑
    # 例如使用 langchain 提取文本并存储到向量数据库
    # await process_and_vectorize_document(document.id, content)
    pass
    
    return {
        "status": "success",
        "message": "文档上传成功",
        "document": {
            "id": document.id,
            "fileName": document.file_name,
            "category": document.category
        }
    }


async def query_knowledge(
    db: AsyncSession, query_data: KnowledgeQuery
) -> Dict[str, Any]:
    """查询知识库"""
    
    # 使用 AI 生成答案
    llm = ChatOpenAI(
        model=settings.DEFAULT_AI_MODEL,
        temperature=0.7,
        api_key=settings.OPENAI_API_KEY
    )
    
    system_prompt = """你是一位知识渊博的助手。
根据提供的信息，组织清晰、准确的回答。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query_data.query)
    ]
    
    response = await llm.ainvoke(messages)
    
    return {
        "status": "success",
        "query": query_data.query,
        "answer": response.content,
        "sources": []
    }


async def list_documents(
    db: AsyncSession, category: str = None, limit: int = 20
) -> List[KnowledgeDocument]:
    """获取文档列表"""
    
    query = select(KnowledgeDocument)
    
    if category:
        query = query.where(KnowledgeDocument.category == category)
    
    query = query.limit(limit)
    result = await db.execute(query)
    
    return result.scalars().all()
