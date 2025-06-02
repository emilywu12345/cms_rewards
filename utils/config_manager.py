from typing import Any, Dict
import yaml
import os
import logging
from pathlib import Path


class ConfigManager:
    """统一的配置管理类"""
    
    _instance = None
    _config = None
    
    @classmethod
    def get_instance(cls):
        """单例模式获取实例"""
        if cls._instance is None:
            cls._instance = ConfigManager()
        return cls._instance
    
    def __init__(self):
        """初始化配置管理器"""
        if self._config is None:
            self._config = self._load_config()
        self._init_directories()
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config", "config.yaml")
            
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                logging.info("成功加载配置文件")
                return config
        except Exception as e:
            logging.error(f"加载配置文件失败: {str(e)}")
            raise
    
    def _init_directories(self):
        """初始化必要的目录结构"""
        directories = [
            "logs",
            "screenshots",
            "reports/allure-results",
            "reports/allure-report"
        ]
        
        try:
            for dir_path in directories:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
            logging.info("成功初始化目录结构")
        except Exception as e:
            logging.error(f"创建目录失败: {str(e)}")
            raise
    
    def get_browser_config(self) -> Dict[str, Any]:
        """获取浏览器配置"""
        return self._config.get("browser", {})
    
    def get_env_config(self, env: str = None) -> Dict[str, Any]:
        """
        获取环境配置
        Args:
            env: 环境名称，如果未指定则使用默认环境
        """
        if not env:
            env = self._config.get("default_env", "uat")
        
        env_config = self._config.get("environments", {}).get(env)
        if not env_config:
            logging.warning(f"未找到环境 {env} 的配置，使用 uat 环境")
            env_config = self._config.get("environments", {}).get("uat", {})
        
        return env_config
    
    def get_test_config(self) -> Dict[str, Any]:
        """获取测试配置"""
        return self._config.get("test", {})
    
    def get_report_config(self) -> Dict[str, Any]:
        """获取报告配置"""
        return self._config.get("report", {})
    
    def get_wait_time(self, type_: str = "medium") -> int:
        """
        获取等待时间
        Args:
            type_: 等待类型 (short/medium/long)
        """
        wait_times = self.get_test_config().get("wait", {
            "short": 5,
            "medium": 10,
            "long": 30
        })
        return wait_times.get(type_, 10)
    
    def get_screenshot_dir(self) -> str:
        """获取截图保存目录"""
        return self.get_test_config().get("screenshot_dir", "screenshots")
    
    def get_base_url(self, env: str = None) -> str:
        """
        获取基础URL
        Args:
            env: 环境名称
        """
        return self.get_env_config(env).get("url", "")
