"""
增强版去水印API路由
提供多种去水印方法的HTTP接口
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Dict, Any, List, Tuple
import tempfile
import os

from app.services.advanced_watermark_removal_service import get_watermark_removal_service, AdvancedWatermarkRemovalService


router = APIRouter(prefix="/advanced-watermark-removal", tags=["advanced-watermark-removal"])


@router.post("/by-coordinates")
async def remove_watermark_by_coordinates(
    input_file: UploadFile = File(...),
    output_path: str = "/tmp/output.jpg",  # 实际应用中应该使用更安全的路径
    coordinates: List[Tuple[int, int, int, int]] = [(100, 100, 50, 50)]  # 默认坐标
):
    """
    通过坐标去除水印
    coordinates: [(x, y, width, height), ...] 每个元组代表一个要去除的矩形区域
    """
    try:
        # 保存上传的文件到临时位置
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.filename)[1]) as temp_input:
            content = await input_file.read()
            temp_input.write(content)
            temp_input_path = temp_input.name

        # 准备输出路径
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 调用服务进行处理
        service = get_watermark_removal_service()
        result = await service.remove_watermark_by_coordinates(
            temp_input_path, output_path, coordinates
        )

        # 清理临时文件
        os.unlink(temp_input_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"去水印处理失败: {str(e)}")


@router.post("/by-color-range")
async def remove_watermark_by_color_range(
    input_file: UploadFile = File(...),
    output_path: str = "/tmp/output.jpg",
    lower_color: Tuple[int, int, int] = (0, 0, 0),  # 默认黑色
    upper_color: Tuple[int, int, int] = (50, 50, 50)  # 默认深灰色
):
    """
    通过颜色范围去除水印
    """
    try:
        # 保存上传的文件到临时位置
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.filename)[1]) as temp_input:
            content = await input_file.read()
            temp_input.write(content)
            temp_input_path = temp_input.name

        # 准备输出路径
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 调用服务进行处理
        service = get_watermark_removal_service()
        result = await service.remove_watermark_by_color_range(
            temp_input_path, output_path, lower_color, upper_color
        )

        # 清理临时文件
        os.unlink(temp_input_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"按颜色范围去水印失败: {str(e)}")


@router.post("/by-edge-detection")
async def remove_watermark_by_edge_detection(
    input_file: UploadFile = File(...)
):
    """
    通过边缘检测去除水印
    """
    try:
        # 保存上传的文件到临时位置
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.filename)[1]) as temp_input:
            content = await input_file.read()
            temp_input.write(content)
            temp_input_path = temp_input.name

        # 生成输出路径
        output_path = temp_input_path.replace(os.path.splitext(temp_input_path)[1], "_no_watermark.jpg")

        # 调用服务进行处理
        service = get_watermark_removal_service()
        result = await service.remove_watermark_by_edge_detection(
            temp_input_path, output_path
        )

        # 清理临时文件
        os.unlink(temp_input_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"按边缘检测去水印失败: {str(e)}")


@router.post("/detect-areas")
async def detect_watermark_areas(
    input_file: UploadFile = File(...)
):
    """
    检测图像中可能的水印区域
    """
    try:
        # 保存上传的文件到临时位置
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.filename)[1]) as temp_input:
            content = await input_file.read()
            temp_input.write(content)
            temp_input_path = temp_input.name

        # 调用服务进行检测
        service = get_watermark_removal_service()
        result = await service.detect_watermark_areas(temp_input_path)

        # 清理临时文件
        os.unlink(temp_input_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"水印区域检测失败: {str(e)}")


@router.post("/by-clicks")
async def remove_watermark_by_clicks(
    input_file: UploadFile = File(...),
    output_path: str = "/tmp/output.jpg",
    clicks: List[Tuple[int, int]] = [(100, 100)],  # 默认点击位置
    brush_radius: int = 20
):
    """
    根据点击位置去除水印
    clicks: [(x, y), ...] 点击位置列表
    """
    try:
        # 保存上传的文件到临时位置
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.filename)[1]) as temp_input:
            content = await input_file.read()
            temp_input.write(content)
            temp_input_path = temp_input.name

        # 准备输出路径
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 调用服务进行处理
        service = get_watermark_removal_service()
        result = await service.create_mask_from_clicks(
            temp_input_path, output_path, clicks, brush_radius
        )

        # 清理临时文件
        os.unlink(temp_input_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"按点击位置去水印失败: {str(e)}")


@router.post("/by-segmentation")
async def remove_watermark_by_segmentation(
    input_file: UploadFile = File(...)
):
    """
    使用图像分割技术去除水印
    """
    try:
        # 保存上传的文件到临时位置
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.filename)[1]) as temp_input:
            content = await input_file.read()
            temp_input.write(content)
            temp_input_path = temp_input.name

        # 生成输出路径
        output_path = temp_input_path.replace(os.path.splitext(temp_input_path)[1], "_segmented.jpg")

        # 调用服务进行处理
        service = get_watermark_removal_service()
        result = await service.remove_watermark_by_segmentation(
            temp_input_path, output_path
        )

        # 清理临时文件
        os.unlink(temp_input_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"按分割技术去水印失败: {str(e)}")


@router.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy", "service": "advanced-watermark-removal"}