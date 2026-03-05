"""
OpenClaw服务集成测试
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.services.openclaw_service import OpenClawService, OpenClawConfig


@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)


@pytest.mark.asyncio
async def test_openclaw_process_request(client):
    """测试OpenClaw处理请求功能"""
    # 测试请求数据
    test_data = {
        "input_text": "Hello, OpenClaw!",
        "context": {"user_id": "test_user", "session_id": "test_session"}
    }
    
    response = client.post("/openclaw/process", json=test_data)
    
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    assert "OpenClaw processed" in result["response"]
    assert result["context"] == test_data["context"]


@pytest.mark.asyncio
async def test_openclaw_execute_skill(client):
    """测试OpenClaw执行技能功能"""
    test_data = {
        "skill_name": "web_search",
        "params": {"query": "Python programming"}
    }
    
    response = client.post("/openclaw/execute-skill", json=test_data)
    
    assert response.status_code == 200
    result = response.json()
    assert result["skill"] == test_data["skill_name"]
    assert result["params"] == test_data["params"]
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_openclaw_get_skills(client):
    """测试获取可用技能列表"""
    response = client.get("/openclaw/skills")
    
    assert response.status_code == 200
    result = response.json()
    assert "skills" in result
    assert isinstance(result["skills"], list)
    assert len(result["skills"]) > 0


@pytest.mark.asyncio
async def test_openclaw_chat_with_memory(client):
    """测试带记忆的对话功能"""
    test_data = {
        "message": "Tell me about Python",
        "conversation_id": "test_conv_123"
    }
    
    response = client.post("/openclaw/chat", json=test_data)
    
    assert response.status_code == 200
    result = response.json()
    assert "reply" in result
    assert "conversation_id" in result
    assert result["memory_updated"] is True


@pytest.mark.asyncio
async def test_openclaw_health_check(client):
    """测试健康检查"""
    response = client.get("/openclaw/health")
    
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "healthy"
    assert result["service"] == "openclaw"


@pytest.mark.asyncio
async def test_openclaw_service_initialization():
    """测试OpenClaw服务初始化"""
    config = OpenClawConfig(model="gpt-3.5-turbo")
    service = OpenClawService(config)
    
    # 测试初始化
    await service.initialize()
    assert service.initialized is True


@pytest.mark.asyncio
async def test_openclaw_service_process_request():
    """测试OpenClaw服务处理请求"""
    config = OpenClawConfig(model="gpt-3.5-turbo")
    service = OpenClawService(config)
    
    result = await service.process_request("Test input", {"key": "value"})
    
    assert "response" in result
    assert "context" in result
    assert "metadata" in result
    assert result["context"] == {"key": "value"}