# 工作流执行引擎 - 增强版

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import httpx
import json
import random

class WorkflowEngine:
    """工作流执行引擎 - 增强版"""

    def __init__(self):
        self.executions = {}
        self.node_registry = {}
        self._register_default_nodes()

    def _register_default_nodes(self):
        """注册默认节点处理器"""
        self.node_handlers = {
            'trigger': self._execute_trigger,
            'action': self._execute_action,
            'condition': self._execute_condition,
            'api': self._execute_api,
            'llm': self._execute_llm,
            'data': self._execute_data,
            'learning': self._execute_learning,
            'notification': self._execute_notification
        }

    async def execute_workflow(self, workflow_id: str, nodes: List[Dict], edges: List[Dict],
                               logic: str = 'AND', input_data: Optional[Dict] = None) -> Dict:
        """执行工作流"""

        execution_id = f"exec_{workflow_id}_{datetime.now().timestamp()}"

        execution = {
            "execution_id": execution_id,
            "workflow_id": workflow_id,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "nodes": [],
            "edges": edges,
            "logic": logic,
            "input_data": input_data,
            "output": None,
            "error": None
        }

        self.executions[execution_id] = execution

        try:
            # 按顺序执行节点
            node_results = {}
            sorted_nodes = self._topological_sort(nodes, edges)

            for node in sorted_nodes:
                node_result = await self._execute_node(node, node_results, input_data)
                node_results[node["id"]] = node_result
                execution["nodes"].append({
                    "node_id": node["id"],
                    "node_type": node["type"],
                    "label": node["data"]["label"],
                    "status": "success" if node_result.get("success") else "error",
                    "result": node_result,
                    "executed_at": datetime.now().isoformat()
                })

                # 如果是 OR 逻辑，第一个成功就返回
                if logic == 'OR' and node_result.get("success"):
                    break

            execution["status"] = "success"
            execution["output"] = node_results
            execution["completed_at"] = datetime.now().isoformat()

        except Exception as e:
            execution["status"] = "error"
            execution["error"] = str(e)
            execution["completed_at"] = datetime.now().isoformat()

        return execution

    def _topological_sort(self, nodes: List[Dict], edges: List[Dict]) -> List[Dict]:
        """拓扑排序，确保节点按正确顺序执行"""
        # 构建邻接表和入度表
        graph = {node["id"]: [] for node in nodes}
        in_degree = {node["id"]: 0 for node in nodes}

        for edge in edges:
            source = edge["source"]
            target = edge["target"]
            if source in graph and target in graph:
                graph[source].append(target)
                in_degree[target] += 1

        # 找到所有入度为 0 的节点（起点）
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            node_id = queue.pop(0)
            node = next((n for n in nodes if n["id"] == node_id), None)
            if node:
                result.append(node)

            for neighbor in graph.get(node_id, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result

    async def _execute_node(self, node: Dict, previous_results: Dict, input_data: Optional[Dict]) -> Dict:
        """执行单个节点"""
        node_type = node.get("type")
        handler = self.node_handlers.get(node_type)
        
        if handler:
            return await handler(node, previous_results, input_data)
        else:
            return {"success": False, "error": f"未知节点类型：{node_type}"}

    # ==================== 触发器节点 ====================
    async def _execute_trigger(self, node: Dict, config: Dict, input_data: Optional[Dict]) -> Dict:
        """执行触发器节点"""
        label = node["data"].get("label", "触发器")
        node_config = node["data"].get("config", {})
        
        trigger_type = node_config.get("type", "manual")
        
        return {
            "success": True,
            "message": f"触发器已激活：{label}",
            "trigger_type": trigger_type,
            "input_data": input_data,
            "triggered_at": datetime.now().isoformat()
        }

    # ==================== 动作节点 ====================
    async def _execute_action(self, node: Dict, config: Dict, previous_results: Optional[Dict]) -> Dict:
        """执行动作节点"""
        label = node["data"].get("label", "动作")
        node_config = node["data"].get("config", {})
        action_type = node_config.get("type", "generic")

        if action_type == "email":
            return {
                "success": True,
                "message": f"邮件已发送：{label}",
                "template": node_config.get("template"),
                "sent_at": datetime.now().isoformat()
            }
        elif action_type == "notification":
            return {
                "success": True,
                "message": f"通知已发送：{label}",
                "channel": node_config.get("channel", "email"),
                "priority": node_config.get("priority", "normal"),
                "sent_at": datetime.now().isoformat()
            }
        elif action_type == "delay":
            delay_seconds = node_config.get("delay_seconds", 60)
            await asyncio.sleep(min(delay_seconds, 5))  # 模拟延迟，最多 5 秒
            return {
                "success": True,
                "message": f"延迟执行完成：{label}",
                "delayed_seconds": delay_seconds,
                "completed_at": datetime.now().isoformat()
            }
        elif action_type == "update_progress":
            return {
                "success": True,
                "message": f"进度已更新：{label}",
                "field": node_config.get("field"),
                "value": node_config.get("value"),
                "updated_at": datetime.now().isoformat()
            }
        elif action_type == "award_badge":
            return {
                "success": True,
                "message": f"徽章已颁发：{label}",
                "badge_id": node_config.get("badge_id"),
                "reason": node_config.get("reason"),
                "awarded_at": datetime.now().isoformat()
            }
        else:
            return {
                "success": True,
                "message": f"动作已执行：{label}",
                "executed_at": datetime.now().isoformat()
            }

    # ==================== 条件节点 ====================
    async def _execute_condition(self, node: Dict, config: Dict, previous_results: Optional[Dict]) -> Dict:
        """执行条件节点"""
        label = node["data"].get("label", "条件")
        node_config = node["data"].get("config", {})
        operator = node_config.get("operator", ">=")
        value = node_config.get("value", 0)
        field = node_config.get("field", "")

        # 获取前一个节点的结果
        prev_result = list(previous_results.values())[-1] if previous_results else {}
        actual_value = prev_result.get(field, 0) if field else 50  # 默认值

        # 条件判断
        condition_met = False
        if operator == ">=":
            condition_met = actual_value >= value
        elif operator == ">":
            condition_met = actual_value > value
        elif operator == "<=":
            condition_met = actual_value <= value
        elif operator == "<":
            condition_met = actual_value < value
        elif operator == "==":
            condition_met = actual_value == value
        elif operator == "!=":
            condition_met = actual_value != value
        elif operator == "contains":
            condition_met = str(value) in str(actual_value)
        elif operator == "changed":
            condition_met = True  # 检测变化

        return {
            "success": True,
            "condition_met": condition_met,
            "message": f"条件判断：{label} ({operator} {value})",
            "actual_value": actual_value,
            "result": condition_met
        }

    # ==================== API 节点 ====================
    async def _execute_api(self, node: Dict, config: Dict, previous_results: Optional[Dict]) -> Dict:
        """执行 API 节点"""
        label = node["data"].get("label", "API 请求")
        node_config = node["data"].get("config", {})
        method = node_config.get("method", "GET")
        endpoint = node_config.get("endpoint", "/api")
        url = node_config.get("url", f"http://localhost:8000{endpoint}")

        # 模拟 API 调用
        return {
            "success": True,
            "message": f"API 请求已发送：{label}",
            "method": method,
            "url": url,
            "response": {"status": "ok", "data": {}},
            "called_at": datetime.now().isoformat()
        }

    # ==================== LLM 节点 ====================
    async def _execute_llm(self, node: Dict, config: Dict, previous_results: Optional[Dict]) -> Dict:
        """执行 LLM 节点"""
        label = node["data"].get("label", "LLM 调用")
        node_config = node["data"].get("config", {})
        model = node_config.get("model", "qwen-plus")
        temperature = node_config.get("temperature", 0.7)
        max_tokens = node_config.get("max_tokens", 2000)

        # 模拟 LLM 调用
        llm_responses = {
            "summary": "这是一个自动生成的摘要内容...",
            "analysis": "根据分析，该内容呈现积极倾向...",
            "code": "def hello_world():\n    print('Hello, World!')",
            "translation": "This is the translated content...",
            "answer": "根据您的问题的详细回答..."
        }
        
        task_type = node_config.get("task_type", "generic")
        response_text = llm_responses.get(task_type, "LLM 已处理您的请求...")

        return {
            "success": True,
            "message": f"LLM 已调用：{label}",
            "model": model,
            "task_type": task_type,
            "response": response_text,
            "tokens_used": random.randint(50, 500),
            "temperature": temperature,
            "called_at": datetime.now().isoformat()
        }

    # ==================== 数据节点 ====================
    async def _execute_data(self, node: Dict, config: Dict, previous_results: Optional[Dict]) -> Dict:
        """执行数据节点"""
        label = node["data"].get("label", "数据操作")
        node_config = node["data"].get("config", {})
        table = node_config.get("table", "data")
        operation = node_config.get("operation", "insert")

        # 模拟数据操作
        return {
            "success": True,
            "message": f"数据操作完成：{label}",
            "table": table,
            "operation": operation,
            "rows_affected": random.randint(1, 10),
            "executed_at": datetime.now().isoformat()
        }

    # ==================== 学习相关节点 ====================
    async def _execute_learning(self, node: Dict, config: Dict, previous_results: Optional[Dict]) -> Dict:
        """执行学习相关节点"""
        label = node["data"].get("label", "学习操作")
        node_config = node["data"].get("config", {})
        operation_type = node_config.get("type", "generate_path")

        if operation_type == "generate_path":
            return {
                "success": True,
                "message": f"学习路径已生成：{label}",
                "goal": node_config.get("goal"),
                "duration_days": node_config.get("duration_days", 30),
                "difficulty": node_config.get("difficulty", "medium"),
                "path_id": f"path_{datetime.now().timestamp()}",
                "generated_at": datetime.now().isoformat()
            }
        elif operation_type == "recommend":
            return {
                "success": True,
                "message": f"资源推荐完成：{label}",
                "topic": node_config.get("topic"),
                "recommendations": [
                    {"id": 1, "title": "推荐资源 1", "type": "video"},
                    {"id": 2, "title": "推荐资源 2", "type": "article"}
                ],
                "recommended_at": datetime.now().isoformat()
            }
        elif operation_type == "check_progress":
            return {
                "success": True,
                "message": f"进度检查完成：{label}",
                "path_id": node_config.get("path_id"),
                "completion": random.randint(0, 100),
                "checked_at": datetime.now().isoformat()
            }
        elif operation_type == "quiz":
            return {
                "success": True,
                "message": f"测验完成：{label}",
                "quiz_id": node_config.get("quiz_id"),
                "score": random.randint(60, 100),
                "passed": True,
                "completed_at": datetime.now().isoformat()
            }
        else:
            return {
                "success": True,
                "message": f"学习操作完成：{label}",
                "executed_at": datetime.now().isoformat()
            }

    # ==================== 通知节点 ====================
    async def _execute_notification(self, node: Dict, config: Dict, previous_results: Optional[Dict]) -> Dict:
        """执行通知节点"""
        label = node["data"].get("label", "通知")
        node_config = node["data"].get("config", {})
        channel = node_config.get("channel", node_config.get("platform", "email"))

        if channel == "email":
            return {
                "success": True,
                "message": f"邮件通知已发送：{label}",
                "template": node_config.get("template"),
                "recipients": node_config.get("recipients", []),
                "sent_at": datetime.now().isoformat()
            }
        elif channel in ["dingtalk", "wecom"]:
            return {
                "success": True,
                "message": f"{channel}通知已发送：{label}",
                "webhook": node_config.get("webhook", "hidden"),
                "msgtype": node_config.get("msgtype", "text"),
                "sent_at": datetime.now().isoformat()
            }
        elif channel == "push":
            return {
                "success": True,
                "message": f"推送通知已发送：{label}",
                "title": node_config.get("title"),
                "body": node_config.get("body"),
                "platform": node_config.get("platform", "all"),
                "sent_at": datetime.now().isoformat()
            }
        else:
            return {
                "success": True,
                "message": f"站内消息已发送：{label}",
                "user_ids": node_config.get("user_ids", []),
                "message": node_config.get("message"),
                "sent_at": datetime.now().isoformat()
            }

    def get_execution_status(self, execution_id: str) -> Optional[Dict]:
        """获取执行状态"""
        return self.executions.get(execution_id)

    def get_workflow_executions(self, workflow_id: str) -> List[Dict]:
        """获取工作流的所有执行记录"""
        return [
            exec_data for exec_id, exec_data in self.executions.items()
            if exec_data["workflow_id"] == workflow_id
        ]

    def get_node_definitions(self) -> List[Dict]:
        """获取所有节点定义"""
        return [
            {"type": "trigger", "name": "触发器", "description": "触发工作流执行"},
            {"type": "action", "name": "动作", "description": "执行具体操作"},
            {"type": "condition", "name": "条件", "description": "条件分支判断"},
            {"type": "api", "name": "API 集成", "description": "调用外部 API"},
            {"type": "llm", "name": "AI 模型", "description": "调用大语言模型"},
            {"type": "data", "name": "数据处理", "description": "数据存取操作"},
            {"type": "learning", "name": "学习相关", "description": "学习相关操作"},
            {"type": "notification", "name": "通知消息", "description": "发送通知"}
        ]

# 全局引擎实例
workflow_engine = WorkflowEngine()
