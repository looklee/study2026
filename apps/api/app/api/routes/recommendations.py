from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import RecommendationRequest, RecommendationResponse
from app.services import recommendation_service

router = APIRouter()


@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    """获取推荐内容"""
    recommendations = await recommendation_service.get_recommendations(db, request)
    return recommendations


@router.get("/trending")
async def get_trending_topics(limit: int = 10):
    """获取热门主题"""
    topics = [
        "llm", "transformer", "diffusion", "rag", "agent",
        "fine-tuning", "prompt-engineering", "vector-database",
        "machine-learning", "deep-learning"
    ]
    return {"trending": topics[:limit]}
