import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from page_objects.base_page import BasePage
from utils.log_manager import logger

class LoginPage(BasePage):
    """登录页面操作"""

    # 正常登录元素定位
    USERNAME_INPUT = (By.XPATH, '//input[@id="username"]')
    PASSWORD_INPUT = (By.XPATH, '//input[@id="password"]')
    LOGIN_BUTTON = (By.XPATH, '//button[@type="submit" and contains(@class, "ant-btn") and contains(@class, "ant-btn-block")]')
    COLLECT_GIFT_BUTTON = (By.XPATH, '//button[@type="button" and contains(@class, "sino-btn") and span[text()="Collect Gift"]]')

    @allure.step("执行正常登录操作")
    def login(self, username: str, password: str, timeout: int = 30) -> bool:
        try:
            logger.info(f"登录操作: {username}")
            self.open()
            # 先等待loading遮罩消失
            self.wait_loading_disappear(timeout=15)
            # 输入账号密码
            self.input_text(self.USERNAME_INPUT, username)
            self.input_text(self.PASSWORD_INPUT, password)
            # 点击登录按钮
            self.click(self.LOGIN_BUTTON)
            # 等待Collect Gift按鈕出现
            if not self.wait_for_element(self.COLLECT_GIFT_BUTTON, timeout=timeout):
                logger.error("登录失败: 未找到Collect Gift按鈕")
                self.take_screenshot("登录失败")
                return False
            logger.info("登录成功")
            self.take_screenshot("登录成功")
            return True
        except Exception as e:
            return self.handle_exception(e, "登录操作")


