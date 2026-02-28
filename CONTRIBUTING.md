# 贡献指南

感谢您对 Study2026 项目的关注！欢迎通过以下方式贡献您的力量：

## 🤝 贡献方式

### 1. 报告问题

发现 Bug 或有功能建议？请创建 [Issue](https://github.com/YOUR_USERNAME/study2026/issues)：

- 🐛 **Bug 报告**：提供详细的重现步骤、环境信息
- 💡 **功能建议**：描述功能用途、使用场景
- 📚 **文档改进**：指出需要改进的文档部分

### 2. 提交代码

#### 开发环境设置

```bash
# 1. Fork 项目并克隆
git clone https://github.com/YOUR_USERNAME/study2026.git
cd study2026

# 2. 安装依赖
# 后端
cd apps/api
pip install -r requirements.txt

# 前端
cd apps/web
npm install

# 3. 创建开发分支
git checkout -b feature/your-feature-name
```

#### 代码规范

**Python：**
- 遵循 PEP 8 风格指南
- 使用类型注解
- 编写单元测试

**TypeScript/JavaScript：**
- 使用 ESLint 检查代码
- 使用 TypeScript 类型系统
- 编写有意义的变量名

#### 提交信息规范

```bash
# 格式：<type>(<scope>): <subject>

# 示例：
feat(workflow): 添加新的节点类型
fix(auth): 修复登录会话过期问题
docs(readme): 更新快速开始指南
style(format): 代码格式化
refactor(core): 重构用户认证逻辑
test(api): 添加 API 测试用例
```

**类型说明：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具配置

### 3. 改进文档

- 修正拼写错误和语法问题
- 补充缺失的文档
- 添加使用示例
- 翻译文档

## 📋 Pull Request 流程

1. **Fork 项目** - 点击右上角 Fork 按钮
2. **创建分支** - `git checkout -b feature/amazing-feature`
3. **提交更改** - `git commit -m 'feat: add amazing feature'`
4. **推送分支** - `git push origin feature/amazing-feature`
5. **创建 PR** - 在 GitHub 上创建 Pull Request

### PR 检查清单

在提交 PR 前，请确保：

- [ ] 代码通过所有测试
- [ ] 遵循项目代码规范
- [ ] 更新了相关文档
- [ ] 提交信息符合规范
- [ ] 无敏感信息泄露

## 🏷️ 分支命名

```
feature/    # 新功能
bugfix/     # Bug 修复
hotfix/     # 紧急修复
docs/       # 文档更新
refactor/   # 重构
test/       # 测试相关
```

## 💬 讨论交流

- 💬 [GitHub Discussions](https://github.com/YOUR_USERNAME/study2026/discussions) - 讨论交流
- 📧 Email: your-email@example.com
- 🐛 [Issues](https://github.com/YOUR_USERNAME/study2026/issues) - 问题反馈

## 🎯 开发任务

查看 [Good First Issues](https://github.com/YOUR_USERNAME/study2026/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) 开始您的第一次贡献！

## 📜 行为准则

请遵守以下准则：

- 尊重他人，保持友好
- 建设性批评，避免人身攻击
- 包容不同观点和经验
- 专注于对社区最有利的事情

## 🙏 致谢

感谢所有为 Study2026 项目做出贡献的开发者！

---

**第一次贡献？**

查看这些资源：
- [如何为开源项目做贡献](https://opensource.guide/how-to-contribute/)
- [第一次 PR 指南](https://github.com/firstcontributions/first-contributions)
