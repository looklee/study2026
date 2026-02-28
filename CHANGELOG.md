# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 工作流节点库（8 大类 40+ 节点）
- 可视化工作流编辑器
- AI 驱动的学习路径生成
- 学习伴侣（虚拟宠物）系统
- 每日签到系统
- 知识库管理
- GitHub Actions CI/CD
- Dependabot 自动依赖更新

### Changed
- 优化前端构建缓存配置
- 改进认证流程

### Fixed
- 修复 lucide-react 图标导入问题（Fire → Flame）
- 修复 TypeScript 类型错误
- 修复 API 连接问题

---

## [1.0.0] - 2026-02-28

### Added
- ✨ **首次发布**
- 🎯 完整的 AI 学习平台功能
- 🔄 可视化工作流引擎
  - 触发器节点（5 种）
  - 动作节点（7 种）
  - 条件节点（4 种）
  - AI 模型节点（6 种）
  - API 集成节点（4 种）
  - 数据处理节点（6 种）
  - 学习相关节点（6 种）
  - 通知消息节点（5 种）
- 📚 知识库与 RAG 检索
- 💬 AI 导师对话系统
- 📊 学习进度追踪
- 🐾 虚拟宠物陪伴系统
- 📅 每日签到与奖励

### Technical
- **Frontend**: Next.js 14, TypeScript, TailwindCSS, ReactFlow
- **Backend**: FastAPI, Python, SQLAlchemy
- **Database**: SQLite (默认), PostgreSQL (可选)
- **DevOps**: GitHub Actions, Docker support

### Documentation
- README.md - 项目主文档
- CONTRIBUTING.md - 贡献指南
- CODE_OF_CONDUCT.md - 行为准则
- SECURITY.md - 安全策略
- INSTALL.md - 安装指南
- DEPLOYMENT.md - 部署指南

---

## Notes

- **[Unreleased]**: 未发布的更改（开发中）
- **[1.0.0]**: 首次公开发布

### Legend
- `Added` - 新功能
- `Changed` - 变更
- `Deprecated` - 即将弃用
- `Removed` - 删除
- `Fixed` - 修复
- `Security` - 安全修复
