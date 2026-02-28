@echo off
REM ===========================================
REM STUDY2026 一键启动脚本
REM ===========================================

echo.
echo ========================================
echo   STUDY2026 AI 学习平台
echo   一键启动脚本
echo ========================================
echo.

cd /d "%~dp0"

REM 检查 Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js
    echo 请先安装 Node.js: https://nodejs.org/
    pause
    exit /b 1
)
echo [✓] Node.js 已安装

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python
    pause
    exit /b 1
)
echo [✓] Python 已安装

REM 检查 .env 文件
if not exist ".env" (
    echo [提示] 创建环境变量文件...
    copy .env.example .env
    echo.
    echo ========================================
    echo   请编辑 .env 文件配置 API 密钥
    echo ========================================
    echo.
)

echo.
echo ========================================
echo   启动服务
echo ========================================
echo.

REM 启动后端
echo [1/2] 启动后端 API...
cd apps\api
start "Study2026 API" cmd /k "echo 正在启动后端 API... && python -m uvicorn app.main_v2:app --host 0.0.0.0 --port 8001 --reload"
cd ..\..

REM 等待后端启动
echo [等待] 后端启动中 (5 秒)...
timeout /t 5 /nobreak >nul

REM 启动前端
echo [2/2] 启动前端...
cd apps\web
if not exist "node_modules" (
    echo [提示] 正在安装前端依赖...
    call npm install
)
start "Study2026 Web" cmd /k "echo 正在启动前端... && npm run dev"
cd ..\..

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo   访问地址:
echo   - 前端：http://localhost:3000
echo   - 后端：http://localhost:8001
echo   - API 文档：http://localhost:8001/docs
echo.
echo   推荐访问页面:
echo   - 首页：http://localhost:3000
echo   - 仪表板：http://localhost:3000/dashboard
echo   - AI 工具库：http://localhost:3000/tools
echo   - 工作流：http://localhost:3000/workflows
echo.
echo   按 Ctrl+C 停止服务（需要手动关闭命令行窗口）
echo ========================================
echo.

REM 打开浏览器
timeout /t 3 /nobreak >nul
start http://localhost:3000

pause
