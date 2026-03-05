# 知识库 API

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, KnowledgeDocument
from app.services.rag_service import get_rag_service
from app.services.file_storage import save_file, list_user_files, delete_file

router = APIRouter(prefix="/knowledge", tags=["知识库"])


@router.post("/upload", response_model=Dict[str, Any])
async def upload_document(
    file: UploadFile = File(...),
    category: str = "general",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """上传文档到知识库"""
    # 保存文件
    file_info = await save_file(file, current_user.id, category, db)
    
    # 提取文本并索引 (简化实现)
    from app.services.file_storage import extract_text_from_file
    text_content = await extract_text_from_file(file_info["file_path"])
    
    # 使用 RAG 服务索引
    rag_service = get_rag_service(db)
    await rag_service.index_document(
        doc_id=str(file_info["id"]),
        text=text_content,
        metadata={
            "user_id": current_user.id,
            "file_name": file_info["file_name"],
            "category": category
        }
    )
    
    return {
        "status": "success",
        "message": "文档上传并索引成功",
        "document": file_info
    }


@router.get("/documents", response_model=Dict[str, Any])
async def list_documents(
    category: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的文档列表"""
    query = select(KnowledgeDocument).where(KnowledgeDocument.user_id == current_user.id)
    
    if category:
        query = query.where(KnowledgeDocument.category == category)
    
    result = await db.execute(query.order_by(KnowledgeDocument.created_at.desc()))
    docs = result.scalars().all()
    
    return {
        "documents": [
            {
                "id": doc.id,
                "file_name": doc.file_name,
                "file_size": doc.file_size,
                "mime_type": doc.mime_type,
                "category": doc.category,
                "status": doc.status,
                "created_at": doc.created_at.isoformat() if doc.created_at else None
            }
            for doc in docs
        ],
        "total": len(docs)
    }


@router.post("/search", response_model=Dict[str, Any])
async def search_knowledge(
    query: str,
    top_k: int = 5,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """搜索知识库"""
    rag_service = get_rag_service(db)
    
    results = await rag_service.search(
        query=query,
        top_k=top_k,
        filters={"user_id": current_user.id}
    )
    
    return {
        "query": query,
        "results": [
            {
                "doc_id": r["doc_id"],
                "score": r["score"],
                "text": r["metadata"].get("text", "")[:300] + "...",
                "file_name": r["metadata"].get("file_name", "")
            }
            for r in results
        ],
        "total": len(results)
    }


@router.post("/query", response_model=Dict[str, Any])
async def query_knowledge(
    question: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """基于知识库问答"""
    rag_service = get_rag_service(db)
    
    response = await rag_service.answer_with_context(
        query=question,
        user_id=current_user.id
    )
    
    return response


@router.delete("/documents/{document_id}", response_model=Dict[str, Any])
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除文档"""
    success = await delete_file(document_id, current_user.id, db)
    if success:
        return {"status": "success", "message": "文档已删除"}
    else:
        raise HTTPException(status_code=404, detail="文档不存在或无权限")
