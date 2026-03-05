"""
多媒体AI处理API路由
提供文生图、图生图、视频生成等功能的HTTP接口
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Dict, Any

from app.services.multimedia_service import get_multimedia_service, MultimediaAIService
from app.services.multimedia_service import (
    TextToImageRequest, 
    ImageToImageRequest, 
    VideoGenerationRequest, 
    ImageEditingRequest
)


router = APIRouter(prefix="/multimedia", tags=["multimedia"])


@router.post("/text-to-image")
async def text_to_image(
    request: TextToImageRequest,
    multimedia_service: MultimediaAIService = Depends(get_multimedia_service)
):
    """
    文生图功能
    """
    try:
        result = await multimedia_service.text_to_image(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文生图处理失败: {str(e)}")


@router.post("/image-to-image")
async def image_to_image(
    request: ImageToImageRequest,
    multimedia_service: MultimediaAIService = Depends(get_multimedia_service)
):
    """
    图生图功能
    """
    try:
        result = await multimedia_service.image_to_image(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图生图处理失败: {str(e)}")


@router.post("/generate-video")
async def generate_video(
    request: VideoGenerationRequest,
    multimedia_service: MultimediaAIService = Depends(get_multimedia_service)
):
    """
    视频生成功能
    """
    try:
        result = await multimedia_service.generate_video(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"视频生成失败: {str(e)}")


@router.post("/edit-image")
async def edit_image(
    request: ImageEditingRequest,
    multimedia_service: MultimediaAIService = Depends(get_multimedia_service)
):
    """
    图片编辑功能
    """
    try:
        result = await multimedia_service.edit_image(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片编辑失败: {str(e)}")


@router.get("/styles")
async def get_supported_styles(
    multimedia_service: MultimediaAIService = Depends(get_multimedia_service)
):
    """
    获取支持的样式列表
    """
    try:
        styles = await multimedia_service.get_supported_styles()
        return {"styles": styles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取样式列表失败: {str(e)}")


@router.get("/job-status/{job_id}")
async def get_job_status(
    job_id: str,
    multimedia_service: MultimediaAIService = Depends(get_multimedia_service)
):
    """
    获取任务状态
    """
    try:
        status = await multimedia_service.get_job_status(job_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务状态失败: {str(e)}")


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片
    """
    try:
        # 实现图片上传逻辑
        # 这里简化处理，仅返回文件信息
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file.size,
            "upload_status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片上传失败: {str(e)}")


@router.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy", "service": "multimedia-ai"}