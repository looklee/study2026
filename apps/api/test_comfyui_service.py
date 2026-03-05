"""
ComfyUI 服务测试脚本
用于验证 ComfyUI 集成服务的基本功能
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.comfyui_service import get_comfyui_service
from app.services.comfyui_workflow_manager import get_workflow_manager


async def test_comfyui_connection():
    """测试 ComfyUI 连接"""
    print("[TEST] 测试 ComfyUI 连接...")
    
    comfyui_service = get_comfyui_service()
    
    try:
        is_connected = await comfyui_service.ping()
        if is_connected:
            print("[SUCCESS] ComfyUI 服务连接成功!")
        else:
            print("[ERROR] ComfyUI 服务未连接")
            print("[INFO] 提示: 请确保 ComfyUI 在 http://127.0.0.1:8188 上运行")
        return is_connected
    except Exception as e:
        print(f"[ERROR] 连接测试失败: {e}")
        return False


async def test_get_models():
    """测试获取模型列表"""
    print("\n[TEST] 测试获取模型列表...")
    
    comfyui_service = get_comfyui_service()
    
    try:
        models = await comfyui_service.get_installed_models()
        print(f"[SUCCESS] 找到 {len(models)} 个模型:")
        for model in models[:5]:  # 只显示前5个
            print(f"   - {model}")
        if len(models) > 5:
            print(f"   ... 还有 {len(models) - 5} 个模型")
        return True
    except Exception as e:
        print(f"[ERROR] 获取模型列表失败: {e}")
        return False


async def test_get_queue_status():
    """测试获取队列状态"""
    print("\n[TEST] 测试获取队列状态...")
    
    comfyui_service = get_comfyui_service()
    
    try:
        status = await comfyui_service.get_queue_status()
        print(f"[SUCCESS] 队列状态: 剩余 {status.queue_remaining} 个任务")
        return True
    except Exception as e:
        print(f"[ERROR] 获取队列状态失败: {e}")
        return False


def test_workflow_manager():
    """测试工作流管理器"""
    print("\n[TEST] 测试工作流管理器...")
    
    try:
        workflow_manager = get_workflow_manager()
        
        # 列出模板
        templates = workflow_manager.list_workflow_templates()
        print(f"[SUCCESS] 找到 {len(templates)} 个工作流模板:")
        for template in templates:
            print(f"   - {template['name']}: {template['description']}")
        
        # 创建一个基本的文本到图像工作流
        workflow = workflow_manager.create_text_to_image_workflow(
            prompt="a beautiful landscape",
            width=512,
            height=512
        )
        print(f"[SUCCESS] 成功创建文本到图像工作流，包含 {len(workflow)} 个节点")
        
        return True
    except Exception as e:
        print(f"[ERROR] 工作流管理器测试失败: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("开始 ComfyUI 服务测试...\n")
    
    tests = [
        test_comfyui_connection,
        test_get_models,
        test_get_queue_status,
        test_workflow_manager
    ]
    
    results = []
    for test in tests:
        if test.__name__ == 'test_workflow_manager':
            results.append(test())
        else:
            results.append(await test())
    
    print(f"\n[SUMMARY] 测试结果: {sum(results)}/{len(results)} 项测试通过")
    
    if all(results):
        print("[SUCCESS] 所有测试都通过了!")
    else:
        print("[WARNING] 部分测试失败，请检查配置")
    
    # 关闭服务
    comfyui_service = get_comfyui_service()
    await comfyui_service.close_session()


if __name__ == "__main__":
    asyncio.run(run_all_tests())