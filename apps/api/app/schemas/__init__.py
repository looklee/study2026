from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============== 用户相关 ==============

class UserBase(BaseModel):
    """用户基础模式"""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """更新用户"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    current_level: Optional[str] = None
    learning_style: Optional[str] = None


class UserResponse(UserBase):
    """用户响应"""
    id: int
    current_level: str
    learning_style: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== 学习路径相关 ==============

class LearningPathBase(BaseModel):
    """学习路径基础"""
    path_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_goal: Optional[str] = None


class LearningPathCreate(LearningPathBase):
    """创建学习路径"""
    current_level: str
    available_hours_per_week: int
    preferred_learning_style: Optional[str] = "mixed"
    prior_experience: Optional[List[str]] = []
    deadline: Optional[datetime] = None


class LearningPathGenerate(BaseModel):
    """AI 生成学习路径请求"""
    currentLevel: str = Field(..., description="当前水平")
    targetGoal: str = Field(..., description="学习目标")
    availableHoursPerWeek: int = Field(..., ge=1, le=168, description="每周可用小时数")
    preferredLearningStyle: Optional[str] = "mixed"
    priorExperience: Optional[List[str]] = []
    deadline: Optional[str] = None
    budget: Optional[str] = "free"


class LearningPathResponse(LearningPathBase):
    """学习路径响应"""
    id: int
    user_id: int
    target_goal: Optional[str]
    total_duration: Optional[str]
    path_data: Dict[str, Any]
    status: str
    current_phase: int
    overall_progress: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== 进度相关 ==============

class ProgressTrack(BaseModel):
    """进度追踪请求"""
    userId: int
    pathId: int
    action: str = Field(..., pattern="^(start|complete|update)$")
    itemType: str = Field(..., pattern="^(topic|phase|resource)$")
    itemId: str
    metadata: Optional[Dict[str, Any]] = None


class ProgressResponse(BaseModel):
    """进度响应"""
    status: str
    progress: Dict[str, Any]
    statistics: Dict[str, Any]
    achievements: List[Dict[str, Any]]
    motivation: str
    streak: int


# ============== AI 对话相关 ==============

class ChatMessage(BaseModel):
    """聊天消息"""
    message: str = Field(..., min_length=1, max_length=10000)
    userId: int
    conversationId: Optional[str] = None


class ChatResponse(BaseModel):
    """聊天响应"""
    message: str
    conversationId: str
    topics: Optional[List[str]] = []
    suggestions: Optional[List[str]] = []
    responseTime: int


# ============== 工作流相关 ==============

class WorkflowNode(BaseModel):
    """工作流节点"""
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]


class WorkflowConnection(BaseModel):
    """工作流连接"""
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None


class WorkflowCreate(BaseModel):
    """创建工作流"""
    name: str
    description: Optional[str] = None
    nodes: List[WorkflowNode]
    connections: List[WorkflowConnection]


class WorkflowExecute(BaseModel):
    """执行工作流"""
    inputData: Optional[Dict[str, Any]] = None


# ============== 推荐相关 ==============

class RecommendationRequest(BaseModel):
    """推荐请求"""
    userId: int
    topics: List[str]
    level: str = "beginner"
    languages: Optional[List[str]] = ["Python"]
    pricePreference: Optional[str] = "free"
    limit: Optional[int] = 10


class RecommendationItem(BaseModel):
    """推荐项"""
    id: str
    title: str
    type: str
    url: str
    description: str
    difficulty: str
    estimatedHours: int
    rating: float
    reason: str
    tags: List[str]


class RecommendationResponse(BaseModel):
    """推荐响应"""
    status: str
    recommendations: List[RecommendationItem]
    learningPath: str
    tips: str


# ============== 知识库相关 ==============

class KnowledgeUpload(BaseModel):
    """知识上传"""
    fileName: str
    category: Optional[str] = "general"
    tags: Optional[List[str]] = []
    content: str


class KnowledgeQuery(BaseModel):
    """知识查询"""
    query: str = Field(..., min_length=1, max_length=5000)
    filters: Optional[Dict[str, Any]] = None
    limit: Optional[int] = 10


class KnowledgeResponse(BaseModel):
    """知识响应"""
    status: str
    answer: str
    sources: List[Dict[str, Any]]
    query: str


# ============== 通用响应 ==============

class MessageResponse(BaseModel):
    """消息响应"""
    status: str
    message: str


class ErrorResponse(BaseModel):
    """错误响应"""
    status: str = "error"
    error: str
    detail: Optional[str] = None
