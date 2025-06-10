import pytest
import allure
import time
import logging
from page_objects.knowledge_page import KnowledgePage
from utils.config_manager import ConfigManager

@allure.feature("知识库管理")
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
        场景：导航到知识库首页
        步骤：
        1. 通过 KnowledgePage 进行导航
        2. 断言页面跳转成功
        """
        kb_page = KnowledgePage(self.driver)
        with allure.step("导航到知识库"):
            logging.info("等待页面加载完成")
            assert kb_page.navigate_knowledge(),"导航到知识库失败"

    @allure.story("导航到知识库")
    def test_2_navigate_model(self):
        """
        场景：再次导航到知识库，验证页面可重复进入
        """
        kb_page = KnowledgePage(self.driver)
        with allure.step("导航到知识库"):
            logging.info("等待页面加载完成")
            assert kb_page.navigate_model(),"导航到知识库失败"
    
    # 以下为扩展用例模板，后续可根据实际业务需求补充实现
    #
    # @allure.story("创建知识库")
    # @allure.description("验证用户能否成功创建新的知识库")
    # @pytest.mark.usefixtures("logged_in_driver")
    # def test_create_knowledge_base(self, logged_in_driver):
    #     """
    #     场景：创建新知识库
    #     步骤：
    #     1. 输入知识库名称和描述
    #     2. 提交并断言创建成功
    #     """
    #     kb_name = f"测试知识库_{time.strftime('%Y%m%d_%H%M%S')}"
    #     kb_desc = "这是一个自动化测试创建的知识库"
    #     kb_page = KnowledgeBasePage(logged_in_driver)
    #     
    #     with allure.step(f"创建知识库: {kb_name}"):
    #         logging.info("等待页面加载完成")
    #         result = kb_page.create_knowledge_base(kb_name, kb_desc)
    #         allure.attach(
    #             logged_in_driver.get_screenshot_as_png(),
    #             name="创建知识库结果",
    #             attachment_type=allure.attachment_type.PNG
    #         )
    #         assert result, "创建知识库失败"
    #
    # @allure.story("编辑知识库")
    # @allure.description("验证用户能否成功编辑现有知识库")
    # @pytest.mark.usefixtures("logged_in_driver")
    # def test_edit_knowledge_base(self, logged_in_driver):
    #     """
    #     场景：编辑知识库
    #     步骤：
    #     1. 修改知识库名称和描述
    #     2. 提交并断言编辑成功
    #     3. 验证修改结果
    #     """
    #     kb_page = KnowledgeBasePage(logged_in_driver)
    #     new_name = f"编辑的知识库_{time.strftime('%Y%m%d_%H%M%S')}"
    #     new_desc = "这是编辑后的知识库描述"
    #     
    #     with allure.step(f"编辑知识库为: {new_name}"):
    #         result = kb_page.edit_knowledge_base(new_name, new_desc)
    #         allure.attach(
    #             logged_in_driver.get_screenshot_as_png(),
    #             name="编辑知识库结果",
    #             attachment_type=allure.attachment_type.PNG
    #         )
    #         assert result, "编辑知识库失败"
    #         
    #     with allure.step("验证编辑结果"):
    #         current_name = kb_page.get_first_kb_name()
    #         assert new_name in current_name, f"知识库名称未更新，当前名称: {current_name}"
