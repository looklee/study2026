from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from app.core.config import settings
from app.schemas import LearningPathGenerate
import json


class AIService:
    """AI 服务"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.DEFAULT_AI_MODEL,
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )
        self.parser = JsonOutputParser()
    
    async def generate_path_with_ai(self, path_data: LearningPathGenerate) -> dict:
        """使用 AI 生成学习路径"""
        
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
      "resources": [
        {
          "type": "video|article|course|project",
          "title": "资源标题",
          "url": "链接",
          "estimatedHours": 2
        }
      ],
      "milestone": "里程碑描述",
      "assessment": "评估方式"
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

当前水平：{path_data.currentLevel}
学习目标：{path_data.targetGoal}
每周可用时间：{path_data.availableHoursPerWeek} 小时
学习风格：{path_data.preferredLearningStyle}
已有经验：{', '.join(path_data.priorExperience) if path_data.priorExperience else '无'}
预算：{path_data.budget}
截止日期：{path_data.deadline if path_data.deadline else '无'}

请生成一份详细的学习路径。"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = await self.llm.ainvoke(messages)
        
        try:
            result = self.parser.parse(response.content)
            return result
        except Exception as e:
            # 如果解析失败，尝试手动解析 JSON
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"AI 响应解析失败：{e}")


# 全局 AI 服务实例
ai_service = AIService()


async def generate_path_with_ai(path_data: LearningPathGenerate) -> dict:
    """生成学习路径的便捷函数"""
    return await ai_service.generate_path_with_ai(path_data)
