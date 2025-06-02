import pytest
import allure
import time
import logging
from page_objects.knowledge_base_page import KnowledgeBasePage
from utils.config_loader import ConfigLoader

@allure.feature("知识库管理")
class TestKnowledgeBase:
    
    @allure.story("创建知识库")
    @allure.description("验证用户能否成功创建新的知识库")
    @pytest.mark.usefixtures("logged_in_driver")
    def test_create_knowledge_base(self, logged_in_driver):
        kb_name = f"测试知识库_{time.strftime('%Y%m%d_%H%M%S')}"
        kb_desc = "这是一个自动化测试创建的知识库"
        kb_page = KnowledgeBasePage(logged_in_driver)
        
        with allure.step(f"创建知识库: {kb_name}"):
            logging.info("等待页面加载完成")
            result = kb_page.create_knowledge_base(kb_name, kb_desc)
            allure.attach(
                logged_in_driver.get_screenshot_as_png(),
                name="创建知识库结果",
                attachment_type=allure.attachment_type.PNG
            )
            assert result, "创建知识库失败"
    
    @allure.story("编辑知识库")
    @allure.description("验证用户能否成功编辑现有知识库")
    @pytest.mark.usefixtures("logged_in_driver")
    def test_edit_knowledge_base(self, logged_in_driver):
        kb_page = KnowledgeBasePage(logged_in_driver)
        new_name = f"编辑的知识库_{time.strftime('%Y%m%d_%H%M%S')}"
        new_desc = "这是编辑后的知识库描述"
        
        with allure.step(f"编辑知识库为: {new_name}"):
            result = kb_page.edit_knowledge_base(new_name, new_desc)
            allure.attach(
                logged_in_driver.get_screenshot_as_png(),
                name="编辑知识库结果",
                attachment_type=allure.attachment_type.PNG
            )
            assert result, "编辑知识库失败"
            
        with allure.step("验证编辑结果"):
            current_name = kb_page.get_first_kb_name()
            assert new_name in current_name, f"知识库名称未更新，当前名称: {current_name}"
