from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Any, List, Optional
import httpx
import json

class QwenService:
    """通义千问 (Qwen) AI 服务"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or ""
        self.base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        
        # 使用 OpenAI 兼容接口
        self.llm = ChatOpenAI(
            model="qwen-plus",
            temperature=0.7,
            api_key=self.api_key,
            base_url=self.base_url
        )
        self.parser = JsonOutputParser()
    
    async def chat(self, message: str, system_prompt: str = None) -> str:
        """聊天对话"""
        
        if not system_prompt:
            system_prompt = """你是一位专业、耐心、友善的 AI 导师，专注于帮助学生掌握 AI 和机器学习知识。

你的特点：
1. 善于用简单易懂的语言解释复杂概念
2. 鼓励学生思考，而不是直接给出答案
3. 根据学生的水平调整讲解深度
4. 提供实用的代码示例和最佳实践
5. 指出常见错误和注意事项

请用中文回答，除非用户特别要求使用英文。"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=message)
        ]
        
        response = await self.llm.ainvoke(messages)
        return response.content
    
    async def generate_learning_path(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成学习路径"""
        
        system_prompt = """你是一位专业的 AI 学习路径规划专家。
根据学习者的背景和目标，生成详细的个性化学习路径。

输出 JSON 格式：
{
  "pathName": "路径名称",
  "description": "路径描述",
  "totalDuration": "总时长（如：12 周）",
  "phases": [
    {
      "phaseNumber": 1,
      "phaseName": "阶段名称",
      "duration": "持续时间",
      "objectives": ["目标 1", "目标 2"],
      "topics": ["主题 1", "主题 2"],
      "milestone": "里程碑描述",
      "status": "pending"
    }
  ],
  "weeklySchedule": {
    "monday": "学习内容",
    "wednesday": "学习内容",
    "weekend": "实践项目"
  },
  "tips": ["学习建议 1", "学习建议 2"]
}"""

        user_prompt = f"""请根据以下学习者信息生成学习路径：

当前水平：{user_data.get('currentLevel', 'beginner')}
学习目标：{user_data.get('targetGoal', '学习 AI')}
每周可用时间：{user_data.get('availableHoursPerWeek', 10)} 小时
学习风格：{user_data.get('preferredLearningStyle', 'mixed')}
已有经验：{', '.join(user_data.get('priorExperience', [])) or '无'}
预算：{user_data.get('budget', 'free')}

请生成一份详细的学习路径。"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        try:
            result = self.parser.parse(response.content)
            return result
        except Exception:
            # 尝试提取 JSON
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            # 返回默认结构
            return self._get_default_path(user_data)
    
    def _get_default_path(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """默认学习路径"""
        return {
            "pathName": f"{user_data.get('targetGoal', '学习 AI')}之路",
            "description": f"个性化定制：{user_data.get('targetGoal', '学习 AI')}",
            "totalDuration": "12 周",
            "phases": [
                {
                    "phaseNumber": 1,
                    "phaseName": "基础准备",
                    "duration": "2 周",
                    "objectives": ["掌握基础概念", "熟悉工具和环境"],
                    "topics": ["入门概念", "环境搭建", "Hello World"],
                    "milestone": "完成第一个小项目",
                    "status": "pending"
                },
                {
                    "phaseNumber": 2,
                    "phaseName": "核心知识",
                    "duration": "4 周",
                    "objectives": ["深入理解核心概念", "掌握常用技术"],
                    "topics": ["核心理论", "常用算法", "最佳实践"],
                    "milestone": "完成中等难度项目",
                    "status": "pending"
                },
                {
                    "phaseNumber": 3,
                    "phaseName": "进阶提升",
                    "duration": "4 周",
                    "objectives": ["学习高级主题", "实战演练"],
                    "topics": ["高级特性", "性能优化", "架构设计"],
                    "milestone": "完成综合项目",
                    "status": "pending"
                },
                {
                    "phaseNumber": 4,
                    "phaseName": "实战项目",
                    "duration": "2 周",
                    "objectives": ["独立完成项目"],
                    "topics": ["项目选题", "开发实施", "部署上线"],
                    "milestone": "完成毕业设计",
                    "status": "pending"
                }
            ],
            "weeklySchedule": {
                "monday": "理论学习 2 小时",
                "wednesday": "代码练习 2 小时",
                "weekend": "项目实践 4 小时"
            },
            "tips": ["每天坚持写学习笔记", "多动手实践", "参与社区讨论"]
        }
    
    async def recommend_tools(self, task: str) -> List[Dict[str, Any]]:
        """推荐 AI 工具"""
        
        prompt = f"""用户需要完成以下任务：{task}

请推荐 3-5 个最适合的 AI 工具，返回 JSON 格式：
[
  {
    "name": "工具名称",
    "url": "官网链接",
    "description": "简短描述",
    "reason": "推荐理由"
  }
]"""

        messages = [
            SystemMessage(content="你是一位 AI 工具专家，擅长根据任务推荐合适的 AI 工具。"),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        try:
            return self.parser.parse(response.content)
        except Exception:
            return []


class CodingPlanService:
    """Coding Plan API 服务"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or ""
        self.base_url = base_url or "https://api.codingplan.example.com"
        self.enabled = bool(self.api_key)
    
    async def generate_plan(self, language: str, level: str, duration: str, goal: str) -> Dict[str, Any]:
        """生成编程学习计划"""
        
        if not self.enabled:
            # 返回模拟数据
            return self._get_mock_plan(language, level, duration, goal)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/plans/generate",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "language": language,
                        "level": level,
                        "duration": duration,
                        "goal": goal
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return self._get_mock_plan(language, level, duration, goal)
        except Exception as e:
            print(f"Coding Plan API 错误：{e}")
            return self._get_mock_plan(language, level, duration, goal)
    
    def _get_mock_plan(self, language: str, level: str, duration: str, goal: str) -> Dict[str, Any]:
        """模拟编程学习计划"""
        return {
            "plan_id": f"plan_{language}_{level}",
            "language": language,
            "level": level,
            "duration": duration,
            "goal": goal,
            "phases": [
                {
                    "phase": 1,
                    "name": f"{language} 基础",
                    "duration": "2 周",
                    "topics": [
                        f"{language} 语法基础",
                        "变量和数据类型",
                        "控制流（条件/循环）",
                        "函数和模块"
                    ],
                    "resources": [
                        {
                            "title": f"{language} 官方教程",
                            "url": f"https://docs.python.org/3/tutorial/" if language == "Python" else "#",
                            "type": "documentation"
                        }
                    ],
                    "project": "编写一个简单的计算器"
                },
                {
                    "phase": 2,
                    "name": f"{language} 进阶",
                    "duration": "3 周",
                    "topics": [
                        "面向对象编程",
                        "异常处理",
                        "文件操作",
                        "常用标准库"
                    ],
                    "resources": [
                        {
                            "title": f"《流畅的{language}》",
                            "url": "#",
                            "type": "book"
                        }
                    ],
                    "project": "实现一个待办事项管理系统"
                },
                {
                    "phase": 3,
                    "name": f"{goal} 实战",
                    "duration": "3 周",
                    "topics": [
                        f"{goal} 相关框架",
                        "API 开发",
                        "数据库操作",
                        "部署上线"
                    ],
                    "resources": [
                        {
                            "title": f"{goal} 实战教程",
                            "url": "#",
                            "type": "course"
                        }
                    ],
                    "project": f"完成一个{goal}相关的项目"
                }
            ],
            "tips": [
                "每天至少编写 100 行代码",
                "多阅读优秀开源项目",
                "积极参与技术社区讨论",
                "定期复习和总结"
            ]
        }
    
    async def get_resources(self, topic: str) -> List[Dict[str, Any]]:
        """获取学习资源"""
        
        if not self.enabled:
            return [
                {
                    "title": f"{topic} 官方文档",
                    "url": "https://docs.python.org/",
                    "type": "documentation",
                    "level": "all"
                },
                {
                    "title": f"{topic} 入门教程",
                    "url": "#",
                    "type": "course",
                    "level": "beginner"
                },
                {
                    "title": f"{topic} 实战项目",
                    "url": "#",
                    "type": "project",
                    "level": "intermediate"
                }
            ]
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/resources",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    params={"topic": topic},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json().get("resources", [])
        except Exception:
            pass
        
        return []
    
    async def test_connection(self) -> Dict[str, Any]:
        """测试 API 连接"""
        
        if not self.enabled:
            return {
                "status": "not_configured",
                "message": "请先配置 API 密钥"
            }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/health",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    return {
                        "status": "connected",
                        "message": "连接成功",
                        "response_time": response.elapsed.total_seconds() * 1000
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status_code}"
                    }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


# 全局服务实例
_qwen_service: Optional[QwenService] = None
_coding_plan_service: Optional[CodingPlanService] = None


def get_qwen_service(api_key: str = None, base_url: str = None) -> QwenService:
    """获取 Qwen 服务实例"""
    global _qwen_service
    if _qwen_service is None or api_key:
        _qwen_service = QwenService(api_key, base_url)
    return _qwen_service


def get_coding_plan_service(api_key: str = None, base_url: str = None) -> CodingPlanService:
    """获取 Coding Plan 服务实例"""
    global _coding_plan_service
    if _coding_plan_service is None or api_key:
        _coding_plan_service = CodingPlanService(api_key, base_url)
    return _coding_plan_service
