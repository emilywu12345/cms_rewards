"""配置加载器模块

此模块负责加载和管理测试配置，包括：
- YAML配置文件加载
- 环境配置管理
- 配置数据访问
"""

import os
import yaml
import logging
from typing import Dict, Any
from utils.log_manager import logger


class ConfigLoader:
    """配置加载器类"""
    
    _config = None
    
    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            dict: 配置数据
        """
        if cls._config is None:
            try:
                config_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    'config',
                    'config.yaml'
                )
                
                with open(config_path, 'r', encoding='utf-8') as f:
                    cls._config = yaml.safe_load(f)
                logger.info("配置文件加载成功")
                
            except Exception as e:
                logger.error(f"加载配置文件失败: {str(e)}")
                raise
                
        return cls._config
    
    @classmethod
    def get_env_config(cls, env: str = None) -> Dict[str, Any]:
        """
        获取环境配置
        
        Args:
            env: 环境名称，如果未指定则使用默认环境
            
        Returns:
            dict: 环境配置数据
        """
        config = cls.load_config()
        
        if not env:
            env = config.get('default_env', 'uat')
            
        logger.info(f"使用测试环境: {env}")
        env_config = config.get('environments', {}).get(env)
        
        if not env_config:
            logger.warning(f"未找到环境 {env} 的配置")
            return None
            
        return env_config
    
    @classmethod
    def get_browser_config(cls) -> Dict[str, Any]:
        """
        获取浏览器配置
        
        Returns:
            dict: 浏览器配置数据
        """
        config = cls.load_config()
        return config.get('browser', {})
    
    @classmethod
    def get_test_config(cls) -> Dict[str, Any]:
        """
        获取测试配置
        
        Returns:
            dict: 测试配置数据
        """
        config = cls.load_config()
        return config.get('test', {})
    
    @classmethod
    def get_report_config(cls) -> Dict[str, Any]:
        """
        获取报告配置
        
        Returns:
            dict: 报告配置数据
        """
        config = cls.load_config()
        return config.get('report', {})
