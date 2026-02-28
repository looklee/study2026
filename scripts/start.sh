#!/bin/bash
# ===========================================
# STUDY2026 快速启动脚本 (Linux/Mac)
# ===========================================

set -e

echo ""
echo "========================================"
echo "  STUDY2026 AI 学习路径平台"
echo "  快速启动脚本"
echo "========================================"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "[错误] 未检测到 Docker，请先安装 Docker"
    echo "下载地址：https://docs.docker.com/get-docker/"
    exit 1
fi

echo "[✓] Docker 已安装"

# 检查 docker-compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "[错误] 未检测到 Docker Compose"
    exit 1
fi

echo "[✓] Docker Compose 已安装"

# 检查 .env 文件是否存在
if [ ! -f "docker/.env" ]; then
    echo ""
    echo "[提示] 首次运行，正在创建环境变量文件..."
    cp "docker/.env.example" "docker/.env"
    echo ""
    echo "========================================"
    echo "  请编辑 docker/.env 文件配置 API 密钥"
    echo "========================================"
    echo ""
    read -p "按任意键打开 .env 文件..."
    ${EDITOR:-nano} "docker/.env"
    echo ""
    echo "配置完成后，请重新运行此脚本"
    exit 0
fi

echo "[✓] 环境变量文件已存在"

# 选择启动模式
echo ""
echo "========================================"
echo "  请选择启动模式"
echo "========================================"
echo ""
echo "  1. 开发环境 (推荐初次使用)"
echo "  2. 生产环境"
echo "  3. 仅查看服务状态"
echo "  4. 停止所有服务"
echo "  5. 重置环境 (删除所有数据)"
echo "  0. 退出"
echo ""
read -p "请输入选项 (0-5): " choice

case $choice in
    1)
        echo ""
        echo "========================================"
        echo "  启动开发环境..."
        echo "========================================"
        echo ""
        docker-compose -f docker/docker-compose.dev.yml up -d
        ;;
    2)
        echo ""
        echo "========================================"
        echo "  启动生产环境..."
        echo "========================================"
        echo ""
        docker-compose -f docker/docker-compose.yml up -d
        ;;
    3)
        echo ""
        echo "========================================"
        echo "  服务状态"
        echo "========================================"
        echo ""
        docker-compose -f docker/docker-compose.dev.yml ps
        exit 0
        ;;
    4)
        echo ""
        echo "========================================"
        echo "  停止所有服务..."
        echo "========================================"
        echo ""
        docker-compose -f docker/docker-compose.dev.yml down
        echo "[✓] 所有服务已停止"
        exit 0
        ;;
    5)
        echo ""
        echo "========================================"
        echo "  警告：此操作将删除所有数据！"
        echo "========================================"
        echo ""
        read -p "确定要继续吗？(y/n): " confirm
        if [ "$confirm" = "y" ]; then
            docker-compose -f docker/docker-compose.dev.yml down -v
            echo "[✓] 环境已重置"
        else
            echo "[已取消]"
        fi
        exit 0
        ;;
    0)
        echo ""
        echo "再见！"
        echo ""
        exit 0
        ;;
    *)
        echo "[错误] 无效的选项"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "  启动成功！"
echo "========================================"
echo ""
echo "  服务访问地址:"
echo "  - n8n:       http://localhost:5678"
echo "  - pgAdmin:   http://localhost:5050"
echo "  - Chroma:    http://localhost:8000"
echo ""
echo "  默认登录:"
echo "  - 用户名：admin"
echo "  - 密码：admin"
echo ""
echo "  请查看日志：docker-compose -f docker/docker-compose.dev.yml logs -f"
echo ""
echo "========================================"
