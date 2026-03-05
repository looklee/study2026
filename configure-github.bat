@echo off
REM ============================================
REM Study2026 GitHub 仓库配置脚本
REM 用户：looklee
REM 仓库：study2026
REM ============================================

set GITHUB_USERNAME=looklee
set REPO_NAME=study2026

echo.
echo ========================================
echo   Study2026 GitHub 仓库配置
echo ========================================
echo.
echo   GitHub 用户名：%GITHUB_USERNAME%
echo   仓库地址：https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo ========================================
echo.

REM 检查 Git 是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Git
    echo 请先安装 Git: https://git-scm.com/
    pause
    exit /b 1
)

echo [✓] Git 已安装
echo.

REM 打开浏览器让用户创建仓库
echo [步骤 1] 请先在 GitHub 上创建仓库
echo.
echo   正在打开创建仓库页面...
start https://github.com/new?name=%REPO_NAME%&description=AI-powered+learning+platform&public=1
echo.
echo   请在打开的页面中：
echo   1. Repository name: %REPO_NAME%
echo   2. 选择 Public（公开）
echo   3. 不要勾选 "Initialize with README"
echo   4. 点击 "Create repository"
echo.
set /p DONE="完成后按回车继续..."

echo.
echo [步骤 2] 配置远程仓库...

REM 检查是否已配置远程仓库
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo [!] 已存在远程仓库配置，正在删除...
    git remote remove origin
)

REM 添加远程仓库
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
if %errorlevel% neq 0 (
    echo [错误] 添加远程仓库失败
    pause
    exit /b 1
)
echo [✓] 远程仓库已添加

REM 重命名主分支
echo.
echo [步骤 3] 重命名主分支为 main...
git branch -M main
echo [✓] 主分支已重命名

REM 推送代码
echo.
echo ========================================
echo   推送代码到 GitHub
echo ========================================
echo.
echo [推送] 正在上传代码...
echo       这可能需要几分钟，请耐心等待
echo.

git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   推送失败
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. 仓库未创建 - 请在上方打开的页面中创建仓库
    echo 2. 认证失败 - 需要 GitHub 密码或 Token
    echo.
    echo 如果是认证问题：
    echo 1. 访问 https://github.com/settings/tokens
    echo 2. 生成新 Token（勾选 repo 权限）
    echo 3. 使用 Token 代替密码重新推送
    echo.
    echo 手动推送命令：git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   配置完成！
echo ========================================
echo.
echo ✓ 代码已成功推送到 GitHub
echo.
echo 仓库地址：
echo https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.
echo 下一步操作：
echo 1. 访问仓库页面
echo 2. 添加 Topics
echo 3. 启用 GitHub Actions
echo 4. 创建第一个 Release (v1.0.0)
echo.
echo ========================================
echo.

REM 自动打开仓库页面
set /p OPEN_BROWSER="是否打开仓库页面？(Y/N): "
if /i "%OPEN_BROWSER%"=="Y" (
    start https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
)

pause
