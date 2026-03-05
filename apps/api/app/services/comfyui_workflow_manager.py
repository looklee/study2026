"""
ComfyUI 工作流管理器
用于管理预定义的工作流模板和动态创建工作流
"""
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)


class ComfyUIWorkflowManager:
    """ComfyUI工作流管理器"""

    def __init__(self):
        self.workflow_templates_dir = Path("workflows/templates")
        self.workflow_templates_dir.mkdir(parents=True, exist_ok=True)
        self._load_default_workflows()

    def _load_default_workflows(self):
        """加载默认工作流模板"""
        # 创建一个简单的文本到图像工作流模板
        text_to_image_workflow = {
            "3": {
                "inputs": {
                    "seed": 12345,
                    "steps": 20,
                    "cfg": 8.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler",
                "_meta": {
                    "title": "KSampler"
                }
            },
            "4": {
                "inputs": {
                    "ckpt_name": "model.safetensors"
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "5": {
                "inputs": {
                    "width": 1024,
                    "height": 1024,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage",
                "_meta": {
                    "title": "Empty Latent Image"
                }
            },
            "6": {
                "inputs": {
                    "text": "masterpiece, best quality, ",
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "Positive Prompt"
                }
            },
            "7": {
                "inputs": {
                    "text": "bad hands, bad feet, low quality, low resolution",
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "Negative Prompt"
                }
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode",
                "_meta": {
                    "title": "VAE Decode"
                }
            },
            "9": {
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "Save Image"
                }
            }
        }

        # 保存默认工作流
        self.save_workflow_template("text_to_image_basic", text_to_image_workflow, "基本文生图工作流")

    def save_workflow_template(self, name: str, workflow: Dict[str, Any], description: str = ""):
        """保存工作流模板"""
        template_path = self.workflow_templates_dir / f"{name}.json"
        template_data = {
            "name": name,
            "description": description,
            "workflow": workflow,
            "created_at": str(uuid.uuid4()),
            "updated_at": str(uuid.uuid4())
        }
        
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"已保存工作流模板: {name}")

    def load_workflow_template(self, name: str) -> Optional[Dict[str, Any]]:
        """加载工作流模板"""
        template_path = self.workflow_templates_dir / f"{name}.json"
        if not template_path.exists():
            logger.warning(f"工作流模板不存在: {name}")
            return None
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_workflow_templates(self) -> List[Dict[str, str]]:
        """列出所有工作流模板"""
        templates = []
        for file_path in self.workflow_templates_dir.glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    templates.append({
                        "name": data.get("name", file_path.stem),
                        "description": data.get("description", ""),
                        "created_at": data.get("created_at", ""),
                        "updated_at": data.get("updated_at", "")
                    })
                except Exception as e:
                    logger.error(f"加载模板 {file_path.name} 失败: {e}")
        
        return templates

    def get_workflow_template(self, name: str) -> Optional[Dict[str, Any]]:
        """获取工作流模板"""
        template_path = self.workflow_templates_dir / f"{name}.json"
        if not template_path.exists():
            logger.warning(f"工作流模板不存在: {name}")
            return None
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def create_text_to_image_workflow(
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
        """创建文本到图像工作流"""
        if seed == -1:
            seed = int(uuid.uuid4().int & (1<<32)-1)  # 生成随机种子
        
        workflow = {
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler",
                "_meta": {"title": "KSampler"}
            },
            "4": {
                "inputs": {"ckpt_name": model_name},
                "class_type": "CheckpointLoaderSimple",
                "_meta": {"title": "Load Checkpoint"}
            },
            "5": {
                "inputs": {"width": width, "height": height, "batch_size": 1},
                "class_type": "EmptyLatentImage",
                "_meta": {"title": "Empty Latent Image"}
            },
            "6": {
                "inputs": {"text": f"masterpiece, best quality, {prompt}", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "Positive Prompt"}
            },
            "7": {
                "inputs": {"text": f"bad hands, bad feet, low quality, low resolution, {negative_prompt}", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "Negative Prompt"}
            },
            "8": {
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                "class_type": "VAEDecode",
                "_meta": {"title": "VAE Decode"}
            },
            "9": {
                "inputs": {"filename_prefix": "ComfyUI", "images": ["8", 0]},
                "class_type": "SaveImage",
                "_meta": {"title": "Save Image"}
            }
        }
        
        return workflow

    def create_image_to_image_workflow(
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
        """创建图像到图像工作流"""
        if seed == -1:
            seed = int(uuid.uuid4().int & (1<<32)-1)  # 生成随机种子
        
        workflow = {
            "1": {
                "inputs": {"image": image_name, "upload": "image"},
                "class_type": "LoadImage",
                "_meta": {"title": "Load Image"}
            },
            "2": {
                "inputs": {"pixels": ["1", 0], "vae": ["4", 2]},
                "class_type": "VAEEncode",
                "_meta": {"title": "VAE Encode"}
            },
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": denoise,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["2", 0]
                },
                "class_type": "KSampler",
                "_meta": {"title": "KSampler"}
            },
            "4": {
                "inputs": {"ckpt_name": model_name},
                "class_type": "CheckpointLoaderSimple",
                "_meta": {"title": "Load Checkpoint"}
            },
            "6": {
                "inputs": {"text": f"masterpiece, best quality, {prompt}", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "Positive Prompt"}
            },
            "7": {
                "inputs": {"text": f"bad hands, bad feet, low quality, low resolution, {negative_prompt}", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "Negative Prompt"}
            },
            "8": {
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                "class_type": "VAEDecode",
                "_meta": {"title": "VAE Decode"}
            },
            "9": {
                "inputs": {"filename_prefix": "ComfyUI", "images": ["8", 0]},
                "class_type": "SaveImage",
                "_meta": {"title": "Save Image"}
            }
        }
        
        return workflow

    def create_inpainting_workflow(
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
        """创建修复工作流"""
        if seed == -1:
            seed = int(uuid.uuid4().int & (1<<32)-1)  # 生成随机种子
        
        workflow = {
            "1": {
                "inputs": {"image": image_name, "upload": "image"},
                "class_type": "LoadImage",
                "_meta": {"title": "Load Image"}
            },
            "2": {
                "inputs": {"image": mask_name, "upload": "image"},
                "class_type": "LoadImageMask",
                "_meta": {"title": "Load Mask"}
            },
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": denoise,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["8", 0],
                    "mask": ["2", 0]
                },
                "class_type": "KSampler",
                "_meta": {"title": "KSampler"}
            },
            "4": {
                "inputs": {"ckpt_name": model_name},
                "class_type": "CheckpointLoaderSimple",
                "_meta": {"title": "Load Checkpoint"}
            },
            "6": {
                "inputs": {"text": f"masterpiece, best quality, {prompt}", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "Positive Prompt"}
            },
            "7": {
                "inputs": {"text": f"bad hands, bad feet, low quality, low resolution, {negative_prompt}", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "Negative Prompt"}
            },
            "8": {
                "inputs": {"pixels": ["1", 0], "vae": ["4", 2], "mask": ["2", 0]},
                "class_type": "VAEEncodeForInpaint",
                "_meta": {"title": "VAE Encode (for Inpainting)"}
            },
            "9": {
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                "class_type": "VAEDecode",
                "_meta": {"title": "VAE Decode"}
            },
            "10": {
                "inputs": {"filename_prefix": "ComfyUI", "images": ["9", 0]},
                "class_type": "SaveImage",
                "_meta": {"title": "Save Image"}
            }
        }
        
        return workflow


# 全局实例
_workflow_manager: Optional[ComfyUIWorkflowManager] = None


def get_workflow_manager() -> ComfyUIWorkflowManager:
    """获取工作流管理器实例"""
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = ComfyUIWorkflowManager()
    return _workflow_manager