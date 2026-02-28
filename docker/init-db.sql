-- ===========================================
-- STUDY2026 数据库初始化脚本
-- ===========================================

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ===========================================
-- 用户表
-- ===========================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    full_name VARCHAR(255),
    avatar_url TEXT,
    current_level VARCHAR(50) DEFAULT 'beginner',
    learning_style VARCHAR(50) DEFAULT 'mixed',
    timezone VARCHAR(50) DEFAULT 'Asia/Shanghai',
    status VARCHAR(20) DEFAULT 'active',
    last_activity_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- 学习路径表
-- ===========================================
CREATE TABLE IF NOT EXISTS learning_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    path_name VARCHAR(255) NOT NULL,
    description TEXT,
    target_goal TEXT,
    total_duration VARCHAR(50),
    path_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    current_phase INTEGER DEFAULT 0,
    overall_progress INTEGER DEFAULT 0,
    started_at TIMESTAMP WITH TIME ZONE,
    estimated_end_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_learning_paths_user_id ON learning_paths(user_id);
CREATE INDEX idx_learning_paths_status ON learning_paths(status);

-- ===========================================
-- 用户进度表
-- ===========================================
CREATE TABLE IF NOT EXISTS user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    path_id UUID REFERENCES learning_paths(id) ON DELETE CASCADE,
    item_type VARCHAR(50) NOT NULL, -- 'topic', 'phase', 'resource'
    item_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'start', 'complete', 'update'
    completed BOOLEAN DEFAULT FALSE,
    progress_data JSONB,
    time_spent_minutes INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_path_id ON user_progress(path_id);
CREATE INDEX idx_user_progress_completed ON user_progress(completed);

-- ===========================================
-- 知识文档表
-- ===========================================
CREATE TABLE IF NOT EXISTS knowledge_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    category VARCHAR(100) DEFAULT 'general',
    tags JSONB DEFAULT '[]',
    summary TEXT,
    key_points JSONB,
    keywords JSONB,
    difficulty VARCHAR(20), -- 'beginner', 'intermediate', 'advanced'
    prerequisites JSONB,
    related_topics JSONB,
    estimated_read_time INTEGER, -- 分钟
    uploaded_by UUID REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'processed', 'failed'
    vector_store_id VARCHAR(255), -- 向量库中的 ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_knowledge_documents_category ON knowledge_documents(category);
CREATE INDEX idx_knowledge_documents_status ON knowledge_documents(status);
CREATE INDEX idx_knowledge_documents_keywords ON knowledge_documents USING GIN(keywords);

-- ===========================================
-- 对话日志表
-- ===========================================
CREATE TABLE IF NOT EXISTS conversation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    conversation_id VARCHAR(255) NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    topics JSONB,
    response_time INTEGER, -- 毫秒
    feedback_rating INTEGER, -- 1-5 评分
    feedback_comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversation_logs_user_id ON conversation_logs(user_id);
CREATE INDEX idx_conversation_logs_conversation_id ON conversation_logs(conversation_id);
CREATE INDEX idx_conversation_logs_created_at ON conversation_logs(created_at);

-- ===========================================
-- 推荐资源表
-- ===========================================
CREATE TABLE IF NOT EXISTS recommended_resources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    path_id UUID REFERENCES learning_paths(id) ON DELETE CASCADE,
    resource_data JSONB NOT NULL,
    source VARCHAR(50), -- 'ai', 'manual', 'community'
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'viewed', 'saved', 'completed'
    viewed BOOLEAN DEFAULT FALSE,
    saved BOOLEAN DEFAULT FALSE,
    completed BOOLEAN DEFAULT FALSE,
    user_rating INTEGER, -- 1-5
    user_feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recommended_resources_user_id ON recommended_resources(user_id);
CREATE INDEX idx_recommended_resources_status ON recommended_resources(status);

-- ===========================================
-- 成就表
-- ===========================================
CREATE TABLE IF NOT EXISTS achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_key VARCHAR(100) NOT NULL,
    achievement_name VARCHAR(255) NOT NULL,
    description TEXT,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, achievement_key)
);

CREATE INDEX idx_achievements_user_id ON achievements(user_id);

-- ===========================================
-- 学习打卡表
-- ===========================================
CREATE TABLE IF NOT EXISTS study_streaks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    minutes_studied INTEGER DEFAULT 0,
    items_completed INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, date)
);

CREATE INDEX idx_study_streaks_user_id ON study_streaks(user_id);
CREATE INDEX idx_study_streaks_date ON study_streaks(date);

-- ===========================================
-- 通知表
-- ===========================================
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'reminder', 'milestone', 'achievement', 'system'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    action_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(read);

-- ===========================================
-- 系统配置表
-- ===========================================
CREATE TABLE IF NOT EXISTS system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- 插入默认配置
-- ===========================================
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('ai_model_config', '{"default_model": "gpt-4o", "fallback_model": "gpt-3.5-turbo", "temperature": 0.7}', 'AI 模型配置'),
('notification_settings', '{"email_enabled": true, "slack_enabled": false, "reminder_frequency": "daily"}', '通知设置'),
('learning_path_defaults', '{"default_duration": "12 周", "default_hours_per_week": 10}', '学习路径默认值')
ON CONFLICT (setting_key) DO NOTHING;

-- ===========================================
-- 创建更新触发器函数
-- ===========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ===========================================
-- 添加更新触发器
-- ===========================================
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_learning_paths_updated_at
    BEFORE UPDATE ON learning_paths
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_progress_updated_at
    BEFORE UPDATE ON user_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_knowledge_documents_updated_at
    BEFORE UPDATE ON knowledge_documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recommended_resources_updated_at
    BEFORE UPDATE ON recommended_resources
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ===========================================
-- 创建视图
-- ===========================================

-- 用户学习概览
CREATE OR REPLACE VIEW user_learning_overview AS
SELECT 
    u.id,
    u.username,
    u.email,
    u.current_level,
    COUNT(DISTINCT lp.id) as total_paths,
    COUNT(DISTINCT CASE WHEN lp.status = 'active' THEN lp.id END) as active_paths,
    AVG(lp.overall_progress) as avg_progress,
    COUNT(DISTINCT up.id) as total_progress_items,
    COUNT(DISTINCT CASE WHEN up.completed THEN up.id END) as completed_items
FROM users u
LEFT JOIN learning_paths lp ON u.id = lp.user_id
LEFT JOIN user_progress up ON u.id = up.user_id
GROUP BY u.id, u.username, u.email, u.current_level;

-- 学习路径统计
CREATE OR REPLACE VIEW learning_path_stats AS
SELECT 
    lp.id,
    lp.path_name,
    lp.user_id,
    lp.status,
    lp.overall_progress,
    lp.current_phase,
    COUNT(up.id) as total_items,
    COUNT(CASE WHEN up.completed THEN up.id END) as completed_items,
    SUM(up.time_spent_minutes) as total_time_spent,
    lp.created_at,
    lp.updated_at
FROM learning_paths lp
LEFT JOIN user_progress up ON lp.id = up.path_id
GROUP BY lp.id, lp.path_name, lp.user_id, lp.status, lp.overall_progress, lp.current_phase, lp.created_at, lp.updated_at;

-- ===========================================
-- 插入示例数据（可选）
-- ===========================================
-- INSERT INTO users (username, email, full_name, current_level) VALUES
-- ('demo_user', 'demo@example.com', '演示用户', 'beginner');
