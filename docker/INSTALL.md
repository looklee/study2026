# 🐳 Docker Desktop 安装指南

## 步骤 1：下载 Docker Desktop

### 官方下载地址
https://www.docker.com/products/docker-desktop/

### 或直接下载链接
- **Windows 版**: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

---

## 步骤 2：安装 Docker

1. **运行安装程序**
   - 双击下载的 `Docker Desktop Installer.exe`

2. **选择安装选项**
   ```
   ✅ Use WSL 2 instead of Hyper-V (推荐)
   ✅ Add shortcut to desktop
   ```

3. **等待安装完成**
   - 安装过程约 5-10 分钟

4. **重启电脑**
   - 安装完成后需要重启

---

## 步骤 3：启动 Docker Desktop

1. **打开 Docker Desktop**
   - 双击桌面快捷方式
   - 或在开始菜单搜索 "Docker Desktop"

2. **首次启动配置**
   - 接受服务条款
   - 选择是否发送使用数据（可选）
   - 等待 Docker 引擎启动（约 1 分钟）

3. **确认运行状态**
   - 看到左下角显示 **"Engine running"** 表示成功

---

## 步骤 4：验证安装

打开 **PowerShell** 或 **命令提示符**，运行：

```bash
# 检查 Docker 版本
docker --version

# 检查 Docker Compose 版本
docker-compose --version

# 运行测试容器
docker run hello-world
```

如果看到类似以下输出，表示安装成功：

```
Docker version 25.x.x, build xxxxxxx
Docker Compose version v2.x.x

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## 步骤 5：运行 STUDY2026

安装成功后，再次运行启动脚本：

```bash
# 在项目目录中
scripts\start.bat
```

选择 `1. 开发环境` 启动服务。

---

## ⚠️ 常见问题

### 问题 1：WSL 2 未安装

**错误信息**: "WSL 2 installation is not available"

**解决方案**:
```bash
# 在 PowerShell 中运行（管理员权限）
wsl --install

# 重启电脑
```

### 问题 2：虚拟化未启用

**错误信息**: "Virtualization is not enabled"

**解决方案**:
1. 重启电脑，进入 BIOS/UEFI 设置
2. 找到 **Intel VT-x** 或 **AMD-V** 选项
3. 设置为 **Enabled**
4. 保存并重启

### 问题 3：端口被占用

**错误信息**: "Bind for 0.0.0.0:5678 failed: port is already allocated"

**解决方案**:
1. 打开 `docker\.env` 文件
2. 修改端口：
   ```env
   N8N_PORT=5679
   ```
3. 重新启动

### 问题 4：Docker Desktop 一直启动中

**解决方案**:
1. 打开 Docker Desktop 设置（齿轮图标）
2. 进入 **Resources** → **Advanced**
3. 调整资源分配：
   - CPUs: 2-4 核心
   - Memory: 4-8 GB
   - Disk: 50 GB+
4. 点击 **Apply & Restart**

---

## 📚 系统要求

| 要求 | 说明 |
|------|------|
| **操作系统** | Windows 10 64-bit 专业版/企业版/教育版 或 Windows 11 |
| **内存** | 至少 4GB（推荐 8GB+） |
| **磁盘** | 至少 10GB 可用空间 |
| **虚拟化** | BIOS 中启用虚拟化技术 |

---

## 🔗 有用链接

- [Docker 官方文档](https://docs.docker.com/desktop/)
- [Docker 入门教程](https://docs.docker.com/get-started/)
- [WSL 2 安装指南](https://learn.microsoft.com/zh-cn/windows/wsl/install)

---

## 安装完成后

1. ✅ 确认 Docker Desktop 显示 "Engine running"
2. ✅ 在命令行运行 `docker --version` 验证
3. ✅ 再次运行 `scripts\start.bat` 启动项目

**有任何问题随时告诉我！** 🚀
