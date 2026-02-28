# LinkBridge

LinkBridge - 跨 NAS 软链接管理工具，支持群晖、威联通、飞牛、极空间等主流 NAS 系统。

## 功能特性

- **多 NAS 支持**: 自动适配群晖、威联通、飞牛、极空间等 NAS 系统
- **软链接管理**: 创建、删除、查看软链接
- **断链检测**: 自动检测损坏的软链接并报警
- **插件架构**: 支持动态加载插件扩展功能
- **Docker 联动**: 通过插件与 Docker 容器联动
- **多架构支持**: 支持 amd64 和 arm64 架构

## 项目结构

```
backend/
├── app/
│   ├── adapters/          # 文件系统适配器
│   │   ├── base.py        # 抽象基类
│   │   ├── generic.py     # 通用 Linux 适配器
│   │   ├── synology.py    # 群晖适配器
│   │   ├── qnap.py        # 威联通适配器
│   │   └── fnos.py        # 飞牛适配器
│   ├── plugins/           # 插件系统
│   │   ├── interface.py   # 插件接口
│   │   └── manager.py     # 插件管理器
│   ├── middleware/        # 中间件
│   │   └── security.py    # 安全中间件
│   ├── models/            # 数据模型
│   ├── routers/           # API 路由
│   └── __init__.py
├── plugins/               # 示例插件
│   ├── docker_helper.py   # Docker 联动插件
│   └── docker_helper.json # 插件配置
├── spk/                   # 群晖 SPK 包
├── fnos/                  # 飞牛 App Center 配置
├── .github/workflows/     # CI/CD 配置
├── tests/                 # 单元测试
├── main.py                # 应用入口
├── requirements.txt       # 依赖列表
├── Dockerfile             # Docker 镜像
├── docker-compose.yml     # Docker Compose 配置
└── .env.example           # 环境变量模板
```

## 快速开始

### 环境变量配置

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
cp .env.example .env
```

### Docker Compose 运行

```bash
docker-compose up -d
```

### Docker 运行

```bash
docker run -d \
  --name linkbridge \
  -p 8000:8000 \
  -v /volume1:/volume1:ro \
  -v /share:/share:ro \
  -v /data:/data:ro \
  -v ./plugins:/app/plugins:rw \
  -e NAS_SYSTEM=generic \
  -e ALLOWED_ROOTS=/ \
  linkbridge/linkbridge:latest
```

## 各品牌 NAS 安装指南

### 群晖 (Synology)

#### 1. 通过 Docker 安装

```bash
# SSH 登录群晖
ssh admin@your-nas-ip

# 创建 docker-compose.yml
mkdir -p /volume1/docker/linkbridge
cd /volume1/docker/linkbridge
cat > docker-compose.yml <<EOF
services:
  linkbridge:
    image: linkbridge/linkbridge:latest
    container_name: linkbridge
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - NAS_SYSTEM=synology
      - ALLOWED_ROOTS=/volume1,/volume2,/volume3
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - /volume1:/volume1:ro
      - /volume2:/volume2:ro
      - /volume3:/volume3:ro
      - ./plugins:/app/plugins:rw
EOF

# 启动服务
docker-compose up -d
```

#### 2. 通过 SPK 包安装

1. 下载 `linkbridge.spk` 安装包
2. 登录群晖 DSM，进入「套件中心」
3. 点击「手动安装」，选择下载的 SPK 包
4. 按照向导完成安装

#### 3. 权限设置

```bash
# 赋予 Docker 容器访问权限
sudo chown -R 1026:100 /volume1/docker/linkbridge
```

### 威联通 (QNAP)

#### 1. 通过 Container Station 安装

```bash
# SSH 登录威联通
ssh admin@your-nas-ip

# 创建 docker-compose.yml
mkdir -p /share/Container/linkbridge
cd /share/Container/linkbridge
cat > docker-compose.yml <<EOF
services:
  linkbridge:
    image: linkbridge/linkbridge:latest
    container_name: linkbridge
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - NAS_SYSTEM=qnap
      - ALLOWED_ROOTS=/share,/share/CACHEDEV1_DATA
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - /share:/share:ro
      - /share/CACHEDEV1_DATA:/share/CACHEDEV1_DATA:ro
      - ./plugins:/app/plugins:rw
EOF

# 启动服务
docker-compose up -d
```

#### 2. 通过 Container Station UI 安装

1. 打开「Container Station」
2. 点击「创建」，选择「Docker Compose」
3. 粘贴上述 yaml 配置
4. 点击「创建」完成安装

#### 3. 权限设置

```bash
# 赋予容器访问权限
sudo chown -R 1000:100 /share/Container/linkbridge
```

### 飞牛 (FnOS)

#### 1. 通过 App Center 安装

1. 打开「App Center」
2. 搜索「LinkBridge」
3. 点击「安装」
4. 按照向导完成配置

#### 2. 通过 Docker 安装

```bash
# SSH 登录飞牛
ssh admin@your-nas-ip

# 创建 docker-compose.yml
mkdir -p /data/docker/linkbridge
cd /data/docker/linkbridge
cat > docker-compose.yml <<EOF
services:
  linkbridge:
    image: linkbridge/linkbridge:latest
    container_name: linkbridge
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - NAS_SYSTEM=fnos
      - ALLOWED_ROOTS=/data,/mnt/data
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - /data:/data:ro
      - /mnt/data:/mnt/data:ro
      - ./plugins:/app/plugins:rw
EOF

# 启动服务
docker-compose up -d
```

#### 3. 权限设置

```bash
# 赋予容器访问权限
sudo chown -R 1000:100 /data/docker/linkbridge
```

### 极空间 (ZSpace)

#### 1. 通过 Docker 安装

```bash
# SSH 登录极空间
ssh admin@your-nas-ip

# 创建 docker-compose.yml
mkdir -p /mnt/HD1/HD1_a2/docker/linkbridge
cd /mnt/HD1/HD1_a2/docker/linkbridge
cat > docker-compose.yml <<EOF
services:
  linkbridge:
    image: linkbridge/linkbridge:latest
    container_name: linkbridge
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - NAS_SYSTEM=generic
      - ALLOWED_ROOTS=/mnt/HD1/HD1_a2,/mnt/MD0/MD0_Data1
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - /mnt/HD1/HD1_a2:/mnt/HD1/HD1_a2:ro
      - /mnt/MD0/MD0_Data1:/mnt/MD0/MD0_Data1:ro
      - ./plugins:/app/plugins:rw
EOF

# 启动服务
docker-compose up -d
```

#### 2. 权限设置

```bash
# 赋予容器访问权限
sudo chown -R 1000:100 /mnt/HD1/HD1_a2/docker/linkbridge
```

### 通用 Linux

```bash
# 创建 docker-compose.yml
mkdir -p ~/linkbridge
cd ~/linkbridge
cat > docker-compose.yml <<EOF
services:
  linkbridge:
    image: linkbridge/linkbridge:latest
    container_name: linkbridge
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - NAS_SYSTEM=generic
      - ALLOWED_ROOTS=/
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - /:/rootfs:ro
      - ./plugins:/app/plugins:rw
EOF

# 启动服务
docker-compose up -d
```

## API 接口

### 列出目录内容

```bash
curl http://localhost:8000/api/v1/list?path=/
```

### 创建软链接

```bash
curl -X POST http://localhost:8000/api/v1/symlink/create \
  -H "Content-Type: application/json" \
  -d '{
    "source": "/path/to/source",
    "target": "/path/to/target"
  }'
```

### 删除软链接

```bash
curl -X POST http://localhost:8000/api/v1/symlink/delete \
  -H "Content-Type: application/json" \
  -d '{
    "symlink_path": "/path/to/symlink"
  }'
```

### 检查损坏的软链接

```bash
curl -X POST http://localhost:8000/api/v1/symlink/check-broken \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/"
  }'
```

## 插件开发

### 插件接口

```python
from app.plugins.interface import IPlugin

class MyPlugin(IPlugin):
    @property
    def name(self) -> str:
        return "my_plugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "My custom plugin"

    def on_init(self, config: Dict[str, Any]) -> None:
        """插件初始化"""
        pass

    def on_schedule(self) -> None:
        """定时任务回调"""
        pass

    def on_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """HTTP 请求回调"""
        return {"status": "ok"}

    def on_destroy(self) -> None:
        """插件销毁"""
        pass
```

### 插件配置

在插件目录下创建同名 JSON 配置文件：

```json
{
  "enabled": true,
  "schedule_interval": 300,
  "custom_config": "value"
}
```

### 示例插件

参考 `plugins/docker_helper.py` 了解如何开发 Docker 联动插件。

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| NAS_SYSTEM | NAS 系统类型 (synology/qnap/fnos/generic) | 自动探测 |
| ALLOWED_ROOTS | 允许访问的根目录（逗号分隔） | / |
| HOST | 监听地址 | 0.0.0.0 |
| PORT | 监听端口 | 8000 |
| LOG_LEVEL | 日志级别 (DEBUG/INFO/WARNING/ERROR) | INFO |

## 安全机制

- 所有文件操作必须经过 `SecurityMiddleware` 校验
- 确保操作路径在用户授权的 `ALLOWED_ROOTS` 列表内
- 严禁越界访问

## CI/CD

项目使用 GitHub Actions 自动构建多架构镜像：

- **触发条件**: 推送到 main 分支或创建 tag
- **构建架构**: linux/amd64, linux/arm64
- **镜像仓库**: Docker Hub

## 运行测试

```bash
pytest tests/
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- GitHub: https://github.com/yourusername/linkbridge
- Issues: https://github.com/yourusername/linkbridge/issues
