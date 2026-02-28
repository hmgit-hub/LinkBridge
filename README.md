# LinkBridge

LinkBridge - 跨 NAS 软链接管理工具，支持群晖、威联通、飞牛、极空间等主流 NAS 系统。

## 项目简介

LinkBridge 是一款专为 NAS 用户设计的软链接管理工具，旨在解决跨 NAS 系统、跨存储池的文件访问问题。通过软链接技术，用户可以轻松地在不同存储位置之间建立逻辑连接，实现统一的文件访问路径。

### 核心特性

- **多 NAS 支持**: 自动适配群晖、威联通、飞牛、极空间等 NAS 系统
- **软链接管理**: 创建、删除、查看软链接
- **断链检测**: 自动检测损坏的软链接并报警
- **插件架构**: 支持动态加载插件扩展功能
- **Docker 联动**: 通过插件与 Docker 容器联动
- **多架构支持**: 支持 amd64 和 arm64 架构
- **移动端支持**: iOS/Android 双平台 App

## 项目结构

```
LinkBridge/
├── backend/               # 后端服务
│   ├── app/
│   │   ├── adapters/      # 文件系统适配器
│   │   ├── plugins/       # 插件系统
│   │   ├── middleware/    # 中间件
│   │   ├── models/        # 数据模型
│   │   └── routers/       # API 路由
│   ├── plugins/           # 示例插件
│   ├── spk/               # 群晖 SPK 包
│   ├── fnos/              # 飞牛 App Center 配置
│   ├── tests/             # 单元测试
│   ├── Dockerfile         # Docker 镜像
│   └── README.md          # 后端文档
├── mobile/                # 移动端 App
│   ├── lib/
│   │   ├── services/      # 服务层
│   │   ├── models/        # 数据模型
│   │   ├── providers/     # 状态管理
│   │   └── screens/       # 页面
│   ├── android/           # Android 配置
│   ├── ios/               # iOS 配置
│   └── README.md          # 移动端文档
└── README.md              # 项目文档
```

## 快速开始

### 后端部署

#### Docker Compose 部署

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/linkbridge.git
cd linkbridge/backend

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，根据需要修改配置

# 3. 启动服务
docker-compose up -d

# 4. 访问 Web UI
open http://localhost:8000
```

#### 各品牌 NAS 安装指南

详细的安装指南请参考 [backend/README.md](backend/README.md#各品牌-nas-安装指南)

- [群晖 (Synology)](backend/README.md#群晖-synology)
- [威联通 (QNAP)](backend/README.md#威联通-qnap)
- [飞牛 (FnOS)](backend/README.md#飞牛-fnos)
- [极空间 (ZSpace)](backend/README.md#极空间-zspace)

### 移动端部署

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/linkbridge.git
cd linkbridge/mobile

# 2. 安装依赖
flutter pub get

# 3. 代码生成
flutter pub run build_runner build --delete-conflicting-outputs

# 4. 运行应用
flutter run

# 5. 构建发布包
flutter build apk --release
flutter build ios --release
```

详细的开发指南请参考 [mobile/README.md](mobile/README.md)

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

LinkBridge 支持通过插件扩展功能。插件系统基于 Python 动态加载，允许开发者自定义功能。

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

### 示例插件

参考 [backend/plugins/docker_helper.py](backend/plugins/docker_helper.py) 了解如何开发 Docker 联动插件。

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| NAS_SYSTEM | NAS 系统类型 (synology/qnap/fnos/generic) | 自动探测 |
| ALLOWED_ROOTS | 允许访问的根目录（逗号分隔） | / |
| HOST | 监听地址 | 0.0.0.0 |
| PORT | 监听端口 | 8000 |
| LOG_LEVEL | 日志级别 (DEBUG/INFO/WARNING/ERROR) | INFO |

## 安全机制

- **路径验证**: 所有文件操作必须经过 `SecurityMiddleware` 校验
- **访问控制**: 确保操作路径在用户授权的 `ALLOWED_ROOTS` 列表内
- **只读挂载**: NAS 目录以只读方式挂载，防止误操作
- **插件隔离**: 插件运行在独立进程空间

## CI/CD

项目使用 GitHub Actions 自动构建多架构镜像：

- **触发条件**: 推送到 main 分支或创建 tag
- **构建架构**: linux/amd64, linux/arm64
- **镜像仓库**: Docker Hub

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 后端: 遵循 PEP 8 规范
- 移动端: 遵循 Flutter 官方规范
- 提交信息: 遵循 Conventional Commits 规范

## 许可证

MIT License

## 联系方式

- GitHub: https://github.com/yourusername/linkbridge
- Issues: https://github.com/yourusername/linkbridge/issues
- Discussions: https://github.com/yourusername/linkbridge/discussions

## 致谢

感谢所有为此项目做出贡献的开发者！

## 更新日志

### v1.0.0 (2024-02-28)

- 初始版本发布
- 支持群晖、威联通、飞牛、极空间等 NAS 系统
- 实现软链接管理功能
- 实现断链检测功能
- 实现插件架构
- 发布 iOS/Android 移动端 App
