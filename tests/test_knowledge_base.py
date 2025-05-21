import pytest
import allure
import time
import logging
from page_objects.login_page import LoginPage
from page_objects.knowledge_base_page import KnowledgeBasePage

@allure.feature("知识库管理")
class TestKnowledgeBase:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        """前置条件：用户已登录"""
        with allure.step("登录系统"):
            login_page = LoginPage(driver)
            result = login_page.login(
                config['ENV']['username'],
                config['ENV']['password']
            )
            assert result, "登录失败，无法继续测试"
            # 等待页面加载完成
            time.sleep(3)
        self.kb_page = KnowledgeBasePage(driver)
    
    @allure.story("创建知识库")
    @allure.description("验证用户能否成功创建新的知识库")    def test_create_knowledge_base(self, driver):
        kb_name = f"测试知识库_{time.strftime('%Y%m%d_%H%M%S')}"
        kb_desc = "这是一个自动化测试创建的知识库"
        
        with allure.step(f"创建知识库: {kb_name}"):
            logging.info("等待页面加载完成")
            time.sleep(3)  # 等待页面完全加载
            result = self.kb_page.create_knowledge_base(kb_name, kb_desc)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="创建知识库结果",
                attachment_type=allure.attachment_type.PNG
            )
            assert result, "创建知识库失败"
    
    @allure.story("编辑知识库")
    @allure.description("验证用户能否成功编辑现有知识库")
    def test_edit_knowledge_base(self, driver):
        new_name = "已编辑的知识库"
        new_desc = "这是编辑后的知识库描述"
        
        with allure.step(f"编辑知识库为: {new_name}"):
            result = self.kb_page.edit_knowledge_base(new_name, new_desc)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="编辑知识库结果",
                attachment_type=allure.attachment_type.PNG
            )
            assert result, "编辑知识库失败"
            
        with allure.step("验证编辑结果"):
            current_name = self.kb_page.get_first_kb_name()
            assert new_name in current_name, f"知识库名称未更新，当前名称: {current_name}"
