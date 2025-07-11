"""
统一测试数据管理模块
提供结构化的测试数据访问接口，支持登录、聊天、知识库等各种测试场景
"""
import time
import yaml
import os
from utils.log_manager import logger


class TestDataManager:
    """测试数据管理器 - 统一管理所有测试数据"""
    
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), "test_data.yaml")
        self._data = None
    
    @property
    def data(self):
        """延迟加载数据"""
        if self._data is None:
            self._data = self.load_data()
        return self._data
    
    def load_data(self):
        """加载YAML数据文件"""
        try:
            with open(self.data_file, encoding="utf-8") as f:
                data = yaml.safe_load(f)
                logger.info(f"成功加载测试数据: {self.data_file}")
                return data
        except FileNotFoundError:
            logger.error(f"测试数据文件未找到: {self.data_file}")
            raise
        except Exception as e:
            logger.error(f"加载测试数据失败: {str(e)}")
            raise
    
    def get_login_data(self, data_type="valid_user"):
        """获取登录测试数据"""
        return self.data["login_data"][data_type]
    
    def get_chat_messages(self):
        """获取聊天消息数据"""
        return self.data["chat_data"]["messages"]
    
    def get_chat_questions(self):
        """获取聊天问题数据"""
        return {k: v for k, v in self.data["chat_data"].items() if k != "messages"}
    
    def get_knowledge_data(self, data_type="valid_knowledge"):
        """获取知识库数据"""
        return self.data["knowledge_data"][data_type]
    
    def get_form_data(self, form_type="user_profile"):
        """获取表单数据"""
        return self.data["form_data"][form_type]
    
    def get_test_config(self):
        """获取测试配置"""
        return self.data["test_config"]
    
    def generate_unique_name(self, prefix="测试"):
        """生成唯一名称"""
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        return f"{prefix}_{timestamp}"
    
    def get_variable(self, var_name):
        """获取变量值，支持动态替换"""
        variables = self.data.get("variables", {})
        value = variables.get(var_name, "")
        
        # 处理动态变量
        if "${timestamp}" in value:
            value = value.replace("${timestamp}", time.strftime('%Y%m%d_%H%M%S'))
        if "${random_string}" in value:
            value = value.replace("${random_string}", str(int(time.time() * 1000) % 10000))
        
        return value


# 全局实例
test_data_manager = TestDataManager()


# 向后兼容的函数接口
def get_ai_chat_data():
    """获取AI聊天数据 - 保持向后兼容"""
    return test_data_manager.get_chat_messages()


def get_kb_create_data():
    """获取知识库创建数据"""
    return {
        "name": test_data_manager.generate_unique_name("测试知识库"),
        "prompt": "快来创建知识库吧"
    }


def get_unique_kb_name(prefix="测试知识库"):
    """生成唯一的知识库名称 - 保持向后兼容"""
    return test_data_manager.generate_unique_name(prefix)
    