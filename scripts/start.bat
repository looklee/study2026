@echo off
REM ===========================================
REM STUDY2026 快速启动脚本 (Windows)
REM ===========================================

echo.
echo ========================================
echo   STUDY2026 AI 学习路径平台
echo   快速启动脚本
echo ========================================
echo.

REM 检查 Docker 是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Docker，请先安装 Docker Desktop
    echo 下载地址：https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [✓] Docker 已安装

REM 检查 docker-compose 是否安装
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Docker Compose
    pause
    exit /b 1
)

echo [✓] Docker Compose 已安装

REM 检查 .env 文件是否存在
if not exist "docker\.env" (
    echo.
    echo [提示] 首次运行，正在创建环境变量文件...
    copy "docker\.env.example" "docker\.env"
    echo.
    echo ========================================
    echo   请编辑 docker\.env 文件配置 API 密钥
    echo ========================================
    echo.
    echo 按任意键打开 .env 文件...
    pause
    notepad "docker\.env"
    echo.
    echo 配置完成后，请重新运行此脚本
    pause
    exit /b 0
)

echo [✓] 环境变量文件已存在

REM 选择启动模式
echo.
echo ========================================
echo   请选择启动模式
echo ========================================
echo.
echo   1. 开发环境 (推荐初次使用)
echo   2. 生产环境
echo   3. 仅查看服务状态
echo   4. 停止所有服务
echo   5. 重置环境 (删除所有数据)
echo   0. 退出
echo.
set /p choice="请输入选项 (0-5): "

if "%choice%"=="1" goto dev
if "%choice%"=="2" goto prod
if "%choice%"=="3" goto status
if "%choice%"=="4" goto stop
if "%choice%"=="5" goto reset
if "%choice%"=="0" goto end

echo [错误] 无效的选项
pause
exit /b 1

:dev
echo.
echo ========================================
echo   启动开发环境...
echo ========================================
echo.
docker-compose -f docker\docker-compose.dev.yml up -d
if %errorlevel% neq 0 (
    echo [错误] 启动失败
    pause
    exit /b 1
)
goto success

:prod
echo.
echo ========================================
echo   启动生产环境...
echo ========================================
echo.
docker-compose -f docker\docker-compose.yml up -d
if %errorlevel% neq 0 (
    echo [错误] 启动失败
    pause
    exit /b 1
)
goto success

:status
echo.
echo ========================================
echo   服务状态
echo ========================================
echo.
docker-compose -f docker\docker-compose.dev.yml ps
pause
exit /b 0

:stop
echo.
echo ========================================
echo   停止所有服务...
echo ========================================
echo.
docker-compose -f docker\docker-compose.dev.yml down
echo [✓] 所有服务已停止
pause
exit /b 0

:reset
echo.
echo ========================================
echo   警告：此操作将删除所有数据！
echo ========================================
echo.
set /p confirm="确定要继续吗？(y/n): "
if "%confirm%"=="y" (
    docker-compose -f docker\docker-compose.dev.yml down -v
    echo [✓] 环境已重置
) else (
    echo [已取消]
)
pause
exit /b 0

:success
echo.
echo ========================================
echo   启动成功！
echo ========================================
echo.
echo   服务访问地址:
echo   - n8n:       http://localhost:5678
echo   - pgAdmin:   http://localhost:5050
echo   - Chroma:    http://localhost:8000
echo.
echo   默认登录:
echo   - 用户名：admin
echo   - 密码：admin
echo.
echo   请查看日志：docker-compose -f docker\docker-compose.dev.yml logs -f
echo.
echo ========================================
pause

:end
echo.
echo 再见！
echo.
