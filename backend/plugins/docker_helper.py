import json
from pathlib import Path
from typing import Any, Dict

import docker

import sys
sys.path.insert(0, '/app')

from app.plugins.interface import IPlugin


class DockerHelperPlugin(IPlugin):
    """Docker 联动插件，用于读取容器配置并建议软链接"""

    @property
    def name(self) -> str:
        return "docker_helper"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "读取 Docker 容器配置，建议软链接路径"

    def __init__(self):
        self.client = None
        self.config = {}

    def on_init(self, config: Dict[str, Any]) -> None:
        """初始化 Docker 客户端"""
        self.config = config
        try:
            self.client = docker.from_env()
            print("DockerHelperPlugin: Docker client initialized")
        except Exception as e:
            print(f"DockerHelperPlugin: Failed to initialize Docker client: {e}")

    def on_schedule(self) -> None:
        """定时检查容器状态"""
        if self.client is None:
            return

        try:
            containers = self.client.containers.list(all=True)
            for container in containers:
                print(f"Container: {container.name}, Status: {container.status}")
        except Exception as e:
            print(f"DockerHelperPlugin.on_schedule error: {e}")

    def on_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        action = request.get("action")

        if action == "list_containers":
            return self._list_containers()
        elif action == "get_container_volumes":
            return self._get_container_volumes(request.get("container_name"))
        elif action == "suggest_symlinks":
            return self._suggest_symlinks(request.get("container_name"))
        else:
            return {"error": "Unknown action"}

    def _list_containers(self) -> Dict[str, Any]:
        """列出所有容器"""
        if self.client is None:
            return {"error": "Docker client not initialized"}

        try:
            containers = self.client.containers.list(all=True)
            return {
                "containers": [
                    {
                        "name": c.name,
                        "image": c.image.tags[0] if c.image.tags else str(c.image.id),
                        "status": c.status,
                    }
                    for c in containers
                ]
            }
        except Exception as e:
            return {"error": str(e)}

    def _get_container_volumes(self, container_name: str) -> Dict[str, Any]:
        """获取容器的卷挂载信息"""
        if self.client is None:
            return {"error": "Docker client not initialized"}

        try:
            container = self.client.containers.get(container_name)
            mounts = container.attrs.get("Mounts", [])

            return {
                "container": container_name,
                "mounts": [
                    {
                        "source": m.get("Source"),
                        "destination": m.get("Destination"),
                        "type": m.get("Type"),
                    }
                    for m in mounts
                ],
            }
        except Exception as e:
            return {"error": str(e)}

    def _suggest_symlinks(self, container_name: str) -> Dict[str, Any]:
        """建议软链接路径"""
        if self.client is None:
            return {"error": "Docker client not initialized"}

        try:
            container = self.client.containers.get(container_name)
            mounts = container.attrs.get("Mounts", [])

            suggestions = []
            for mount in mounts:
                source = mount.get("Source")
                destination = mount.get("Destination")

                if source and destination:
                    # 建议在容器内创建软链接，指向宿主机路径
                    suggestions.append(
                        {
                            "source": source,
                            "target": f"/host{source}",
                            "description": f"Symlink for {container_name} mount: {destination}",
                        }
                    )

            return {"container": container_name, "suggestions": suggestions}
        except Exception as e:
            return {"error": str(e)}

    def on_destroy(self) -> None:
        """清理资源"""
        if self.client:
            self.client.close()
        print("DockerHelperPlugin: Destroyed")
