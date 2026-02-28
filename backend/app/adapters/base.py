from abc import ABC, abstractmethod
from typing import List
from pathlib import Path


class FileSystemAdapter(ABC):
    """文件系统适配器抽象基类"""

    @abstractmethod
    async def list_dir(self, path: str) -> List[dict]:
        """列出目录内容"""
        pass

    @abstractmethod
    async def create_symlink(self, source: str, target: str) -> None:
        """创建软链接"""
        pass

    @abstractmethod
    async def delete_symlink(self, symlink_path: str) -> None:
        """删除软链接"""
        pass

    @abstractmethod
    async def check_broken(self, path: str) -> List[str]:
        """检查损坏的软链接"""
        pass
