import logging
import os
from datetime import datetime
from typing import Optional


class LogManager:
    """统一的日志管理类"""
    
    _instance = None
    _logger = None
    
    @classmethod
    def get_instance(cls):
        """单例模式获取实例"""
        if cls._instance is None:
            cls._instance = LogManager()
        return cls._instance
    
    def __init__(self):
        """初始化日志管理器"""
        if self._logger is None:
            self._setup_logging()
    
    def _setup_logging(self):
        """配置日志系统"""
        try:
            # 创建日志目录
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            
            # 生成日志文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"test_{timestamp}.log")
            
            # 创建日志记录器
            self._logger = logging.getLogger("TestAutomation")
            self._logger.setLevel(logging.INFO)
            
            # 文件处理器
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.INFO)
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 格式化器
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加处理器
            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)
            
            self.info("日志系统初始化完成")
            
        except Exception as e:
            print(f"初始化日志系统失败: {str(e)}")
            raise
    
    def debug(self, message: str, *args, **kwargs):
        """记录调试级别日志"""
        self._logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """记录信息级别日志"""
        self._logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """记录警告级别日志"""
        self._logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """记录错误级别日志"""
        self._logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """记录严重错误级别日志"""
        self._logger.critical(message, *args, **kwargs)
    
    def screenshot_log(self, message: str, screenshot_path: Optional[str] = None):
        """
        记录截图相关的日志
        Args:
            message: 日志消息
            screenshot_path: 截图路径
        """
        if screenshot_path:
            self.info(f"{message} - 截图路径: {screenshot_path}")
        else:
            self.warning(f"{message} - 截图失败")


# 创建全局日志管理器实例
logger = LogManager.get_instance()
