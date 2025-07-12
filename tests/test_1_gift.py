"""
Gift功能测试用例
测试Gift的创建功能
"""

import pytest
import allure
import time
from selenium.webdriver.common.by import By
from page_objects.gift_page import GiftPage
from data.test_data import GIFT_TEST_DATA, COPY_GIFT_TEST_DATA
from utils.log_manager import logger


@allure.epic("Gift管理")
@allure.feature("Gift功能")
class TestGift:
    """Gift功能测试类"""

    def setup_method(self):
        """每个测试方法执行前的设置"""
        logger.info("开始Gift功能测试")

    def teardown_method(self):
        """每个测试方法执行后的清理"""
        logger.info("Gift功能测试完成")

    @allure.story("创建Gift")
    @allure.title("测试创建Gift功能")
    @allure.description("测试用户是否能够成功创建Gift")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.run(order=1)  # 第一个执行
    def test_add_gift(self, session_logged_in_driver):
        """
        测试User能否正常创建Gift
        
        步骤:
        1. 打开Gift列表页面
        2. 点击Add按钮
        3. 打开Gift创建页面
        4. 输入Gift的基本信息
        5. 点击提交按钮
        6. 验证Gift是否成功创建
        """

        logger.info("开始测试创建Gift")

        # 初始化Gift页面对象
        gift_page = GiftPage(session_logged_in_driver)
        
        # 获取测试数据
        add_gift_data = GIFT_TEST_DATA["add_auto_gift"]

        # 执行创建Gift操作
        result = gift_page.add_gift(add_gift_data)
        
        # 验证结果
        assert result, "创建Gift失败"
        logger.info("Gift创建测试通过")


    @allure.story("Copy Gift")
    @allure.title("测试Copy Gift功能")
    @allure.description("测试用户是否能够成功Copy Gift")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.run(order=2)  # 第二个执行
    def test_copy_gift(self, session_logged_in_driver):
        """
        测试User能否正常Copy Gift
        
        步骤:
        1. 进入Gift列表页面
        2. 找到需要Copy的Gift
        3. 点击Copy按钮
        4. 打开Gift detail页面
        5. 输入Gift的基本信息
        6. 点击提交按钮
        7. 验证Gift是否成功 Copy
        """

        logger.info("开始测试Copy Gift")

        # 初始化Gift页面对象
        gift_page = GiftPage(session_logged_in_driver)
        
        # 获取测试数据
        copy_gift_data = COPY_GIFT_TEST_DATA["copy_auto_gift"]
        add_gift_data = GIFT_TEST_DATA["add_auto_gift"]

        # 执行创建Gift操作
        result = gift_page.copy_gift(copy_gift_data,add_gift_data)

        # 验证结果
        assert result, "Copy Gift失败"
        logger.info("Gift Copy测试通过")