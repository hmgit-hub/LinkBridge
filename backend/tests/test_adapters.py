import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from app.adapters.generic import GenericLinuxProvider
from app.adapters.synology import SynologyProvider
from app.adapters.qnap import QnapProvider
from app.adapters.fnos import FnOSProvider
from app.adapters.base import FileSystemAdapter


class TestGenericLinuxProvider:
    """测试 GenericLinuxProvider"""

    @pytest.fixture
    def provider(self):
        return GenericLinuxProvider()

    @pytest.mark.asyncio
    async def test_list_dir_success(self, provider, tmp_path):
        """测试成功列出目录"""
        # 创建测试文件和目录
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "dir1").mkdir()

        result = await provider.list_dir(str(tmp_path))

        assert len(result) == 2
        names = {item["name"] for item in result}
        assert "file1.txt" in names
        assert "dir1" in names

    @pytest.mark.asyncio
    async def test_list_dir_invalid_path(self, provider):
        """测试列出不存在的目录"""
        with pytest.raises(ValueError, match="路径不存在或不是目录"):
            await provider.list_dir("/nonexistent/path")

    @pytest.mark.asyncio
    async def test_create_symlink_success(self, provider, tmp_path):
        """测试成功创建软链接"""
        source = tmp_path / "source.txt"
        source.write_text("content")

        target = tmp_path / "link.txt"
        await provider.create_symlink(str(source), str(target))

        assert target.is_symlink()
        assert target.read_text() == "content"

    @pytest.mark.asyncio
    async def test_create_symlink_source_not_exist(self, provider, tmp_path):
        """测试创建软链接时源路径不存在"""
        source = tmp_path / "nonexistent.txt"
        target = tmp_path / "link.txt"

        with pytest.raises(ValueError, match="源路径不存在"):
            await provider.create_symlink(str(source), str(target))

    @pytest.mark.asyncio
    async def test_delete_symlink_success(self, provider, tmp_path):
        """测试成功删除软链接"""
        source = tmp_path / "source.txt"
        source.write_text("content")
        target = tmp_path / "link.txt"
        target.symlink_to(source)

        await provider.delete_symlink(str(target))

        assert not target.exists()

    @pytest.mark.asyncio
    async def test_delete_symlink_not_symlink(self, provider, tmp_path):
        """测试删除非软链接"""
        target = tmp_path / "file.txt"
        target.write_text("content")

        with pytest.raises(ValueError, match="路径不是软链接"):
            await provider.delete_symlink(str(target))

    @pytest.mark.asyncio
    async def test_check_broken_success(self, provider, tmp_path):
        """测试成功检查损坏的软链接"""
        source = tmp_path / "source.txt"
        source.write_text("content")
        target = tmp_path / "link.txt"
        target.symlink_to(source)

        # 删除源文件，使软链接损坏
        source.unlink()

        broken = await provider.check_broken(str(tmp_path))
        assert str(target) in broken


class TestSynologyProvider:
    """测试 SynologyProvider"""

    @pytest.fixture
    def provider(self):
        return SynologyProvider()

    def test_normalize_path_with_volume_prefix(self, provider):
        """测试规范化带 /volume 前缀的路径"""
        path = provider._normalize_path("/volume1/test")
        assert path == "/volume1/test"

    @patch.object(Path, "exists", return_value=True)
    def test_normalize_path_without_volume_prefix(self, mock_exists, provider):
        """测试规范化不带 /volume 前缀的路径"""
        path = provider._normalize_path("/test")
        assert path.startswith("/volume1")


class TestQnapProvider:
    """测试 QnapProvider"""

    @pytest.fixture
    def provider(self):
        return QnapProvider()

    def test_normalize_path_with_share_prefix(self, provider):
        """测试规范化带 /share 前缀的路径"""
        path = provider._normalize_path("/share/test")
        assert path == "/share/test"

    @patch.object(Path, "exists", return_value=True)
    def test_normalize_path_without_share_prefix(self, mock_exists, provider):
        """测试规范化不带 /share 前缀的路径"""
        path = provider._normalize_path("/test")
        assert path.startswith("/share")


class TestFnOSProvider:
    """测试 FnOSProvider"""

    @pytest.fixture
    def provider(self):
        return FnOSProvider()

    def test_normalize_path_with_data_prefix(self, provider):
        """测试规范化带 /data 前缀的路径"""
        path = provider._normalize_path("/data/test")
        assert path == "/data/test"

    @patch.object(Path, "exists", return_value=True)
    def test_normalize_path_without_data_prefix(self, mock_exists, provider):
        """测试规范化不带 /data 前缀的路径"""
        path = provider._normalize_path("/test")
        assert path.startswith("/data")


class TestFileSystemAdapter:
    """测试 FileSystemAdapter 抽象基类"""

    def test_adapter_is_abstract(self):
        """测试 FileSystemAdapter 是抽象类"""
        with pytest.raises(TypeError):
            FileSystemAdapter()
