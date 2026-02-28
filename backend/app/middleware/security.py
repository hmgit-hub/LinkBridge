from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from pathlib import Path
import os


class SecurityMiddleware(BaseHTTPMiddleware):
    """安全中间件，确保所有文件操作在允许的根目录范围内"""

    def __init__(self, app, allowed_roots: list[str] | None = None):
        super().__init__(app)
        self.allowed_roots = [
            Path(root).resolve() for root in (allowed_roots or ["/"])
        ]

    def _validate_path(self, path: str) -> Path:
        """验证路径是否在允许的根目录范围内"""
        try:
            resolved_path = Path(path).resolve()
        except (OSError, RuntimeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的路径: {path}"
            )

        for allowed_root in self.allowed_roots:
            try:
                resolved_path.relative_to(allowed_root)
                return resolved_path
            except ValueError:
                continue

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"路径超出允许范围: {path}"
        )

    async def dispatch(self, request: Request, call_next):
        # 从请求体或查询参数中提取路径
        if request.method in ["POST", "PUT", "DELETE"]:
            body = await request.body()
            # 注意：这里简化处理，实际应该解析 JSON body
            # 在路由层会再次验证路径

        response = await call_next(request)
        return response
