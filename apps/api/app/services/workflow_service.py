from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from app.models import Workflow, KnowledgeDocument
from app.schemas import WorkflowCreate
from datetime import datetime


async def create_workflow(
    db: AsyncSession, workflow_data: WorkflowCreate, user_id: int
) -> Workflow:
    """创建工作流"""
    
    workflow = Workflow(
        user_id=user_id,
        name=workflow_data.name,
        description=workflow_data.description,
        workflow_data={
            "nodes": [n.model_dump() for n in workflow_data.nodes],
            "connections": [c.model_dump() for c in workflow_data.connections]
        },
        status="active"
    )
    
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return workflow


async def list_workflows(db: AsyncSession, user_id: int) -> List[Workflow]:
    """获取工作流列表"""
    result = await db.execute(
        select(Workflow)
        .where(Workflow.user_id == user_id)
        .order_by(Workflow.created_at.desc())
    )
    return result.scalars().all()


async def get_workflow(db: AsyncSession, workflow_id: int) -> Workflow | None:
    """获取工作流详情"""
    result = await db.execute(
        select(Workflow).where(Workflow.id == workflow_id)
    )
    return result.scalar_one_or_none()


async def execute_workflow(
    db: AsyncSession, workflow_id: int, input_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """执行工作流"""
    
    workflow = await get_workflow(db, workflow_id)
    if not workflow:
        raise ValueError("工作流不存在")
    
    # 简单的执行逻辑 - 实际应该实现工作流引擎
    result = {
        "workflow_id": workflow_id,
        "executed_at": datetime.utcnow().isoformat(),
        "input": input_data,
        "output": {"status": "executed", "message": "工作流执行成功"}
    }
    
    # 更新执行统计
    workflow.execution_count += 1
    workflow.last_executed_at = datetime.utcnow()
    await db.commit()
    
    return result


async def delete_workflow(db: AsyncSession, workflow_id: int):
    """删除工作流"""
    workflow = await get_workflow(db, workflow_id)
    if workflow:
        await db.delete(workflow)
        await db.commit()
