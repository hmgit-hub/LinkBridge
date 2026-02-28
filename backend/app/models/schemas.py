from pydantic import BaseModel
from typing import List
from enum import Enum


class FileType(str, Enum):
    FILE = "file"
    DIRECTORY = "directory"


class FileItem(BaseModel):
    name: str
    path: str
    type: FileType
    size: int = 0
    is_symlink: bool = False
    symlink_target: str | None = None
    is_broken: bool = False


class SymlinkCreateRequest(BaseModel):
    source: str
    target: str


class SymlinkDeleteRequest(BaseModel):
    symlink_path: str


class BrokenSymlinkCheckRequest(BaseModel):
    path: str


class BrokenSymlinkCheckResponse(BaseModel):
    broken_symlinks: List[str]


class ErrorResponse(BaseModel):
    detail: str
