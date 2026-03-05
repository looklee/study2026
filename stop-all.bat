@echo off
chcp 65001 >nul
REM ===========================================
REM STUDY2026 停止所有服务脚本
REM ===========================================

title STUDY2026 - 停止服务

echo.
echo ========================================
echo   STUDY2026 AI 学习平台
echo   停止所有服务
echo ========================================
echo.

echo [1/2] 正在停止后端 API...
taskkill /FI "WINDOWTITLE eq Study2026 API*" /T /F >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] 后端 API 已停止
) else (
    echo [!] 未找到运行中的后端 API
)

echo.
echo [2/2] 正在停止前端 Web...
taskkill /FI "WINDOWTITLE eq Study2026 Web*" /T /F >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] 前端 Web 已停止
) else (
    echo [!] 未找到运行中的前端 Web
)

echo.
echo ========================================
echo   清理完成！
echo ========================================
echo.
echo [提示] 如果仍有进程残留，可以手动关闭相关窗口
echo.
pause
