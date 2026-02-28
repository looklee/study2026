# 知识库 API 端点

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import datetime

router = APIRouter()

class KnowledgeQuery(BaseModel):
    """知识库查询请求"""
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = 10

class DocumentUpload(BaseModel):
    """文档上传请求"""
    file_name: str
    content: str
    category: str = "general"
    tags: List[str] = []

@router.get("/api/v1/knowledge/stats")
async def get_knowledge_stats():
    """获取知识库统计"""
    from app.knowledge_engine import knowledge_engine
    
    stats = knowledge_engine.get_stats()
    return {
        "status": "success",
        "stats": stats
    }

@router.get("/api/v1/knowledge/categories")
async def get_categories():
    """获取所有分类"""
    from app.knowledge_engine import knowledge_engine
    
    categories = knowledge_engine.get_categories()
    return {
        "status": "success",
        "categories": categories
    }

@router.get("/api/v1/knowledge/documents")
async def list_documents(category: Optional[str] = None, limit: int = 20):
    """列出文档"""
    from app.knowledge_engine import knowledge_engine
    
    docs = knowledge_engine.list_documents(category, limit)
    return {
        "status": "success",
        "documents": docs
    }

@router.get("/api/v1/knowledge/documents/{doc_id}")
async def get_document(doc_id: str):
    """获取文档详情"""
    from app.knowledge_engine import knowledge_engine
    
    doc = knowledge_engine.get_document(doc_id)
    if not doc:
        return {"status": "error", "message": "文档不存在"}
    
    return {
        "status": "success",
        "document": doc
    }

@router.post("/api/v1/knowledge/documents")
async def create_document(doc_data: DocumentUpload):
    """创建文档"""
    from app.knowledge_engine import knowledge_engine
    
    result = await knowledge_engine.upload_document({
        "file_name": doc_data.file_name,
        "content": doc_data.content,
        "category": doc_data.category,
        "tags": doc_data.tags,
        "mime_type": "text/plain",
        "file_size": len(doc_data.content)
    })
    
    return result

@router.post("/api/v1/knowledge/search")
async def search_knowledge(query_data: KnowledgeQuery):
    """搜索知识库"""
    from app.knowledge_engine import knowledge_engine
    
    result = await knowledge_engine.search_documents(
        query=query_data.query,
        filters=query_data.filters,
        limit=query_data.limit
    )
    
    return result

@router.post("/api/v1/knowledge/rag-query")
async def rag_query(query_data: KnowledgeQuery):
    """RAG 检索增强查询"""
    from app.knowledge_engine import knowledge_engine
    
    result = await knowledge_engine.rag_query(
        query=query_data.query,
        context_limit=query_data.limit
    )
    
    return result

@router.delete("/api/v1/knowledge/documents/{doc_id}")
async def delete_document(doc_id: str):
    """删除文档"""
    from app.knowledge_engine import knowledge_engine
    
    result = knowledge_engine.delete_document(doc_id)
    return result
