from pathlib import Path
from app.adapters.generic import GenericLinuxProvider


class QnapProvider(GenericLinuxProvider):
    """威联通 QTS 文件系统适配器"""

    def __init__(self):
        super().__init__()
        # 威联通特殊路径映射
        self.share_prefixes = ["/share", "/share/CACHEDEV1_DATA"]

    def _normalize_path(self, path: str) -> str:
        """规范化威联通路径，处理 /share 等特殊前缀"""
        path_obj = Path(path)

        # 如果路径以 /share 开头，保持原样
        if any(str(path_obj).startswith(prefix) for prefix in self.share_prefixes):
            return str(path_obj)

        # 否则尝试映射到默认共享目录
        for prefix in self.share_prefixes:
            share_path = Path(prefix)
            if share_path.exists():
                return str(share_path / path_obj.relative_to("/"))

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
