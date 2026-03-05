# 社交功能 API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.services import social_service

router = APIRouter(prefix="/social", tags=["社交功能"])


# ==================== 好友系统 ====================

@router.post("/friends/request", response_model=Dict[str, Any])
async def send_friend_request(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发送好友请求"""
    try:
        await social_service.send_friend_request(db, current_user.id, friend_id)
        return {"status": "success", "message": "好友请求已发送"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/friends/accept", response_model=Dict[str, Any])
async def accept_friend_request(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """接受好友请求"""
    try:
        await social_service.accept_friend_request(db, current_user.id, friend_id)
        return {"status": "success", "message": "已接受好友请求"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/friends", response_model=Dict[str, Any])
async def get_friends(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取好友列表"""
    friends = await social_service.get_friends(db, current_user.id)
    return {"friends": friends, "total": len(friends)}


@router.delete("/friends/{friend_id}", response_model=Dict[str, Any])
async def remove_friend(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除好友"""
    success = await social_service.remove_friend(db, current_user.id, friend_id)
    if success:
        return {"status": "success", "message": "好友已删除"}
    raise HTTPException(status_code=404, detail="好友关系不存在")


# ==================== 关注系统 ====================

@router.post("/follow/{user_id}", response_model=Dict[str, Any])
async def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """关注用户"""
    try:
        await social_service.follow_user(db, current_user.id, user_id)
        return {"status": "success", "message": "已关注"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/follow/{user_id}", response_model=Dict[str, Any])
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消关注"""
    success = await social_service.unfollow_user(db, current_user.id, user_id)
    if success:
        return {"status": "success", "message": "已取消关注"}
    raise HTTPException(status_code=404, detail="关注关系不存在")


@router.get("/followers", response_model=Dict[str, Any])
async def get_followers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取粉丝列表"""
    follower_ids = await social_service.get_followers(db, current_user.id)
    return {"followers": follower_ids, "total": len(follower_ids)}


@router.get("/following", response_model=Dict[str, Any])
async def get_following(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取关注列表"""
    following_ids = await social_service.get_following(db, current_user.id)
    return {"following": following_ids, "total": len(following_ids)}


# ==================== 排行榜 ====================

@router.get("/leaderboard", response_model=Dict[str, Any])
async def get_leaderboard(
    type: str = "study_time",
    period: str = "all_time",
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """获取排行榜"""
    leaderboard = await social_service.get_leaderboard(db, type, period, limit)
    return {
        "type": type,
        "period": period,
        "leaderboard": leaderboard,
        "total": len(leaderboard)
    }


# ==================== 专注计时器 ====================

@router.post("/focus/start", response_model=Dict[str, Any])
async def start_focus_session(
    target_minutes: int = 25,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """开始专注会话"""
    session = await social_service.start_focus_session(db, current_user.id, target_minutes)
    return {
        "status": "success",
        "message": "专注会话已开始",
        "session": {
            "id": session.id,
            "target_minutes": session.target_minutes,
            "started_at": session.started_at.isoformat() if session.started_at else None
        }
    }


@router.post("/focus/complete", response_model=Dict[str, Any])
async def complete_focus_session(
    session_id: int,
    duration_minutes: int = None,
    notes: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """完成专注会话"""
    try:
        session = await social_service.complete_focus_session(db, session_id, duration_minutes, notes)
        # 奖励积分
        await social_service.add_points(db, current_user.id, 10, "focus", f"完成 {session.duration_minutes} 分钟专注")
        
        return {
            "status": "success",
            "message": "专注会话已完成",
            "session": {
                "id": session.id,
                "duration_minutes": session.duration_minutes,
                "points_earned": 10
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/focus/stats", response_model=Dict[str, Any])
async def get_focus_stats(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取专注统计"""
    stats = await social_service.get_focus_stats(db, current_user.id, days)
    return stats


# ==================== 学习笔记 ====================

@router.post("/notes", response_model=Dict[str, Any])
async def create_note(
    title: str,
    content: str,
    tags: str = None,
    path_id: int = None,
    is_public: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建笔记"""
    tags_list = tags.split(",") if tags else []
    note = await social_service.create_note(
        db, current_user.id, title, content, tags_list, path_id, is_public
    )
    return {
        "status": "success",
        "message": "笔记已创建",
        "note": {
            "id": note.id,
            "title": note.title
        }
    }


@router.get("/notes", response_model=Dict[str, Any])
async def get_notes(
    path_id: int = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取笔记列表"""
    notes = await social_service.get_notes(db, current_user.id, path_id, limit)
    return {"notes": notes, "total": len(notes)}


@router.put("/notes/{note_id}", response_model=Dict[str, Any])
async def update_note(
    note_id: int,
    title: str = None,
    content: str = None,
    tags: str = None,
    is_public: bool = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新笔记"""
    try:
        tags_list = tags.split(",") if tags else None
        note = await social_service.update_note(
            db, note_id, current_user.id, title, content, tags_list, is_public
        )
        return {"status": "success", "message": "笔记已更新"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/notes/{note_id}", response_model=Dict[str, Any])
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除笔记"""
    success = await social_service.delete_note(db, note_id, current_user.id)
    if success:
        return {"status": "success", "message": "笔记已删除"}
    raise HTTPException(status_code=404, detail="笔记不存在")


# ==================== 积分系统 ====================

@router.get("/points", response_model=Dict[str, Any])
async def get_points_info(
    current_user: User = Depends(get_current_user)
):
    """获取积分信息"""
    return {
        "user_id": current_user.id,
        "points": current_user.points or 0,
        "username": current_user.username
    }


@router.get("/points/history", response_model=Dict[str, Any])
async def get_points_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取积分历史"""
    history = await social_service.get_points_history(db, current_user.id, limit)
    return {"transactions": history, "total": len(history)}


# ==================== 商城系统 ====================

@router.get("/shop", response_model=Dict[str, Any])
async def get_shop_items(
    db: AsyncSession = Depends(get_db)
):
    """获取商城物品"""
    items = await social_service.get_shop_items(db)
    return {"items": items, "total": len(items)}


@router.post("/shop/purchase/{item_id}", response_model=Dict[str, Any])
async def purchase_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """购买物品"""
    try:
        inventory = await social_service.purchase_item(db, current_user.id, item_id)
        return {
            "status": "success",
            "message": "购买成功",
            "item": {
                "id": inventory.id,
                "quantity": inventory.quantity
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/inventory", response_model=Dict[str, Any])
async def get_inventory(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取背包物品"""
    items = await social_service.get_user_inventory(db, current_user.id)
    return {"items": items, "total": len(items)}
