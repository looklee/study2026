"""
ComfyUI API路由
提供与ComfyUI集成的HTTP接口
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any

from app.services.comfyui_service import (
    get_comfyui_service, 
    ComfyUIService, 
    ComfyUIWorkflowRequest,
    ComfyUIQueueStatus
)


router = APIRouter(prefix="/comfyui", tags=["comfyui"])


@router.get("/health")
async def comfyui_health_check(
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    ComfyUI服务健康检查
    """
    try:
        is_available = await comfyui_service.ping()
        return {
            "status": "healthy" if is_available else "unavailable",
            "service": "comfyui",
            "connected": is_available
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ComfyUI健康检查失败: {str(e)}")


@router.get("/queue-status")
async def get_queue_status(
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    获取ComfyUI队列状态
    """
    try:
        status = await comfyui_service.get_queue_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取队列状态失败: {str(e)}")


@router.post("/interrupt")
async def interrupt_task(
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    中断当前任务
    """
    try:
        await comfyui_service.interrupt_current_task()
        return {"status": "success", "message": "中断请求已发送"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"中断任务失败: {str(e)}")


@router.get("/models")
async def get_installed_models(
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    获取已安装的模型列表
    """
    try:
        models = await comfyui_service.get_installed_models()
        return {"models": models, "count": len(models)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {str(e)}")


@router.get("/system-stats")
async def get_system_stats(
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    获取系统统计信息
    """
    try:
        stats = await comfyui_service.get_system_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统统计失败: {str(e)}")


@router.post("/generate")
async def generate_image_from_workflow(
    request: ComfyUIWorkflowRequest,
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    根据工作流生成图像
    """
    try:
        result = await comfyui_service.generate_image_from_workflow(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图像生成失败: {str(e)}")


@router.get("/history/{task_id}")
async def get_workflow_history(
    task_id: str,
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    获取特定任务的历史记录
    """
    try:
        history = await comfyui_service.get_workflow_history(task_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")


@router.get("/history")
async def get_all_workflow_history(
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    获取所有工作流历史记录
    """
    try:
        history = await comfyui_service.get_workflow_history()
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")


@router.post("/upload-image")
async def upload_image_endpoint(
    image_path: str,
    image_name: str = None,
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    上传图像到ComfyUI
    """
    try:
        result = await comfyui_service.upload_image(image_path, image_name)
        return {"status": "success", "filename": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传图像失败: {str(e)}")


# 快速生成端点
@router.post("/quick/text-to-image")
async def quick_text_to_image(
    prompt: str,
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    steps: int = 20,
    cfg: float = 8.0,
    seed: int = -1,
    model_name: str = "model.safetensors",
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    快速文本到图像生成
    """
    try:
        result = await comfyui_service.quick_text_to_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            steps=steps,
            cfg=cfg,
            seed=seed,
            model_name=model_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"快速文生图失败: {str(e)}")


@router.post("/quick/image-to-image")
async def quick_image_to_image(
    image_name: str,
    prompt: str,
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    steps: int = 20,
    cfg: float = 8.0,
    denoise: float = 0.7,
    seed: int = -1,
    model_name: str = "model.safetensors",
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    快速图像到图像生成
    """
    try:
        result = await comfyui_service.quick_image_to_image(
            image_name=image_name,
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            steps=steps,
            cfg=cfg,
            denoise=denoise,
            seed=seed,
            model_name=model_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"快速图生图失败: {str(e)}")


@router.post("/quick/inpainting")
async def quick_inpainting(
    image_name: str,
    mask_name: str,
    prompt: str,
    negative_prompt: str = "",
    steps: int = 20,
    cfg: float = 8.0,
    denoise: float = 0.7,
    seed: int = -1,
    model_name: str = "model.safetensors",
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    快速修复生成
    """
    try:
        result = await comfyui_service.quick_inpainting(
            image_name=image_name,
            mask_name=mask_name,
            prompt=prompt,
            negative_prompt=negative_prompt,
            steps=steps,
            cfg=cfg,
            denoise=denoise,
            seed=seed,
            model_name=model_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"快速修复生成失败: {str(e)}")


# 工作流模板端点
@router.get("/workflow-templates")
async def list_workflow_templates(
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    列出工作流模板
    """
    try:
        templates = await comfyui_service.list_workflow_templates()
        return {"templates": templates, "count": len(templates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工作流模板失败: {str(e)}")


@router.get("/workflow-templates/{template_name}")
async def get_workflow_template(
    template_name: str,
    comfyui_service: ComfyUIService = Depends(get_comfyui_service)
):
    """
    获取特定工作流模板
    """
    try:
        template = await comfyui_service.get_workflow_template(template_name)
        if not template:
            raise HTTPException(status_code=404, detail=f"工作流模板 '{template_name}' 不存在")
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工作流模板失败: {str(e)}")