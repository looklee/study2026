# 知识库管理引擎

from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import httpx
import json
import os

class KnowledgeEngine:
    """知识库引擎"""
    
    def __init__(self):
        self.documents = {}
        self.collections = {}
    
    async def upload_document(self, file_data: Dict[str, Any]) -> Dict:
        """上传文档"""
        doc_id = f"doc_{datetime.now().timestamp()}"
        
        document = {
            "doc_id": doc_id,
            "file_name": file_data.get("file_name", "unknown"),
            "file_size": file_data.get("file_size", 0),
            "mime_type": file_data.get("mime_type", "text/plain"),
            "category": file_data.get("category", "general"),
            "tags": file_data.get("tags", []),
            "content": file_data.get("content", ""),
            "chunks": [],
            "embeddings": [],
            "status": "processing",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 文本分块
        document["chunks"] = self._chunk_text(document["content"])
        
        # 模拟生成 embedding
        document["embeddings"] = [
            {"chunk_id": i, "embedding": [0.1] * 1536}
            for i in range(len(document["chunks"]))
        ]
        
        document["status"] = "processed"
        self.documents[doc_id] = document
        
        return {
            "status": "success",
            "doc_id": doc_id,
            "message": f"文档已上传：{file_data.get('file_name')}",
            "chunks_count": len(document["chunks"])
        }
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """文本分块"""
        if not text:
            return []
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append(chunk)
            start += chunk_size - overlap
        
        return chunks
    
    async def search_documents(self, query: str, filters: Optional[Dict] = None, limit: int = 10) -> Dict:
        """搜索文档"""
        results = []
        
        # 简单文本搜索
        for doc_id, doc in self.documents.items():
            if doc["status"] != "processed":
                continue
            
            # 应用过滤器
            if filters:
                if filters.get("category") and doc["category"] != filters["category"]:
                    continue
                if filters.get("tags"):
                    if not any(tag in doc["tags"] for tag in filters["tags"]):
                        continue
            
            # 计算相关性分数
            score = self._calculate_relevance(query, doc)
            
            if score > 0:
                results.append({
                    "doc_id": doc_id,
                    "file_name": doc["file_name"],
                    "category": doc["category"],
                    "tags": doc["tags"],
                    "score": score,
                    "snippet": doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"]
                })
        
        # 按分数排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "status": "success",
            "query": query,
            "total": len(results),
            "results": results[:limit]
        }
    
    def _calculate_relevance(self, query: str, document: Dict) -> float:
        """计算相关性分数"""
        score = 0.0
        query_lower = query.lower()
        
        # 标题匹配
        if query_lower in document["file_name"].lower():
            score += 10.0
        
        # 标签匹配
        for tag in document.get("tags", []):
            if query_lower in tag.lower():
                score += 5.0
        
        # 内容匹配
        content_lower = document.get("content", "").lower()
        if query_lower in content_lower:
            score += 3.0
        
        # 关键词匹配
        query_words = query_lower.split()
        for word in query_words:
            if word in content_lower:
                score += 0.5
        
        return score
    
    async def rag_query(self, query: str, context_limit: int = 3) -> Dict:
        """RAG 检索增强生成"""
        # 检索相关文档
        search_result = await self.search_documents(query, limit=context_limit)
        
        # 构建上下文
        context = []
        for i, result in enumerate(search_result["results"], 1):
            context.append(f"[来源{i}] {result['file_name']}: {result['snippet']}")
        
        return {
            "status": "success",
            "query": query,
            "context": "\n\n".join(context),
            "sources_count": len(search_result["results"]),
            "sources": search_result["results"]
        }
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """获取文档详情"""
        return self.documents.get(doc_id)
    
    def list_documents(self, category: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """列出文档"""
        docs = []
        for doc_id, doc in self.documents.items():
            if category and doc["category"] != category:
                continue
            docs.append({
                "doc_id": doc_id,
                "file_name": doc["file_name"],
                "category": doc["category"],
                "tags": doc["tags"],
                "status": doc["status"],
                "created_at": doc["created_at"],
                "chunks_count": len(doc.get("chunks", []))
            })
        
        return docs[:limit]
    
    def delete_document(self, doc_id: str) -> Dict:
        """删除文档"""
        if doc_id in self.documents:
            del self.documents[doc_id]
            return {"status": "success", "message": "文档已删除"}
        return {"status": "error", "message": "文档不存在"}
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set()
        for doc in self.documents.values():
            categories.add(doc["category"])
        return list(categories)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_docs = len(self.documents)
        total_chunks = sum(len(doc.get("chunks", [])) for doc in self.documents.values())
        
        by_category = {}
        by_status = {}
        
        for doc in self.documents.values():
            cat = doc["category"]
            status = doc["status"]
            by_category[cat] = by_category.get(cat, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "total_documents": total_docs,
            "total_chunks": total_chunks,
            "by_category": by_category,
            "by_status": by_status
        }

# 全局引擎实例
knowledge_engine = KnowledgeEngine()
