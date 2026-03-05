# GitHub 仓库配置脚本

# ============================================
# 请在 GitHub 上先创建仓库，然后执行以下命令
# ============================================

# 1. 访问 https://github.com/new 创建新仓库
#    - Repository name: study2026
#    - Description: 🎯 AI 驱动的学习平台 | 可视化工作流引擎 | 智能学习路径生成
#    - Visibility: Public (公开)
#    - 不要勾选 "Initialize with README"

# 2. 创建仓库后，在下方替换 YOUR_USERNAME 为您的 GitHub 用户名
# 3. 执行以下所有命令

cd C:\Users\Administrator\Documents\TRAEproject\STUDY2026

# ============================================
# 配置远程仓库（替换 YOUR_USERNAME 为您的 GitHub 用户名）
# ============================================
git remote add origin https://github.com/YOUR_USERNAME/study2026.git

# ============================================
# 重命名主分支为 main
# ============================================
git branch -M main

# ============================================
# 推送到 GitHub
# ============================================
git push -u origin main

# ============================================
# 推送完成后，验证是否成功
# ============================================
# 访问 https://github.com/YOUR_USERNAME/study2026 查看代码是否已上传
