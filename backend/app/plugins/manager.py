import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.plugins.interface import IPlugin


class PluginManager:
    """插件管理器，负责加载、管理和调用插件"""

    def __init__(self, plugin_dir: str = "/app/plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, IPlugin] = {}
        self.plugin_configs: Dict[str, Dict[str, Any]] = {}

    def load_plugins(self) -> None:
        """从插件目录加载所有插件"""
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir(parents=True, exist_ok=True)
            return

        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue

            try:
                self._load_plugin(plugin_file)
            except Exception as e:
                print(f"Failed to load plugin {plugin_file.name}: {e}")

    def _load_plugin(self, plugin_file: Path) -> None:
        """加载单个插件文件"""
        spec = importlib.util.spec_from_file_location(
            plugin_file.stem, plugin_file
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load spec for {plugin_file}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[plugin_file.stem] = module
        spec.loader.exec_module(module)

        # 查找实现了 IPlugin 的类
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, IPlugin)
                and attr is not IPlugin
            ):
                plugin_instance = attr()
                plugin_name = plugin_instance.name

                # 读取插件配置
                config_file = self.plugin_dir / f"{plugin_file.stem}.json"
                config = {}
                if config_file.exists():
                    import json

                    with open(config_file, "r", encoding="utf-8") as f:
                        config = json.load(f)

                # 初始化插件
                plugin_instance.on_init(config)

                self.plugins[plugin_name] = plugin_instance
                self.plugin_configs[plugin_name] = config
                print(f"Loaded plugin: {plugin_name} v{plugin_instance.version}")

    def get_plugin(self, name: str) -> Optional[IPlugin]:
        """获取指定名称的插件"""
        return self.plugins.get(name)

    def get_all_plugins(self) -> List[IPlugin]:
        """获取所有已加载的插件"""
        return list(self.plugins.values())

    def call_on_schedule(self) -> None:
        """调用所有插件的定时任务回调"""
        for plugin in self.plugins.values():
            try:
                plugin.on_schedule()
            except Exception as e:
                print(f"Error in plugin {plugin.name}.on_schedule: {e}")

    def call_on_request(self, plugin_name: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """调用指定插件的请求回调"""
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            raise ValueError(f"Plugin not found: {plugin_name}")

        return plugin.on_request(request)

    def destroy_all(self) -> None:
        """销毁所有插件"""
        for plugin in self.plugins.values():
            try:
                plugin.on_destroy()
            except Exception as e:
                print(f"Error in plugin {plugin.name}.on_destroy: {e}")

        self.plugins.clear()
        self.plugin_configs.clear()
