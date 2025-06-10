import pytest
import allure
import time
import logging
from page_objects.knowledge_page import KnowledgePage
from utils.config_manager import ConfigManager

@allure.feature("知识库管理")
@pytest.mark.usefixtures("class_logged_in_driver")
class TestKnowledge:
    @pytest.fixture(autouse=True, scope="class")
    def setup_class(self, class_logged_in_driver):
        self.driver = class_logged_in_driver

    @allure.story("导航到知识库")
    @allure.description("验证用户能否成功進入知识库")
    def test_1_navigate_knowledge(self):
        kb_page = KnowledgePage(self.driver)
        with allure.step("导航到知识库"):
            logging.info("等待页面加载完成")
            assert kb_page.navigate_knowledge(),"导航到知识库失败"

    @allure.story("导航到知识库-无driver参数应报错")
    def test_2_navigate_knowledge(self):
        kb_page = KnowledgePage(self.driver)
        with allure.step("导航到知识库"):
            logging.info("等待页面加载完成")
            assert kb_page.navigate_knowledge(),"导航到知识库失败"
    
    # @allure.story("创建知识库")
    # @allure.description("验证用户能否成功创建新的知识库")
    # @pytest.mark.usefixtures("logged_in_driver")
    # def test_create_knowledge_base(self, logged_in_driver):
    #     kb_name = f"测试知识库_{time.strftime('%Y%m%d_%H%M%S')}"
    #     kb_desc = "这是一个自动化测试创建的知识库"
    #     kb_page = KnowledgeBasePage(logged_in_driver)
        
    #     with allure.step(f"创建知识库: {kb_name}"):
    #         logging.info("等待页面加载完成")
    #         result = kb_page.create_knowledge_base(kb_name, kb_desc)
    #         allure.attach(
    #             logged_in_driver.get_screenshot_as_png(),
    #             name="创建知识库结果",
    #             attachment_type=allure.attachment_type.PNG
    #         )
    #         assert result, "创建知识库失败"
    
    # @allure.story("编辑知识库")
    # @allure.description("验证用户能否成功编辑现有知识库")
    # @pytest.mark.usefixtures("logged_in_driver")
    # def test_edit_knowledge_base(self, logged_in_driver):
    #     kb_page = KnowledgeBasePage(logged_in_driver)
    #     new_name = f"编辑的知识库_{time.strftime('%Y%m%d_%H%M%S')}"
    #     new_desc = "这是编辑后的知识库描述"
        
    #     with allure.step(f"编辑知识库为: {new_name}"):
    #         result = kb_page.edit_knowledge_base(new_name, new_desc)
    #         allure.attach(
    #             logged_in_driver.get_screenshot_as_png(),
    #             name="编辑知识库结果",
    #             attachment_type=allure.attachment_type.PNG
    #         )
    #         assert result, "编辑知识库失败"
            
    #     with allure.step("验证编辑结果"):
    #         current_name = kb_page.get_first_kb_name()
    #         assert new_name in current_name, f"知识库名称未更新，当前名称: {current_name}"
