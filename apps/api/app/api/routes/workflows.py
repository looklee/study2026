# 工作流执行 API 端点

from fastapi import APIRouter
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import datetime

router = APIRouter()

class WorkflowExecuteRequest(BaseModel):
    """工作流执行请求"""
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    logic: str = "AND"
    input_data: Optional[Dict[str, Any]] = None

@router.post("/api/v1/workflows/execute")
async def execute_workflow(request: WorkflowExecuteRequest):
    """执行工作流"""
    from app.workflow_engine import workflow_engine
    
    workflow_id = f"workflow_{datetime.datetime.utcnow().timestamp()}"
    
    execution = await workflow_engine.execute_workflow(
        workflow_id=workflow_id,
        nodes=request.nodes,
        edges=request.edges,
        logic=request.logic,
        input_data=request.input_data
    )
    
    return {
        "status": "success",
        "execution_id": execution["execution_id"],
        "workflow_id": execution["workflow_id"],
        "started_at": execution["started_at"],
        "nodes_executed": len(execution["nodes"]),
        "result": execution
    }

@router.get("/api/v1/workflows/executions/{execution_id}")
async def get_execution_status(execution_id: str):
    """获取执行状态"""
    from app.workflow_engine import workflow_engine
    
    execution = workflow_engine.get_execution_status(execution_id)
    
    if not execution:
        return {"status": "error", "message": "未找到执行记录"}
    
    return {
        "status": "success",
        "execution": execution
    }

@router.get("/api/v1/workflows/{workflow_id}/executions")
async def get_workflow_executions(workflow_id: str):
    """获取工作流执行历史"""
    from app.workflow_engine import workflow_engine
    
    executions = workflow_engine.get_workflow_executions(workflow_id)
    
    return {
        "status": "success",
        "workflow_id": workflow_id,
        "executions": executions
    }
