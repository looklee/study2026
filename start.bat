@echo off
REM ===========================================
REM STUDY2026 简化版启动脚本 (npm 版)
REM ===========================================

echo.
echo ========================================
echo   STUDY2026 AI 学习路径平台
echo   简化版启动脚本
echo ========================================
echo.

REM 检查 Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js
    echo 请先安装 Node.js: https://nodejs.org/
    pause
    exit /b 1
)

echo [✓] Node.js 已安装

REM 检查 npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 npm
    pause
    exit /b 1
)

echo [✓] npm 已安装

REM 检查 n8n 是否安装
n8n --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [提示] n8n 未安装，正在安装...
    echo.
    npm install -g n8n
    if %errorlevel% neq 0 (
        echo [错误] n8n 安装失败
        pause
        exit /b 1
    )
    echo [✓] n8n 安装完成
)

echo [✓] n8n 已安装

REM 检查 .env 文件
if not exist ".env" (
    echo.
    echo [提示] 正在创建环境变量文件...
    copy "docker\.env.example" ".env"
    echo.
    echo ========================================
    echo   请编辑 .env 文件配置 API 密钥
    echo ========================================
    echo.
    notepad ".env"
    echo.
    echo 配置完成后按任意键继续...
    pause
)

echo.
echo ========================================
echo   选择启动模式
echo ========================================
echo.
echo   1. 正常启动
echo   2. 隧道模式（外部可访问）
echo   3. 调试模式
echo   0. 退出
echo.
set /p choice="请输入选项 (0-3): "

if "%choice%"=="1" goto normal
if "%choice%"=="2" goto tunnel
if "%choice%"=="3" goto debug
if "%choice%"=="0" goto end

echo [错误] 无效的选项
pause
exit /b 1

:normal
echo.
echo ========================================
echo   启动 n8n...
echo ========================================
echo.
echo   访问地址：http://localhost:5678
echo.
echo   按 Ctrl+C 停止服务
echo.
echo ========================================
echo.
n8n start
goto end

:tunnel
echo.
echo ========================================
echo   启动 n8n（隧道模式）
echo ========================================
echo.
echo   外部访问地址将显示在下方
echo.
echo   按 Ctrl+C 停止服务
echo.
echo ========================================
echo.
n8n start --tunnel
goto end

:debug
echo.
echo ========================================
echo   启动 n8n（调试模式）
echo ========================================
echo.
echo   访问地址：http://localhost:5678
echo   调试日志已启用
echo.
echo   按 Ctrl+C 停止服务
echo.
echo ========================================
echo.
n8n start --debug
goto end

:end
echo.
echo 再见！
echo.
