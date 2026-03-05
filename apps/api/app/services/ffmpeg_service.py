"""
FFmpeg 服务类
提供视频和图像处理功能，包括去水印、格式转换等
"""
import asyncio
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from PIL import Image
import cv2
import numpy as np

logger = logging.getLogger(__name__)


class FFmpegService:
    """FFmpeg服务类"""

    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg not found. Please install FFmpeg and ensure it's in your PATH.")
        logger.info(f"FFmpeg found at: {self.ffmpeg_path}")

    def _find_ffmpeg(self) -> Optional[str]:
        """查找FFmpeg可执行文件"""
        # 尝试多个可能的位置
        possible_paths = [
            "ffmpeg",
            "ffmpeg.exe",
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "/opt/homebrew/bin/ffmpeg",
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "-version"], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE,
                                      timeout=5)
                if result.returncode == 0:
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
        
        return None

    async def convert_video_format(self, input_path: str, output_path: str, format: str = "mp4") -> Dict[str, Any]:
        """转换视频格式"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_path,
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-strict", "experimental",
                output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"FFmpeg conversion failed: {stderr.decode()}")
            
            return {
                "status": "success",
                "output_path": output_path,
                "message": f"Video converted to {format} format successfully"
            }
        except Exception as e:
            logger.error(f"Video conversion failed: {e}")
            raise

    async def extract_frames(self, video_path: str, output_dir: str, fps: int = 1) -> Dict[str, Any]:
        """从视频中提取帧"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-vf", f"fps={fps}",
                os.path.join(output_dir, "frame_%04d.jpg")
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Frame extraction failed: {stderr.decode()}")
            
            # 计算提取的帧数
            frame_files = [f for f in os.listdir(output_dir) if f.startswith("frame_")]
            
            return {
                "status": "success",
                "frames_extracted": len(frame_files),
                "output_dir": output_dir,
                "message": f"Extracted {len(frame_files)} frames from video"
            }
        except Exception as e:
            logger.error(f"Frame extraction failed: {e}")
            raise

    async def add_watermark(self, input_path: str, watermark_path: str, output_path: str, 
                           position: str = "bottom-right") -> Dict[str, Any]:
        """给视频或图像添加水印"""
        try:
            # 确定输入类型
            input_ext = Path(input_path).suffix.lower()
            is_video = input_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            
            if is_video:
                # 视频添加水印
                positions = {
                    "top-left": "10:10",
                    "top-right": "main_w-overlay_w-10:10",
                    "bottom-left": "10:main_h-overlay_h-10",
                    "bottom-right": "main_w-overlay_w-10:main_h-overlay_h-10",
                    "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2"
                }
                
                pos = positions.get(position, positions["bottom-right"])
                
                cmd = [
                    self.ffmpeg_path,
                    "-i", input_path,
                    "-i", watermark_path,
                    "-filter_complex", f"overlay={pos}",
                    "-c:a", "copy",  # 保持音频不变
                    output_path
                ]
            else:
                # 图像添加水印
                # 使用临时文件进行处理
                temp_output = output_path + ".tmp"
                
                cmd = [
                    self.ffmpeg_path,
                    "-i", input_path,
                    "-i", watermark_path,
                    "-filter_complex", "overlay=main_w-overlay_w-10:main_h-overlay_h-10",
                    temp_output
                ]
                
                # 重命名临时文件
                os.rename(temp_output, output_path)
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Watermark addition failed: {stderr.decode()}")
            
            return {
                "status": "success",
                "output_path": output_path,
                "message": "Watermark added successfully"
            }
        except Exception as e:
            logger.error(f"Watermark addition failed: {e}")
            raise

    async def remove_watermark_by_area(self, input_path: str, output_path: str, 
                                      x: int, y: int, width: int, height: int) -> Dict[str, Any]:
        """通过指定区域去除水印"""
        try:
            # 确定输入类型
            input_ext = Path(input_path).suffix.lower()
            is_video = input_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            
            if is_video:
                # 视频去水印 - 使用delogo滤镜
                cmd = [
                    self.ffmpeg_path,
                    "-i", input_path,
                    "-vf", f"delogo=x={x}:y={y}:w={width}:h={height}:band=10",
                    "-c:a", "copy",  # 保持音频不变
                    output_path
                ]
            else:
                # 图像去水印 - 使用cv2进行图像修复
                return await self._remove_watermark_from_image(input_path, output_path, x, y, width, height)
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Watermark removal failed: {stderr.decode()}")
            
            return {
                "status": "success",
                "output_path": output_path,
                "message": "Watermark removed successfully"
            }
        except Exception as e:
            logger.error(f"Watermark removal failed: {e}")
            raise

    async def _remove_watermark_from_image(self, input_path: str, output_path: str, 
                                          x: int, y: int, width: int, height: int) -> Dict[str, Any]:
        """从图像中去除水印 - 使用OpenCV修复算法"""
        try:
            # 读取图像
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # 定义要去除的区域
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            mask[y:y+height, x:x+width] = 255
            
            # 使用OpenCV的修复算法
            # 注意：Telea算法通常效果更好，但需要OpenCV的contrib模块
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
                "message": "Watermark removed from image successfully"
            }
        except Exception as e:
            logger.error(f"Image watermark removal failed: {e}")
            raise

    async def crop_media(self, input_path: str, output_path: str, 
                         x: int, y: int, width: int, height: int) -> Dict[str, Any]:
        """裁剪视频或图像"""
        try:
            input_ext = Path(input_path).suffix.lower()
            is_video = input_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            
            if is_video:
                cmd = [
                    self.ffmpeg_path,
                    "-i", input_path,
                    "-vf", f"crop={width}:{height}:{x}:{y}",
                    "-c:a", "copy",  # 保持音频不变
                    output_path
                ]
            else:
                # 图像裁剪
                img = cv2.imread(input_path)
                cropped = img[y:y+height, x:x+width]
                cv2.imwrite(output_path, cropped)
                
                return {
                    "status": "success",
                    "output_path": output_path,
                    "message": "Image cropped successfully"
                }
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Crop failed: {stderr.decode()}")
            
            return {
                "status": "success",
                "output_path": output_path,
                "message": "Media cropped successfully"
            }
        except Exception as e:
            logger.error(f"Media crop failed: {e}")
            raise

    async def resize_media(self, input_path: str, output_path: str, 
                          width: int, height: int, preserve_aspect: bool = False) -> Dict[str, Any]:
        """调整视频或图像大小"""
        try:
            input_ext = Path(input_path).suffix.lower()
            is_video = input_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            
            if is_video:
                if preserve_aspect:
                    cmd = [
                        self.ffmpeg_path,
                        "-i", input_path,
                        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
                        "-c:a", "copy",
                        output_path
                    ]
                else:
                    cmd = [
                        self.ffmpeg_path,
                        "-i", input_path,
                        "-vf", f"scale={width}:{height}",
                        "-c:a", "copy",
                        output_path
                    ]
            else:
                # 图像调整大小
                img = cv2.imread(input_path)
                resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
                cv2.imwrite(output_path, resized)
                
                return {
                    "status": "success",
                    "output_path": output_path,
                    "message": "Image resized successfully"
                }
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Resize failed: {stderr.decode()}")
            
            return {
                "status": "success",
                "output_path": output_path,
                "message": "Media resized successfully"
            }
        except Exception as e:
            logger.error(f"Media resize failed: {e}")
            raise

    async def get_media_info(self, media_path: str) -> Dict[str, Any]:
        """获取媒体文件信息"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", media_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Getting media info failed: {stderr.decode()}")
            
            import json
            info = json.loads(stdout.decode())
            
            return {
                "status": "success",
                "info": info,
                "message": "Media info retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Getting media info failed: {e}")
            raise


# 全局实例
_ffmpeg_service: Optional[FFmpegService] = None


def get_ffmpeg_service() -> FFmpegService:
    """获取FFmpeg服务实例"""
    global _ffmpeg_service
    if _ffmpeg_service is None:
        _ffmpeg_service = FFmpegService()
    return _ffmpeg_service