"""
图像处理模块，包含去水印和其他图像处理功能
"""

import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Optional
import requests
from urllib.parse import urlparse
import tempfile
import os


def download_image_from_url(url: str) -> Optional[np.ndarray]:
    """
    从URL下载图像
    """
    try:
        if url.startswith('data:image'):
            # 处理base64编码的图像数据
            header, encoded = url.split(',', 1)
            image_data = base64.b64decode(encoded)
            image = Image.open(io.BytesIO(image_data))
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            # 处理普通URL
            response = requests.get(url)
            response.raise_for_status()
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
    except Exception as e:
        print(f"下载图像失败: {str(e)}")
        return None


def remove_watermark_with_inpainting(image: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
    """
    使用图像修复技术去除水印
    如果没有提供mask，则尝试自动检测水印区域
    """
    if mask is None:
        # 自动检测水印区域（简化版本 - 实际应用中可能需要更复杂的检测算法）
        mask = detect_watermark_auto(image)
    
    # 使用cv2.inpaint进行图像修复
    # INPAINT_TELEA通常比INPAINT_NS效果更好
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    
    return result


def detect_watermark_auto(image: np.ndarray) -> np.ndarray:
    """
    自动检测水印区域（简化版本）
    实际应用中可能需要更复杂的算法
    """
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 应用阈值以突出可能的水印区域
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # 形态学操作以清理噪声
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # 扩大检测到的区域以确保覆盖整个水印
    kernel_large = np.ones((10,10), np.uint8)
    mask = cv2.dilate(thresh, kernel_large, iterations=1)
    
    # 确保mask是单通道的uint8类型
    mask = (mask / 255).astype(np.uint8)
    
    return mask


def encode_image_to_base64(image: np.ndarray) -> str:
    """
    将OpenCV图像编码为base64字符串
    """
    _, buffer = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    image_bytes = buffer.tobytes()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/jpeg;base64,{image_base64}"


def process_watermark_removal(image_url: str, mask_url: Optional[str] = None, technique: str = "auto") -> dict:
    """
    处理去水印的主要函数
    """
    # 下载原始图像
    original_image = download_image_from_url(image_url)
    if original_image is None:
        raise ValueError("无法下载原始图像")
    
    # 如果提供了mask URL，则下载mask
    mask = None
    if mask_url:
        mask_img = download_image_from_url(mask_url)
        if mask_img is not None:
            # 将mask转换为单通道灰度图
            mask = cv2.cvtColor(mask_img, cv2.COLOR_BGR2GRAY)
            # 二值化mask（将白色区域设为255，其他区域设为0）
            _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
            mask = mask.astype(np.uint8)
    
    # 根据选择的技术进行处理
    if technique == "inpainting":
        result_image = remove_watermark_with_inpainting(original_image, mask)
    elif technique == "detection":
        result_image = remove_watermark_with_inpainting(original_image, mask)
    else:  # auto
        result_image = remove_watermark_with_inpainting(original_image, mask)
    
    # 编码结果图像
    result_base64 = encode_image_to_base64(result_image)
    
    return {
        "original_shape": original_image.shape,
        "result_shape": result_image.shape,
        "result_image": result_base64,
        "technique_used": technique,
        "mask_used": mask is not None
    }


# 测试函数
def test_watermark_removal():
    """
    测试去水印功能
    注意：这只是一个示例，实际使用时需要替换为有效的图像URL
    """
    # 示例图像URL（实际使用时替换为有效URL）
    test_image_url = "https://example.com/test_image.jpg"
    
    try:
        result = process_watermark_removal(test_image_url)
        print("去水印处理成功!")
        print(f"原始尺寸: {result['original_shape']}")
        print(f"结果尺寸: {result['result_shape']}")
        return result
    except Exception as e:
        print(f"去水印处理失败: {str(e)}")
        return None


if __name__ == "__main__":
    test_watermark_removal()