# 工作流 API

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Workflow

router = APIRouter(prefix="/workflows", tags=["工作流"])


@router.get("", response_model=Dict[str, Any])
async def list_workflows(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的工作流列表"""
    result = await db.execute(
        select(Workflow).where(Workflow.user_id == current_user.id)
    )
    workflows = result.scalars().all()
    
    return {
        "workflows": [
            {
                "id": wf.id,
                "name": wf.name,
                "description": wf.description,
                "workflow_type": wf.workflow_type,
                "status": wf.status,
                "config": wf.config,
                "created_at": wf.created_at.isoformat() if wf.created_at else None
            }
            for wf in workflows
        ],
        "total": len(workflows)
    }


@router.post("/create", response_model=Dict[str, Any])
async def create_workflow(
    name: str,
    workflow_type: str,
    description: str = None,
    config: dict = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建工作流"""
    workflow = Workflow(
        user_id=current_user.id,
        name=name,
        description=description,
        workflow_type=workflow_type,
        config=config or {},
        status="draft"
    )
    
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    
    return {
        "status": "success",
        "message": "工作流创建成功",
        "workflow": {
            "id": workflow.id,
            "name": workflow.name,
            "type": workflow.workflow_type,
            "status": workflow.status
        }
    }


@router.get("/{workflow_id}", response_model=Dict[str, Any])
async def get_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取工作流详情"""
    result = await db.execute(
        select(Workflow).where(Workflow.id == workflow_id)
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow or workflow.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    return {
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "workflow_type": workflow.workflow_type,
        "status": workflow.status,
        "config": workflow.config,
        "created_at": workflow.created_at.isoformat() if workflow.created_at else None,
        "updated_at": workflow.updated_at.isoformat() if workflow.updated_at else None
    }


@router.put("/{workflow_id}", response_model=Dict[str, Any])
async def update_workflow(
    workflow_id: int,
    name: str = None,
    description: str = None,
    config: dict = None,
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新工作流"""
    result = await db.execute(
        select(Workflow).where(Workflow.id == workflow_id)
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow or workflow.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    if name:
        workflow.name = name
    if description:
        workflow.description = description
    if config:
        workflow.config = config
    if status:
        workflow.status = status
    
    await db.commit()
    await db.refresh(workflow)
    
    return {
        "status": "success",
        "message": "工作流更新成功",
        "workflow": {
            "id": workflow.id,
            "name": workflow.name,
            "status": workflow.status
        }
    }


@router.delete("/{workflow_id}", response_model=Dict[str, Any])
async def delete_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除工作流"""
    result = await db.execute(
        select(Workflow).where(Workflow.id == workflow_id)
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow or workflow.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    await db.delete(workflow)
    await db.commit()
    
    return {
        "status": "success",
        "message": "工作流已删除"
    }


@router.post("/{workflow_id}/execute", response_model=Dict[str, Any])
async def execute_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """执行工作流"""
    result = await db.execute(
        select(Workflow).where(Workflow.id == workflow_id)
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow or workflow.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    # TODO: 实现工作流执行引擎
    # 这里简化处理，仅更新状态

    from uuid import uuid4

    execution_id = f"exec_{workflow_id}_{uuid4().hex[:8]}_{int(datetime.now().timestamp())}"

    # TODO: 实际启动工作流执行过程
    # 这里应该启动后台任务来执行工作流
    # workflow_executor.start_execution(workflow_id, execution_id)

    workflow.status = "running"
    await db.commit()

    return {
        "status": "success",
        "message": "工作流开始执行",
        "workflow_id": workflow_id,
        "execution_id": execution_id
    }
