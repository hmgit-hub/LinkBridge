import os
import platform
import uvicorn
from pathlib import Path
from app import app
from app.adapters import (
    GenericLinuxProvider,
    SynologyProvider,
    QnapProvider,
    FnOSProvider
)
from app.routers import router
from app.middleware.security import SecurityMiddleware


def detect_nas_system() -> str:
    """自动探测 NAS 系统"""
    system = platform.system().lower()

    # 检查群晖特征
    if Path("/etc/synoinfo.conf").exists() or Path("/usr/syno").exists():
        return "synology"

    # 检查威联通特征
    if Path("/etc/config/qpkg.conf").exists() or Path("/mnt/ext").exists():
        return "qnap"

    # 检查飞牛特征
    if Path("/etc/fnos_release").exists() or Path("/etc/fnos_version").exists():
        return "fnos"

    # 默认返回 generic
    return "generic"


def get_adapter(system: str):
    """根据系统类型返回对应的适配器"""
    adapters = {
        "synology": SynologyProvider,
        "qnap": QnapProvider,
        "fnos": FnOSProvider,
        "generic": GenericLinuxProvider
    }
    return adapters.get(system, GenericLinuxProvider)()


def main():
    # 自动探测 NAS 系统
    nas_system = os.getenv("NAS_SYSTEM", detect_nas_system())
    print(f"检测到 NAS 系统: {nas_system}")

    # 初始化适配器
    router.adapter = get_adapter(nas_system)

    # 添加安全中间件
    allowed_roots = os.getenv("ALLOWED_ROOTS", "/").split(",")
    app.add_middleware(SecurityMiddleware, allowed_roots=allowed_roots)

    # 启动服务
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
