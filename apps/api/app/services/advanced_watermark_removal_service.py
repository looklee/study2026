"""
增强版去水印服务
集成FFmpeg和OpenCV技术，提供多种去水印方法
"""
import asyncio
import logging
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw
import cv2
import numpy as np
from app.services.ffmpeg_service import get_ffmpeg_service

logger = logging.getLogger(__name__)


class AdvancedWatermarkRemovalService:
    """增强版去水印服务"""

    def __init__(self):
        self.ffmpeg_service = get_ffmpeg_service()

    async def remove_watermark_by_coordinates(
        self, 
        input_path: str, 
        output_path: str, 
        coordinates: List[Tuple[int, int, int, int]]
    ) -> Dict[str, Any]:
        """
        通过坐标去除水印
        coordinates: [(x, y, width, height), ...] 每个元组代表一个要去除的矩形区域
        """
        try:
            input_ext = Path(input_path).suffix.lower()
            is_video = input_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            
            if is_video:
                # 对于视频，我们逐个处理每个坐标区域
                # 这里简化处理，只处理第一个区域
                if coordinates:
                    x, y, w, h = coordinates[0]
                    return await self.ffmpeg_service.remove_watermark_by_area(
                        input_path, output_path, x, y, w, h
                    )
                else:
                    raise ValueError("No coordinates provided")
            else:
                # 对于图像，使用OpenCV进行修复
                return await self._remove_watermark_from_image_by_coords(
                    input_path, output_path, coordinates
                )
        except Exception as e:
            logger.error(f"Watermark removal by coordinates failed: {e}")
            raise

    async def _remove_watermark_from_image_by_coords(
        self, 
        input_path: str, 
        output_path: str, 
        coordinates: List[Tuple[int, int, int, int]]
    ) -> Dict[str, Any]:
        """从图像中通过坐标去除水印"""
        try:
            # 读取图像
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # 创建掩码
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            
            # 在掩码上标记要去除的区域
            for x, y, w, h in coordinates:
                mask[y:y+h, x:x+w] = 255
            
            # 使用OpenCV的修复算法
            try:
                # 尝试使用Telea算法
                result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
            except:
                # 如果Telea不可用，使用Navier-Stokes算法
                result = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
            
            # 保存结果
            cv2.imwrite(output_path, result)
            
            return {
                "status": "success",
                "output_path": output_path,
                "coordinates_processed": len(coordinates),
                "message": f"Watermark removed from {len(coordinates)} areas successfully"
            }
        except Exception as e:
            logger.error(f"Image watermark removal by coordinates failed: {e}")
            raise

    async def remove_watermark_by_color_range(
        self, 
        input_path: str, 
        output_path: str, 
        lower_color: Tuple[int, int, int], 
        upper_color: Tuple[int, int, int]
    ) -> Dict[str, Any]:
        """通过颜色范围去除水印"""
        try:
            # 读取图像
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # 转换到HSV色彩空间
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # 创建掩码
            mask = cv2.inRange(hsv, lower_color, upper_color)
            
            # 使用形态学操作清理掩码
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # 使用修复算法
            try:
                result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
            except:
                result = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
            
            # 保存结果
            cv2.imwrite(output_path, result)
            
            return {
                "status": "success",
                "output_path": output_path,
                "message": "Watermark removed by color range successfully"
            }
        except Exception as e:
            logger.error(f"Watermark removal by color range failed: {e}")
            raise

    async def remove_watermark_by_edge_detection(
        self, 
        input_path: str, 
        output_path: str
    ) -> Dict[str, Any]:
        """通过边缘检测去除水印（适用于边框类水印）"""
        try:
            # 读取图像
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # 转换为灰度图
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 应用高斯模糊
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 边缘检测
            edges = cv2.Canny(blurred, 50, 150)
            
            # 膨胀边缘以扩大水印区域
            kernel = np.ones((3,3), np.uint8)
            edges_dilated = cv2.dilate(edges, kernel, iterations=2)
            
            # 使用边缘作为掩码
            mask = edges_dilated
            
            # 使用修复算法
            try:
                result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
            except:
                result = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
            
            # 保存结果
            cv2.imwrite(output_path, result)
            
            return {
                "status": "success",
                "output_path": output_path,
                "message": "Watermark removed by edge detection successfully"
            }
        except Exception as e:
            logger.error(f"Watermark removal by edge detection failed: {e}")
            raise

    async def detect_watermark_areas(self, input_path: str) -> List[Dict[str, Any]]:
        """检测图像中可能的水印区域"""
        try:
            # 读取图像
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Could not read image")
            
            detected_areas = []
            
            # 方法1: 检测图像角落的高对比度区域（常见水印位置）
            h, w = img.shape[:2]
            corner_regions = [
                (0, 0, w//4, h//4),           # 左上角
                (w - w//4, 0, w//4, h//4),    # 右上角
                (0, h - h//4, w//4, h//4),    # 左下角
                (w - w//4, h - h//4, w//4, h//4)  # 右下角
            ]
            
            for i, (x, y, reg_w, reg_h) in enumerate(corner_regions):
                region = img[y:y+reg_h, x:x+reg_w]
                
                # 计算区域的平均亮度和对比度
                gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
                mean_brightness = np.mean(gray_region)
                std_deviation = np.std(gray_region)
                
                # 如果区域有较高的对比度，可能是水印
                if std_deviation > 30:  # 阈值可调整
                    detected_areas.append({
                        "region": f"corner_{i+1}",
                        "bbox": (x, y, reg_w, reg_h),
                        "confidence": min(std_deviation / 50.0, 1.0),  # 归一化置信度
                        "type": "potential_watermark"
                    })
            
            # 方法2: 检测重复图案（常见于版权水印）
            # 这里简化处理，实际应用中可能需要更复杂的算法
            
            return {
                "status": "success",
                "detected_areas": detected_areas,
                "total_detected": len(detected_areas),
                "message": f"Detected {len(detected_areas)} potential watermark areas"
            }
        except Exception as e:
            logger.error(f"Watermark detection failed: {e}")
            raise

    async def create_mask_from_clicks(
        self, 
        input_path: str, 
        output_path: str, 
        clicks: List[Tuple[int, int]], 
        brush_radius: int = 20
    ) -> Dict[str, Any]:
        """根据点击位置创建掩码并去除水印"""
        try:
            # 读取图像
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # 创建掩码
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            
            # 在点击位置绘制圆形区域
            for x, y in clicks:
                cv2.circle(mask, (x, y), brush_radius, (255, 255, 255), -1)
            
            # 使用修复算法
            try:
                result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
            except:
                result = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
            
            # 保存结果
            cv2.imwrite(output_path, result)
            
            return {
                "status": "success",
                "output_path": output_path,
                "clicks_processed": len(clicks),
                "message": f"Watermark removed based on {len(clicks)} click positions"
            }
        except Exception as e:
            logger.error(f"Watermark removal by clicks failed: {e}")
            raise

    async def remove_watermark_by_segmentation(
        self, 
        input_path: str, 
        output_path: str
    ) -> Dict[str, Any]:
        """使用图像分割技术去除水印"""
        try:
            # 读取图像
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # 使用GrabCut算法进行前景分割
            mask = np.zeros(img.shape[:2], np.uint8)
            
            # 定义矩形区域（这里假设水印在边缘）
            h, w = img.shape[:2]
            rect = (w//8, h//8, w - w//4, h - h//4)  # 中央区域作为前景
            
            # 初始化前景和背景模型
            fg_model = np.zeros((1, 65), np.float64)
            bg_model = np.zeros((1, 65), np.float64)
            
            # 应用GrabCut
            cv2.grabCut(img, mask, rect, bg_model, fg_model, 5, cv2.GC_INIT_WITH_RECT)
            
            # 修改掩码：0和2变为背景，1和3变为前景
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            
            # 反转掩码以获取可能的水印区域
            watermark_mask = 1 - mask2
            
            # 使用修复算法
            try:
                result = cv2.inpaint(img, watermark_mask, 3, cv2.INPAINT_TELEA)
            except:
                result = cv2.inpaint(img, watermark_mask, 3, cv2.INPAINT_NS)
            
            # 保存结果
            cv2.imwrite(output_path, result)
            
            return {
                "status": "success",
                "output_path": output_path,
                "message": "Watermark removed by segmentation successfully"
            }
        except Exception as e:
            logger.error(f"Watermark removal by segmentation failed: {e}")
            raise


# 全局实例
_watermark_removal_service: Optional[AdvancedWatermarkRemovalService] = None


def get_watermark_removal_service() -> AdvancedWatermarkRemovalService:
    """获取去水印服务实例"""
    global _watermark_removal_service
    if _watermark_removal_service is None:
        _watermark_removal_service = AdvancedWatermarkRemovalService()
    return _watermark_removal_service