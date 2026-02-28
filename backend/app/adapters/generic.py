import aiofiles
from pathlib import Path
from app.adapters.base import FileSystemAdapter


class GenericLinuxProvider(FileSystemAdapter):
    """通用 Linux 文件系统适配器"""

    async def list_dir(self, path: str):
        dir_path = Path(path)
        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError(f"路径不存在或不是目录: {path}")

        result = []
        for item in dir_path.iterdir():
            try:
                stat = item.stat()
                is_symlink = item.is_symlink()
                symlink_target = None
                is_broken = False

                if is_symlink:
                    try:
                        symlink_target = str(item.readlink())
                        is_broken = not item.exists()
                    except OSError:
                        is_broken = True

                result.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size,
                    "is_symlink": is_symlink,
                    "symlink_target": symlink_target,
                    "is_broken": is_broken
                })
            except (PermissionError, OSError):
                continue

        return result

    async def create_symlink(self, source: str, target: str):
        src_path = Path(source)
        tgt_path = Path(target)

        if not src_path.exists():
            raise ValueError(f"源路径不存在: {source}")

        if tgt_path.exists():
            raise ValueError(f"目标路径已存在: {target}")

        tgt_path.symlink_to(src_path)

    async def delete_symlink(self, symlink_path: str):
        path = Path(symlink_path)

        if not path.is_symlink():
            raise ValueError(f"路径不是软链接: {symlink_path}")

        path.unlink()

    async def check_broken(self, path: str):
        dir_path = Path(path)
        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError(f"路径不存在或不是目录: {path}")

        broken_symlinks = []
        for item in dir_path.rglob("*"):
            if item.is_symlink() and not item.exists():
                broken_symlinks.append(str(item))

        return broken_symlinks
