from abc import ABC, abstractmethod
from typing import Any, Dict


class IPlugin(ABC):
    """插件接口基类，所有插件必须继承此类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """插件描述"""
        pass

    @abstractmethod
    def on_init(self, config: Dict[str, Any]) -> None:
        """插件初始化

        Args:
            config: 插件配置字典
        """
        pass

    @abstractmethod
    def on_schedule(self) -> None:
        """定时任务回调，用于周期性执行插件逻辑"""
        pass

    @abstractmethod
    def on_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """HTTP 请求回调，用于响应外部 API 调用

        Args:
            request: 请求参数字典

        Returns:
            响应数据字典
        """
        pass

    def on_destroy(self) -> None:
        """插件销毁，用于清理资源"""
        pass
