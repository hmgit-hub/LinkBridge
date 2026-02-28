from pathlib import Path
from app.adapters.generic import GenericLinuxProvider


class FnOSProvider(GenericLinuxProvider):
    """飞牛 FnOS 文件系统适配器"""

    def __init__(self):
        super().__init__()
        # 飞牛特殊路径映射
        self.data_prefixes = ["/data", "/mnt/data"]

    def _normalize_path(self, path: str) -> str:
        """规范化飞牛路径，处理 /data 等特殊前缀"""
        path_obj = Path(path)

        # 如果路径以 /data 开头，保持原样
        if any(str(path_obj).startswith(prefix) for prefix in self.data_prefixes):
            return str(path_obj)

        # 否则尝试映射到默认数据目录
        for prefix in self.data_prefixes:
            data_path = Path(prefix)
            if data_path.exists():
                return str(data_path / path_obj.relative_to("/"))

        return str(path_obj)

    async def list_dir(self, path: str):
        normalized_path = self._normalize_path(path)
        return await super().list_dir(normalized_path)

    async def create_symlink(self, source: str, target: str):
        normalized_source = self._normalize_path(source)
        normalized_target = self._normalize_path(target)
        return await super().create_symlink(normalized_source, normalized_target)

    async def delete_symlink(self, symlink_path: str):
        normalized_path = self._normalize_path(symlink_path)
        return await super().delete_symlink(normalized_path)

    async def check_broken(self, path: str):
        normalized_path = self._normalize_path(path)
        return await super().check_broken(normalized_path)
