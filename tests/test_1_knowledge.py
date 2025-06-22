import pytest
import allure
import time
import logging
from page_objects.knowledge_page import KnowledgePage
from utils.config_manager import ConfigManager
from data.test_data import get_kb_create_data

@allure.feature("知识库管理")
# 使用类级别已登录driver夹具，保证本类所有用例共用同一浏览器会话，提升执行效率
@pytest.mark.usefixtures("class_logged_in_driver")
class TestKnowledge:
    """
    知识库相关自动化测试用例集。
    - driver 由 class 级别 fixture 注入，所有用例共用同一浏览器会话，提升执行效率。
    - 页面对象模式(POM)业务操作全部通过 KnowledgePage 实现，测试用例只负责业务流程和断言。
    - 用例结构清晰，便于维护和扩展。
    """
    @pytest.fixture(autouse=True, scope="class")
    def setup_class(self, class_logged_in_driver):
        """
        类级别 fixture,自动注入已登录的 driver。
        driver 生命周期由 conftest.py 管理，页面对象只负责业务操作。
        """
        self.driver = class_logged_in_driver

    @allure.story("导航到知识库")
    @allure.description("验证用户能否成功進入知识库")
    def test_1_navigate_knowledge(self):
        """
        步骤：
        1. 导航到知识库页面
        2. 验证能否成功加载知识库页面
        """
        kb_page = KnowledgePage(self.driver)
        with allure.step("导航到知识库"):
            logging.info("等待页面加载完成")
            assert kb_page.navigate_knowledge(),"导航到知识库失败"

    @allure.story("创建知识库")
    @allure.description("验证用户能否成功创建新的知识库")
    def test_2_create_knowledge(self):
        """
        步骤：
        1. 输入知识库相关信息
        2. 提交并断言创建成功
        """
        kb_page = KnowledgePage(self.driver)
        data = get_kb_create_data()
        kb_name = data["name"]
        kb_prompt = data["prompt"]
        with allure.step(f"创建知识库: {kb_name}"):
            logging.info("等待页面加载完成")
            result = kb_page.create_knowledge(kb_name, kb_prompt)
            assert result, "创建知识库失败"
