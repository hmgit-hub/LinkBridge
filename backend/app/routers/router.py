from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pathlib import Path
from app.models.schemas import (
    FileItem,
    SymlinkCreateRequest,
    SymlinkDeleteRequest,
    BrokenSymlinkCheckRequest,
    BrokenSymlinkCheckResponse,
    ErrorResponse
)
from app.adapters.base import FileSystemAdapter
import os

router = APIRouter()

# 全局适配器实例，将在 main.py 中初始化
adapter: FileSystemAdapter | None = None

def get_allowed_roots():
    """获取允许的根目录列表"""
    return [Path(p).resolve() for p in os.getenv("ALLOWED_ROOTS", "/").split(",")]


def validate_path(path: str) -> Path:
    """验证路径是否在允许的根目录范围内"""
    try:
        resolved_path = Path(path).resolve()
    except (OSError, RuntimeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的路径: {path}"
        )

    for allowed_root in get_allowed_roots():
        try:
            resolved_path.relative_to(allowed_root)
            return resolved_path
        except ValueError:
            continue

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"路径超出允许范围: {path}"
    )


@router.get("/list", response_model=list[FileItem])
async def list_directory(path: str = "/"):
    """列出目录内容"""
    if adapter is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="文件系统适配器未初始化"
        )

    validated_path = validate_path(path)

    try:
        items = await adapter.list_dir(str(validated_path))
        return [FileItem(**item) for item in items]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"列出目录失败: {str(e)}"
        )


@router.post("/symlink/create", response_model=dict)
async def create_symlink(request: SymlinkCreateRequest):
    """创建软链接"""
    if adapter is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="文件系统适配器未初始化"
        )

    validated_source = validate_path(request.source)
    validated_target = validate_path(request.target)

    try:
        await adapter.create_symlink(str(validated_source), str(validated_target))
        return {"message": "软链接创建成功"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建软链接失败: {str(e)}"
        )


@router.post("/symlink/delete", response_model=dict)
async def delete_symlink(request: SymlinkDeleteRequest):
    """删除软链接"""
    if adapter is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="文件系统适配器未初始化"
        )

    validated_path = validate_path(request.symlink_path)

    try:
        await adapter.delete_symlink(str(validated_path))
        return {"message": "软链接删除成功"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除软链接失败: {str(e)}"
        )


@router.post("/symlink/check-broken", response_model=BrokenSymlinkCheckResponse)
async def check_broken_symlinks(request: BrokenSymlinkCheckRequest):
    """检查损坏的软链接"""
    if adapter is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="文件系统适配器未初始化"
        )

    validated_path = validate_path(request.path)

    try:
        broken_symlinks = await adapter.check_broken(str(validated_path))
        return BrokenSymlinkCheckResponse(broken_symlinks=broken_symlinks)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"检查损坏软链接失败: {str(e)}"
        )
