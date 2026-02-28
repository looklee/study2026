# 部署指南

本指南将帮助您将 Study2026 部署到生产环境。

## 📋 部署前检查清单

- [ ] 已完成所有功能测试
- [ ] 已配置生产环境变量
- [ ] 已更新 API 密钥为生产密钥
- [ ] 已配置数据库连接
- [ ] 已设置域名和 SSL 证书（如需要）

---

## 🐳 Docker 部署（推荐）

### 1. 构建镜像

```bash
# 构建后端镜像
docker build -t study2026-api:latest ./apps/api

# 构建前端镜像
docker build -t study2026-web:latest ./apps/web
```

### 2. 使用 Docker Compose

```bash
cd docker

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 3. 配置环境变量

在 `docker/.env` 文件中配置：

```env
# 数据库
DATABASE_URL=postgresql://user:password@postgres:5432/study2026

# Redis
REDIS_URL=redis://redis:6379

# API 密钥
OPENAI_API_KEY=your-production-key
QWEN_API_KEY=your-production-key

# JWT
JWT_SECRET_KEY=your-secure-secret-key
```

---

## ☁️ 云平台部署

### Vercel (前端)

1. 安装 Vercel CLI：
```bash
npm i -g vercel
```

2. 部署：
```bash
cd apps/web
vercel
```

3. 配置环境变量（在 Vercel 控制台）

### Railway / Render (后端)

1. 连接 GitHub 仓库
2. 设置环境变量
3. 自动部署

### AWS 部署

#### EC2 + Docker

```bash
# 1. 安装 Docker
sudo yum install -y docker
sudo service docker start

# 2. 克隆项目
git clone https://github.com/YOUR_USERNAME/study2026.git
cd study2026

# 3. 构建并运行
docker-compose up -d
```

#### Elastic Beanstalk

```bash
# 安装 EB CLI
pip install awsebcli

# 初始化并部署
cd apps/api
eb init
eb create production
```

---

## 🔧 手动部署

### 1. 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装依赖
sudo apt install -y python3 python3-pip nodejs npm nginx
```

### 2. 部署后端

```bash
cd /var/www/study2026/apps/api

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 创建 systemd 服务
sudo nano /etc/systemd/system/study2026-api.service
```

**systemd 服务配置：**
```ini
[Unit]
Description=Study2026 API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/study2026/apps/api
ExecStart=/var/www/study2026/apps/api/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main_simple:app --bind 0.0.0.0:8001
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl enable study2026-api
sudo systemctl start study2026-api
```

### 3. 部署前端

```bash
cd /var/www/study2026/apps/web

# 安装依赖
npm ci

# 构建
npm run build

# 使用 PM2 管理进程
npm install -g pm2
pm2 start npm --name "study2026-web" -- start
pm2 save
pm2 startup
```

### 4. 配置 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 后端 API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 重启 Nginx
sudo systemctl restart nginx
```

### 5. 配置 SSL（可选）

```bash
sudo certbot --nginx -d your-domain.com
```

---

## 🔍 监控和日志

### 日志查看

```bash
# 后端日志
sudo journalctl -u study2026-api -f

# 前端日志
pm2 logs study2026-web

# Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 健康检查

```bash
# API 健康检查
curl http://localhost:8001/health

# 前端检查
curl http://localhost:3000/
```

---

## 📊 性能优化

### 后端优化

- 使用 Gunicorn 多 worker
- 启用 Redis 缓存
- 数据库连接池
- 启用 API 响应缓存

### 前端优化

- 启用 Next.js ISR
- 配置 CDN
- 启用 Gzip 压缩
- 优化静态资源

---

## 🔐 安全建议

1. **防火墙配置**
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. **定期更新依赖**
```bash
# 后端
pip list --outdated
pip install --upgrade -r requirements.txt

# 前端
npm outdated
npm update
```

3. **备份数据库**
```bash
# SQLite 备份
cp study2026.db study2026_backup.db

# PostgreSQL 备份
pg_dump study2026 > backup.sql
```

---

## 🆘 故障排除

### 常见问题

**问题 1：端口被占用**
```bash
# 查看占用端口的进程
sudo lsof -i :8001
sudo kill -9 <PID>
```

**问题 2：权限错误**
```bash
sudo chown -R www-data:www-data /var/www/study2026
sudo chmod -R 755 /var/www/study2026
```

**问题 3：内存不足**
```bash
# 增加 swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 📞 支持

如有问题，请：
- 查看 [GitHub Issues](https://github.com/YOUR_USERNAME/study2026/issues)
- 发送邮件至 your-email@example.com

---

祝部署顺利！🎉
