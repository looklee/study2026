@echo off
chcp 65001 >nul
REM ===========================================
REM STUDY2026 整合版启动脚本
REM ===========================================

title STUDY2026 - 启动管理器

echo.
echo ========================================
echo   STUDY2026 AI 学习平台
echo   整合版一键启动
echo ========================================
echo.

cd /d "%~dp0"

REM 检查 Python
echo [1/6] 检查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python
    echo 请先安装 Python: https://www.python.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo [✓] Python 已安装: %%i

REM 检查 Node.js
echo.
echo [2/6] 检查 Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js
    echo 请先安装 Node.js: https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do echo [✓] Node.js 已安装: %%i

REM 检查 .env 文件
echo.
echo [3/6] 检查环境配置...
if not exist ".env" (
    echo [提示] 创建环境变量文件...
    copy .env.example .env >nul
    echo [✓] .env 文件已创建
) else (
    echo [✓] .env 文件已存在
)

REM 检查后端依赖
echo.
echo [4/6] 检查后端依赖...
python -c "import fastapi, uvicorn, httpx, pydantic" >nul 2>&1
if %errorlevel% neq 0 (
    echo [安装] 正在安装后端依赖...
    cd apps\api
    pip install -r requirements-simple.txt -q
    cd ..\..
)
echo [✓] 后端依赖已就绪

REM 检查前端依赖
echo.
echo [5/6] 检查前端依赖...
cd apps\web
if not exist "node_modules" (
    echo [安装] 正在安装前端依赖...
    call npm install
)
cd ..\..
echo [✓] 前端依赖已就绪

REM 获取本机 IP
echo.
echo [6/6] 获取网络配置...
for /f "tokens=14" %%i in ('ipconfig ^| findstr /i "IPv4"') do set LOCAL_IP=%%i
if "%LOCAL_IP%"=="" set LOCAL_IP=localhost
echo [✓] 本机 IP: %LOCAL_IP%

echo.
echo ========================================
echo   正在启动服务...
echo ========================================
echo.

REM 启动后端
echo [启动] 后端 API (端口 8001)...
cd apps\api
start "Study2026 API" cmd /k "title Study2026 API && echo. && echo ======================================== && echo   Study2026 后端 API && echo   监听地址: 0.0.0.0:8001 && echo   本地访问: http://localhost:8001 && echo   外部访问: http://%LOCAL_IP%:8001 && echo ======================================== && echo. && python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8001 --reload"
cd ..\..

REM 等待后端启动
echo [等待] 后端启动中 (5 秒)...
timeout /t 5 /nobreak >nul

REM 启动前端
echo.
echo [启动] 前端 Web (端口 3000)...
cd apps\web
start "Study2026 Web" cmd /k "title Study2026 Web && echo. && echo ======================================== && echo   Study2026 前端 Web && echo   监听地址: 0.0.0.0:3000 && echo   本地访问: http://localhost:3000 && echo   外部访问: http://%LOCAL_IP%:3000 && echo ======================================== && echo. && npm run dev -- -H 0.0.0.0"
cd ..\..

REM 等待前端启动
echo [等待] 前端启动中 (8 秒)...
timeout /t 8 /nobreak >nul

echo.
echo ========================================
echo   🎉 启动完成！
echo ========================================
echo.
echo   📱 访问地址:
echo.
echo   [本地访问]
echo   - 前端首页: http://localhost:3000
echo   - 后端 API: http://localhost:8001
echo.
echo   [局域网访问]
echo   - 前端首页: http://%LOCAL_IP%:3000
echo   - 后端 API: http://%LOCAL_IP%:8001
echo.
echo   📚 推荐页面:
echo   - 仪表板: http://%LOCAL_IP%:3000/dashboard
echo   - 学习路径: http://%LOCAL_IP%:3000/paths
echo   - AI 导师: http://%LOCAL_IP%:3000/chat
echo   - AI 工具库: http://%LOCAL_IP%:3000/tools
echo   - 工作流: http://%LOCAL_IP%:3000/workflows
echo.
echo   ⏹️  停止服务:
echo   - 关闭对应的命令行窗口即可
echo.
echo ========================================
echo.

REM 打开浏览器
echo [提示] 正在打开浏览器...
timeout /t 2 /nobreak >nul
start http://%LOCAL_IP%:3000

echo.
echo 按任意键关闭此窗口（服务继续运行）...
pause >nul
echo.
echo 提示: 后端和前端服务仍在独立窗口中运行
echo 如需完全停止，请关闭所有 Study2026 相关窗口
echo.
