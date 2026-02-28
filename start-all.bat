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

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python
    echo 请先安装 Python: https://www.python.org/
    pause
    exit /b 1
)
echo [✓] Python 已安装

REM 检查 Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js
    pause
    exit /b 1
)
echo [✓] Node.js 已安装

REM 检查后端依赖
echo.
echo [检查] 后端依赖...
python -c "import fastapi, uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo [安装] 正在安装后端依赖...
    pip install -q fastapi uvicorn python-multipart httpx pydantic
)
echo [✓] 后端依赖已安装

REM 检查前端依赖
echo.
echo [检查] 前端依赖...
cd apps\web
if not exist "node_modules" (
    echo [安装] 正在安装前端依赖...
    call npm install
)
echo [✓] 前端依赖已安装
cd ..\..

REM 清除前端缓存
echo.
echo [清理] 清除前端缓存...
if exist "apps\web\.next" (
    rmdir /s /q "apps\web\.next"
)
echo [✓] 缓存已清理

REM 启动后端
echo.
echo ========================================
echo   启动后端 API (端口 8001)
echo ========================================
echo.

cd apps\api
start "Study2026 API" cmd /k "echo 正在启动后端 API... && python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8001 --reload"
cd ..\..

REM 等待后端启动
echo [等待] 后端启动中 (8 秒)...
timeout /t 8 /nobreak >nul

REM 验证后端
python -c "import urllib.request; r = urllib.request.urlopen('http://localhost:8001/'); print('[✓] 后端 API 已启动:', r.status)" 2>nul
if %errorlevel% neq 0 (
    echo [!] 后端启动中，请等待...
    timeout /t 5 /nobreak >nul
)

REM 启动前端
echo.
echo ========================================
echo   启动前端 Web (端口 3000)
echo ========================================
echo.

cd apps\web
start "Study2026 Web" cmd /k "echo 正在启动前端... && npm run dev"
cd ..\..

REM 等待前端启动
echo [等待] 前端启动中 (10 秒)...
timeout /t 10 /nobreak >nul

REM 验证前端
python -c "import urllib.request; r = urllib.request.urlopen('http://localhost:3000/'); print('[✓] 前端 Web 已启动:', r.status)" 2>nul
if %errorlevel% neq 0 (
    echo [!] 前端启动中，请等待...
)

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo   访问地址:
echo   - 前端首页：http://localhost:3000
echo   - 工作流编辑器：http://localhost:3000/workflows
echo   - 后端 API: http://localhost:8001
echo   - API 文档：http://localhost:8001/docs
echo.
echo   停止服务:
echo   - 关闭对应的命令行窗口即可
echo ========================================
echo.

REM 打开浏览器
timeout /t 3 /nobreak >nul
start http://localhost:3000/workflows

pause
