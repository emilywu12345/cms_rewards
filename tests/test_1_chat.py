import pytest
import allure
import time
import logging
from page_objects.knowledge_page import KnowledgePage
from page_objects.chat_page import ChatPage
from utils.config_manager import ConfigManager
from data.test_data import get_ai_chat_data

@allure.feature("聊天")
# 使用类级别已登录driver夹具，保证本类所有用例共用同一浏览器会话，提升执行效率
@pytest.mark.usefixtures("session_logged_in_driver")
class TestChat:
    """
    聊天相关自动化测试用例集。
    - driver 由 class 级别 fixture 注入，所有用例共用同一浏览器会话，提升执行效率。
    - 页面对象模式(POM)业务操作全部通过 ChatPage 实现，测试用例只负责业务流程和断言。
    - 用例结构清晰，便于维护和扩展。
    """

    @pytest.fixture(autouse=True)
    def _inject_driver(self, session_logged_in_driver):
        self.driver = session_logged_in_driver

    @pytest.mark.parametrize("message_type, case_name", [
        ("normal_message", "正常消息"),
        ("empty_message", "空消息"),
        ("long_message", "长文本消息"),
        ("special_char_message", "特殊字符消息"),
        ("multi_line_message", "多行消息")
    ])
    @allure.story("AI 聊天")
    @allure.description("验证用户能否成功发送不同类型消息")
    def test_2_send_message(self, message_type, case_name):
        """
        步骤：
        1. 发送不同类型消息
        2. 验证消息发送成功并显示在聊天记录
        """
        chat_page = ChatPage(self.driver)
        test_data = get_ai_chat_data()
        message = test_data[message_type]
        
        with allure.step(f"发送{case_name}: {message[:50]}"):
            logging.info(f"发送{case_name}，内容: {message}")
            assert chat_page.send_message(message), f"{case_name}发送失败"
        
        with allure.step(f"验证{case_name}显示"):
            assert chat_page.is_message_displayed(message), f"{case_name}未显示在聊天记录中"