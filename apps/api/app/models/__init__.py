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
    current_phase = Column(String(50), default="planning")
    
    # 统计
    completed_steps = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # 关系
    user = relationship("User", back_populates="paths")
    steps = relationship("LearningPathStep", back_populates="path", cascade="all, delete-orphan")


class LearningPathStep(Base):
    """学习路径步骤模型"""
    __tablename__ = "learning_path_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    
    # 步骤信息
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content = Column(Text)
    resource_links = Column(JSON)  # 存储相关资源链接
    
    # 类型和难度
    step_type = Column(String(50), default="content")  # content, exercise, quiz, project
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    estimated_duration = Column(String(20))  # 如 "30分钟", "1小时"
    
    # 状态
    status = Column(String(20), default="pending")  # pending, in_progress, completed
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    path = relationship("LearningPath", back_populates="steps")
    progress_records = relationship("ProgressRecord", back_populates="step", cascade="all, delete-orphan")


class ProgressRecord(Base):
    """进度记录模型"""
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    step_id = Column(Integer, ForeignKey("learning_path_steps.id"))
    
    # 进度信息
    activity_type = Column(String(50), nullable=False)  # study, practice, assessment, review
    content_summary = Column(Text)
    duration_minutes = Column(Integer, default=0)
    engagement_score = Column(Float)  # 0-100, 用户参与度评分
    comprehension_score = Column(Float)  # 0-100, 理解程度评分
    
    # 学习成果
    notes = Column(Text)
    achievements = Column(JSON)  # 学习成就
    feedback = Column(Text)
    
    # 状态
    status = Column(String(20), default="completed")
    
    # 时间戳
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="progress_records")
    step = relationship("LearningPathStep", back_populates="progress_records")


class Conversation(Base):
    """对话模型"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 对话信息
    title = Column(String(255), nullable=False)
    conversation_data = Column(JSON, nullable=False)  # 存储完整的对话历史
    summary = Column(Text)  # 对话摘要
    tags = Column(JSON)  # 对话标签
    
    # 统计
    message_count = Column(Integer, default=0)
    last_message_at = Column(DateTime(timezone=True))
    
    # 状态
    is_active = Column(Boolean, default=True)
    status = Column(String(20), default="active")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="conversations")


class KnowledgeItem(Base):
    """知识项模型"""
    __tablename__ = "knowledge_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 知识信息
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(String(50), default="text")  # text, link, note, code, image
    source = Column(String(255))  # 来源
    tags = Column(JSON)  # 标签
    
    # 知识图谱关系
    related_items = Column(JSON)  # 相关知识点ID列表
    category = Column(String(100))  # 分类
    difficulty = Column(String(20), default="medium")  # 难度
    
    # 学习统计
    times_reviewed = Column(Integer, default=0)
    last_reviewed_at = Column(DateTime(timezone=True))
    retention_score = Column(Float, default=0.0)  # 保留分数
    
    # 状态
    status = Column(String(20), default="active")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="knowledge_items")


class Notification(Base):
    """通知模型"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 通知信息
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # reminder, achievement, system, ai_suggestion
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    
    # 附加数据
    data = Column(JSON)  # 额外的数据负载
    
    # 状态
    is_read = Column(Boolean, default=False)
    is_delivered = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    read_at = Column(DateTime(timezone=True))
    
    # 关系
    user = relationship("User", back_populates="notifications")


class File(Base):
    """文件模型"""
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 文件信息
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # 字节
    mime_type = Column(String(100))
    
    # 文件元数据
    file_metadata = Column(JSON)  # 文件的额外元数据
    
    # 状态
    status = Column(String(20), default="uploaded")  # uploaded, processing, processed, failed
    file_type = Column(String(50), default="document")  # document, image, audio, video
    
    # 时间戳
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="files")


class SystemSetting(Base):
    """系统设置模型"""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 设置键值
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text, nullable=False)
    description = Column(Text)
    
    # 设置分类
    category = Column(String(50))
    data_type = Column(String(20), default="string")  # string, integer, float, boolean, json
    
    # 状态
    is_public = Column(Boolean, default=False)  # 是否公开设置
    is_editable = Column(Boolean, default=True)  # 是否可编辑
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Pet(Base):
    """学习宠物模型"""
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # 宠物信息
    name = Column(String(100), nullable=False, default="小学者")
    pet_type = Column(String(50), default="cat")
    avatar_url = Column(Text)

    # 成长系统
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    experience_to_next_level = Column(Integer, default=100)

    # 状态
    happiness = Column(Integer, default=50)
    energy = Column(Integer, default=50)
    health = Column(Integer, default=100)

    # 统计
    total_interactions = Column(Integer, default=0)
    consecutive_days = Column(Integer, default=0)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_interaction_at = Column(DateTime(timezone=True))

    # 关系
    user = relationship("User", backref="pet")


class CheckinRecord(Base):
    """签到记录模型"""
    __tablename__ = "checkin_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    checkin_date = Column(String(10), nullable=False, index=True)
    points_earned = Column(Integer, default=10)
    streak_bonus = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

    __table_args__ = (
        __import__('sqlalchemy').UniqueConstraint('user_id', 'checkin_date', name='uq_user_checkin_date'),
    )


class Device(Base):
    """设备模型"""
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(64), unique=True, index=True, nullable=False)
    platform = Column(String(50), default="unknown")
    browser = Column(String(100))
    language = Column(String(20), default="zh-CN")
    timezone = Column(String(50), default="Asia/Shanghai")
    screen_resolution = Column(String(20))
    cpu_cores = Column(Integer)
    memory_gb = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    login_count = Column(Integer, default=1)
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")


class Session(Base):
    """用户会话模型"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(String(64), ForeignKey("devices.device_id"))
    session_data = Column(JSON)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    device = relationship("Device")


class UserBadge(Base):
    """用户徽章模型"""
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(String(50), nullable=False)
    badge_name = Column(String(100), nullable=False)
    badge_description = Column(Text)
    badge_icon = Column(String(255))
    reason = Column(Text)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

    __table_args__ = (
        __import__('sqlalchemy').UniqueConstraint('user_id', 'badge_id', name='uq_user_badge'),
    )


class Workflow(Base):
    """工作流模型"""
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    workflow_data = Column(JSON, nullable=False)  # 存储工作流定义
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    
    # 统计
    execution_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    owner = relationship("User", backref="workflows")


class KnowledgeDocument(Base):
    """知识文档模型"""
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 文档信息
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    document_type = Column(String(50), default="note")  # note, article, summary, etc.
    source_url = Column(String(500))  # 来源URL
    tags = Column(JSON)  # 标签
    
    # 知识图谱关系
    related_docs = Column(JSON)  # 相关文档ID列表
    category = Column(String(100))  # 分类
    difficulty = Column(String(20), default="medium")  # 难度
    
    # 学习统计
    times_accessed = Column(Integer, default=0)
    last_accessed_at = Column(DateTime(timezone=True))
    relevance_score = Column(Float, default=0.0)  # 相关性评分
    
    # 状态
    status = Column(String(20), default="active")
    is_archived = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", backref="knowledge_documents")