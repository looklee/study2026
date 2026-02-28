from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255))
    full_name = Column(String(255))
    avatar_url = Column(Text)
    
    # 学习配置
    current_level = Column(String(50), default="beginner")
    learning_style = Column(String(50), default="mixed")
    timezone = Column(String(50), default="Asia/Shanghai")
    
    # 状态
    status = Column(String(20), default="active")
    last_activity_at = Column(DateTime(timezone=True))
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    paths = relationship("LearningPath", back_populates="user", cascade="all, delete-orphan")
    progress_records = relationship("ProgressRecord", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")


class LearningPath(Base):
    """学习路径模型"""
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 路径信息
    path_name = Column(String(255), nullable=False)
    description = Column(Text)
    target_goal = Column(Text)
    total_duration = Column(String(50))
    
    # 路径数据（JSON 格式存储完整路径结构）
    path_data = Column(JSON, nullable=False)
    
    # 状态
    status = Column(String(20), default="active")
    current_phase = Column(Integer, default=0)
    overall_progress = Column(Integer, default=0)
    
    # 时间
    started_at = Column(DateTime(timezone=True))
    estimated_end_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="paths")
    progress_records = relationship("ProgressRecord", back_populates="path", cascade="all, delete-orphan")


class ProgressRecord(Base):
    """进度记录模型"""
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    
    # 项目信息
    item_type = Column(String(50), nullable=False)  # topic, phase, resource
    item_id = Column(String(255), nullable=False)
    action = Column(String(50), nullable=False)  # start, complete, update
    
    # 状态
    completed = Column(Boolean, default=False)
    
    # 进度数据
    progress_data = Column(JSON)
    time_spent_minutes = Column(Integer, default=0)
    notes = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="progress_records")
    path = relationship("LearningPath", back_populates="progress_records")


class Conversation(Base):
    """对话记录模型"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(String(255), index=True)
    
    # 消息内容
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    
    # 元数据
    topics = Column(JSON)
    response_time_ms = Column(Integer)
    model_used = Column(String(50))
    
    # 反馈
    feedback_rating = Column(Integer)
    feedback_comment = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="conversations")


class Workflow(Base):
    """工作流模型"""
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 工作流信息
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # 工作流定义（JSON 格式）
    workflow_data = Column(JSON, nullable=False)
    
    # 状态
    status = Column(String(20), default="active")
    is_public = Column(Boolean, default=False)
    
    # 执行统计
    execution_count = Column(Integer, default=0)
    last_executed_at = Column(DateTime(timezone=True))
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User")


class KnowledgeDocument(Base):
    """知识文档模型"""
    __tablename__ = "knowledge_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 文件信息
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    category = Column(String(100), default="general")
    tags = Column(JSON, default=list)
    
    # 内容分析
    summary = Column(Text)
    key_points = Column(JSON)
    keywords = Column(JSON)
    difficulty = Column(String(20))
    
    # 向量存储 ID
    vector_store_id = Column(String(255))
    
    # 状态
    status = Column(String(20), default="pending")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User")
