# RAG 向量检索服务

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np


class VectorStore:
    """简易向量存储 (使用 NumPy + 余弦相似度)"""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or "./vector_store"
        self.vectors = {}  # {doc_id: {"vector": np.array, "metadata": dict}}
        self._load()
    
    def _load(self):
        """加载向量存储"""
        path = Path(self.storage_path)
        if path.exists():
            # 简化：实际应该从文件加载
            pass
    
    def _save(self):
        """保存向量存储"""
        path = Path(self.storage_path)
        path.mkdir(parents=True, exist_ok=True)
        # 简化：实际应该保存到文件
    
    def add_vector(self, doc_id: str, vector: np.ndarray, metadata: Dict[str, Any]):
        """添加向量"""
        self.vectors[doc_id] = {
            "vector": vector,
            "metadata": metadata
        }
        self._save()
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """相似度搜索"""
        if not self.vectors:
            return []
        
        # 计算余弦相似度
        scores = []
        for doc_id, data in self.vectors.items():
            doc_vector = data["vector"]
            similarity = cosine_similarity(query_vector, doc_vector)
            scores.append({
                "doc_id": doc_id,
                "score": float(similarity),
                "metadata": data["metadata"]
            })
        
        # 排序并返回 top_k
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """计算余弦相似度"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


async def generate_embedding(text: str, model: str = "default") -> np.ndarray:
    """
    生成文本向量
    
    支持:
    - OpenAI embeddings
    - Sentence Transformers
    - 本地简易模型
    """
    # 简化实现：返回随机向量 (实际应该调用 embedding API)
    # 生产环境应该使用:
    # 1. OpenAI: openai.Embedding.create
    # 2. Sentence Transformers: SentenceTransformer(model).encode(text)
    # 3. 本地模型：text2vec, m3e 等
    
    embedding_dim = 768
    # 使用文本的 hash 生成确定性向量 (仅用于演示)
    np.random.seed(hash(text) % (2**32))
    vector = np.random.randn(embedding_dim).astype(np.float32)
    vector = vector / np.linalg.norm(vector)  # 归一化
    
    return vector


async def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """文本分块"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # 尝试在句子边界处切断
        if end < len(text):
            for sep in [". ", "。", "! ", "!", "? ", "？", "\n"]:
                last_sep = chunk.rfind(sep)
                if last_sep > chunk_size // 2:
                    chunk = chunk[:start + last_sep + len(sep)]
                    break
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks


class RAGService:
    """RAG 检索服务"""
    
    def __init__(self, db: AsyncSession = None):
        self.db = db
        self.vector_store = VectorStore()
    
    async def index_document(
        self,
        doc_id: str,
        text: str,
        metadata: Dict[str, Any]
    ):
        """索引文档"""
        # 分块
        chunks = await chunk_text(text)
        
        # 为每个 chunk 生成向量并存储
        for i, chunk in enumerate(chunks):
            embedding = await generate_embedding(chunk)
            
            chunk_metadata = {
                **metadata,
                "chunk_id": i,
                "total_chunks": len(chunks),
                "text": chunk  # 存储原始文本
            }
            
            self.vector_store.add_vector(
                f"{doc_id}_chunk_{i}",
                embedding,
                chunk_metadata
            )
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """检索相关文档"""
        # 生成查询向量
        query_vector = await generate_embedding(query)
        
        # 搜索
        results = self.vector_store.search(query_vector, top_k * 2)
        
        # 应用过滤器
        if filters:
            filtered_results = []
            for result in results:
                metadata = result["metadata"]
                match = True
                for key, value in filters.items():
                    if metadata.get(key) != value:
                        match = False
                        break
                if match:
                    filtered_results.append(result)
            results = filtered_results
        
        return results[:top_k]
    
    async def answer_with_context(
        self,
        query: str,
        user_id: int = None
    ) -> Dict[str, Any]:
        """基于检索结果生成答案"""
        # 检索相关文档
        filters = {"user_id": user_id} if user_id else None
        results = await self.search(query, top_k=3, filters=filters)
        
        # 构建上下文
        context = ""
        for i, result in enumerate(results, 1):
            context += f"[资料{i}]: {result['metadata'].get('text', '')}\n\n"
        
        # 返回结果 (实际应该调用 LLM 生成答案)
        return {
            "query": query,
            "context": context,
            "sources": [
                {
                    "doc_id": r["doc_id"],
                    "score": r["score"],
                    "text": r["metadata"].get("text", "")[:200] + "..."
                }
                for r in results
            ],
            "answer": f"基于以下资料回答您的问题...\n\n{context}"
        }


# 全局实例
_rag_service: Optional[RAGService] = None


def get_rag_service(db: AsyncSession = None) -> RAGService:
    """获取 RAG 服务实例"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService(db)
    return _rag_service
