"""登录页面对象类

此类负责页面的所有登录相关操作，包括：
- 用户登录
- 检查登录状态
- 错误处理
"""

import allure
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from page_objects.base_page import BasePage
from utils.log_manager import logger

class LoginPage(BasePage):
    """登录页面类，包含所有登录相关元素定位和操作"""    # 页面元素定位器
    USERNAME_INPUT = (By.CSS_SELECTOR, '.el-input__inner[type="text"]')  # 用户名输入框
    PASSWORD_INPUT = (By.CSS_SELECTOR, '.el-input__inner[type="password"]')  # 密码输入框
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.el-button--primary')  # 登录按钮
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.el-message--success')  # 登录成功提示
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.el-message--error')  # 登录失败提示
    TITLE_MESSAGE = (By.CSS_SELECTOR, '.dashboard-title')  # 更新主页标题选择器

    def __init__(self, driver):
        """初始化登录页面对象"""
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 10)  # 使用固定的超时时间

    @allure.step("执行登录操作")
    def login(self, username: str, password: str) -> bool:
        """
        执行登录操作
        Args:
            username: 用户名
            password: 密码
        Returns:
            bool: 登录是否成功
        """
        try:
            logger.info(f"开始登录操作: {username}")
            
            # 打开登录页面
            self.open()
            
            # 输入账号密码
            self.find_element(self.USERNAME_INPUT).send_keys(username)
            self.find_element(self.PASSWORD_INPUT).send_keys(password)
            
            # 点击登录按钮
            self.find_element(self.LOGIN_BUTTON).click()
            
            # 等待登录结果
            try:
                if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
                    error_text = self.get_text(self.ERROR_MESSAGE)
                    logger.error(f"登录失败: {error_text}")
                    return False
                
                # 等待主页标题出现
                self.wait_for_element(self.TITLE_MESSAGE)
                logger.info("登录成功")
                return True
                
            except TimeoutException:
                logger.error("登录超时")
                return False
                
        except Exception as e:
            logger.error(f"登录过程发生异常: {str(e)}")
            self.take_screenshot("登录异常")
            return False

