"""
ComfyUI 集成服务
用于与本地部署的 ComfyUI 进行交互，执行图像生成任务
"""
import asyncio
import logging
import uuid
import aiohttp
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel
from app.core.config import settings
from app.services.comfyui_workflow_manager import get_workflow_manager

logger = logging.getLogger(__name__)


class ComfyUIWorkflowRequest(BaseModel):
    """ComfyUI工作流请求"""
    workflow_json: dict
    prompt_overrides: Optional[Dict[str, Any]] = {}
    output_format: str = "PNG"
    quality: int = 95


class ComfyUIQueueStatus(BaseModel):
    """ComfyUI队列状态"""
    queue_remaining: int


class ComfyUIService:
    """ComfyUI服务类"""

    def __init__(self):
        self.base_url = settings.COMFYUI_BASE_URL or "http://127.0.0.1:8188"
        self.timeout = aiohttp.ClientTimeout(total=300)  # 5分钟超时
        self.session = None

    async def get_session(self):
        """获取HTTP会话"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self.session

    async def close_session(self):
        """关闭HTTP会话"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def ping(self) -> bool:
        """检查ComfyUI服务是否可用"""
        try:
            session = await self.get_session()
            async with session.get(f"{self.base_url}/queue") as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"ComfyUI服务不可用: {e}")
            return False

    async def get_queue_status(self) -> ComfyUIQueueStatus:
        """获取队列状态"""
        try:
            session = await self.get_session()
            async with session.get(f"{self.base_url}/queue") as response:
                response.raise_for_status()
                data = await response.json()
                return ComfyUIQueueStatus(queue_remaining=len(data['queue_running']) + len(data['queue_pending']))
        except Exception as e:
            logger.error(f"获取队列状态失败: {e}")
            raise

    async def interrupt_current_task(self):
        """中断当前任务"""
        try:
            session = await self.get_session()
            async with session.post(f"{self.base_url}/interrupt") as response:
                response.raise_for_status()
                logger.info("已发送中断请求")
        except Exception as e:
            logger.error(f"中断任务失败: {e}")
            raise

    async def get_workflow_history(self, task_id: str = None) -> Dict[str, Any]:
        """获取工作流历史记录"""
        try:
            session = await self.get_session()
            url = f"{self.base_url}/history"
            if task_id:
                url += f"/{task_id}"
            
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"获取历史记录失败: {e}")
            raise

    async def upload_image(self, image_path: str, image_name: str = None) -> str:
        """上传图像到ComfyUI"""
        try:
            session = await self.get_session()
            if not image_name:
                image_name = Path(image_path).name
            
            with open(image_path, 'rb') as f:
                form_data = aiohttp.FormData()
                form_data.add_field('image', f, filename=image_name)
                
                async with session.post(f"{self.base_url}/upload/image", data=form_data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result['name']
        except Exception as e:
            logger.error(f"上传图像失败: {e}")
            raise

    async def queue_prompt(self, workflow_json: Dict[str, Any], prompt_overrides: Dict[str, Any] = None) -> Dict[str, Any]:
        """提交工作流提示到队列"""
        try:
            # 如果有覆盖参数，则更新工作流
            if prompt_overrides:
                workflow_json = self._apply_prompt_overrides(workflow_json, prompt_overrides)

            session = await self.get_session()
            payload = {
                "prompt": workflow_json,
                "client_id": str(uuid.uuid4())
            }

            async with session.post(f"{self.base_url}/prompt", json=payload) as response:
                response.raise_for_status()
                result = await response.json()
                
                logger.info(f"已提交工作流到队列: {result['prompt_id']}")
                return result
        except Exception as e:
            logger.error(f"提交工作流失败: {e}")
            raise

    def _apply_prompt_overrides(self, workflow: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        """应用提示词覆盖"""
        import copy
        workflow_copy = copy.deepcopy(workflow)
        
        for node_id, node_overrides in overrides.items():
            if node_id in workflow_copy:
                for param, value in node_overrides.items():
                    if param in workflow_copy[node_id]['inputs']:
                        workflow_copy[node_id]['inputs'][param] = value
        
        return workflow_copy

    async def poll_result(self, prompt_id: str, timeout: int = 300) -> Dict[str, Any]:
        """轮询结果直到生成完成"""
        start_time = datetime.now()
        
        while (datetime.now() - start_time).seconds < timeout:
            try:
                history = await self.get_workflow_history(prompt_id)
                
                if prompt_id in history:
                    outputs = history[prompt_id].get('outputs', {})
                    
                    # 查找图像输出
                    images = []
                    for node_output in outputs.values():
                        if 'images' in node_output:
                            for img in node_output['images']:
                                images.append({
                                    'filename': img['filename'],
                                    'subfolder': img.get('subfolder', ''),
                                    'type': img['type'],
                                    'url': f"{self.base_url}/view?filename={img['filename']}&subfolder={img.get('subfolder', '')}&type={img['type']}"
                                })
                    
                    if images:
                        return {
                            'status': 'completed',
                            'prompt_id': prompt_id,
                            'images': images,
                            'timestamp': datetime.now().isoformat()
                        }
                
                # 等待一段时间再检查
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"轮询结果时发生错误: {e}")
                await asyncio.sleep(2)
        
        # 超时情况
        return {
            'status': 'timeout',
            'prompt_id': prompt_id,
            'error': '生成超时',
            'timestamp': datetime.now().isoformat()
        }

    async def generate_image_from_workflow(self, request: ComfyUIWorkflowRequest) -> Dict[str, Any]:
        """根据工作流生成图像"""
        try:
            # 提交工作流到队列
            queue_result = await self.queue_prompt(
                request.workflow_json,
                request.prompt_overrides
            )
            
            prompt_id = queue_result['prompt_id']
            
            # 轮询结果
            result = await self.poll_result(prompt_id)
            
            return result
        except Exception as e:
            logger.error(f"生成图像失败: {e}")
            raise

    async def get_installed_models(self) -> List[str]:
        """获取已安装的模型列表"""
        try:
            session = await self.get_session()
            async with session.get(f"{self.base_url}/object_info") as response:
                response.raise_for_status()
                data = await response.json()
                
                # 提取模型名称
                models = set()
                for node_type, node_info in data.items():
                    if 'input' in node_info:
                        for input_name, input_info in node_info['input'].items():
                            if isinstance(input_info, list) and input_name.lower() in ['ckpt_name', 'model_name', 'vae_name']:
                                models.update(input_info)
                
                return sorted(list(models))
        except Exception as e:
            logger.error(f"获取模型列表失败: {e}")
            return []

    async def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        try:
            session = await self.get_session()
            async with session.get(f"{self.base_url}/system_stats") as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"获取系统统计失败: {e}")
            return {}

    # 工作流管理方法
    async def quick_text_to_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 20,
        cfg: float = 8.0,
        seed: int = -1,
        model_name: str = "model.safetensors"
    ) -> Dict[str, Any]:
        """快速文本到图像生成"""
        workflow_manager = get_workflow_manager()
        workflow = workflow_manager.create_text_to_image_workflow(
            prompt, negative_prompt, width, height, steps, cfg, seed, model_name
        )
        
        request = ComfyUIWorkflowRequest(workflow_json=workflow)
        return await self.generate_image_from_workflow(request)

    async def quick_image_to_image(
        self,
        image_name: str,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        cfg: float = 8.0,
        denoise: float = 0.7,
        seed: int = -1,
        model_name: str = "model.safetensors"
    ) -> Dict[str, Any]:
        """快速图像到图像生成"""
        workflow_manager = get_workflow_manager()
        workflow = workflow_manager.create_image_to_image_workflow(
            image_name, prompt, negative_prompt, width, height, steps, cfg, denoise, seed, model_name
        )
        
        request = ComfyUIWorkflowRequest(workflow_json=workflow)
        return await self.generate_image_from_workflow(request)

    async def quick_inpainting(
        self,
        image_name: str,
        mask_name: str,
        prompt: str,
        negative_prompt: str = "",
        steps: int = 20,
        cfg: float = 8.0,
        denoise: float = 0.7,
        seed: int = -1,
        model_name: str = "model.safetensors"
    ) -> Dict[str, Any]:
        """快速修复生成"""
        workflow_manager = get_workflow_manager()
        workflow = workflow_manager.create_inpainting_workflow(
            image_name, mask_name, prompt, negative_prompt, steps, cfg, denoise, seed, model_name
        )
        
        request = ComfyUIWorkflowRequest(workflow_json=workflow)
        return await self.generate_image_from_workflow(request)

    async def list_workflow_templates(self) -> List[Dict[str, str]]:
        """列出工作流模板"""
        workflow_manager = get_workflow_manager()
        return workflow_manager.list_workflow_templates()

    async def get_workflow_template(self, name: str) -> Optional[Dict[str, Any]]:
        """获取工作流模板"""
        workflow_manager = get_workflow_manager()
        return workflow_manager.load_workflow_template(name)


# 全局实例
_comfyui_service: Optional[ComfyUIService] = None


def get_comfyui_service() -> ComfyUIService:
    """获取ComfyUI服务实例"""
    global _comfyui_service
    if _comfyui_service is None:
        _comfyui_service = ComfyUIService()
    return _comfyui_service


async def initialize_comfyui_service():
    """初始化ComfyUI服务"""
    global _comfyui_service
    if _comfyui_service is None:
        _comfyui_service = ComfyUIService()
    
    # 测试连接
    if await _comfyui_service.ping():
        logger.info("✅ ComfyUI服务连接成功")
        return True
    else:
        logger.warning("⚠️ ComfyUI服务未连接，某些功能可能不可用")
        return False


async def shutdown_comfyui_service():
    """关闭ComfyUI服务"""
    global _comfyui_service
    if _comfyui_service:
        await _comfyui_service.close_session()