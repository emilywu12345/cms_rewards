"""
礼物功能测试用例
测试礼物的创建、编辑等功能
"""

import pytest
import allure
import time
from selenium.webdriver.common.by import By
from page_objects.gift_page import GiftPage
from data.gift_data import GIFT_TEST_DATA
from utils.log_manager import logger


@allure.epic("礼物管理")
@allure.feature("礼物功能")
class TestGift:
    """礼物功能测试类"""

    def setup_method(self):
        """每个测试方法执行前的设置"""
        logger.info("开始礼物功能测试")

    def teardown_method(self):
        """每个测试方法执行后的清理"""
        logger.info("礼物功能测试完成")

    @allure.story("添加礼物")
    @allure.title("测试添加基础礼物功能")
    @allure.description("测试用户是否能够成功填写礼物基本信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_basic_gift(self, session_logged_in_driver):
        """测试添加基础礼物"""
        logger.info("开始测试添加基础礼物")
        
        # 初始化礼物页面对象
        gift_page = GiftPage(session_logged_in_driver)
        
        # 获取测试数据
        gift_data = GIFT_TEST_DATA["auto_gift_1"]
        
        # 执行添加礼物操作
        result = gift_page.add_gift(gift_data)
        
        # 验证结果
        assert result, "添加基础礼物失败"
        logger.info("基础礼物添加测试通过")