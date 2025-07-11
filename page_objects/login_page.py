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
    def login(self, username: str, password: str, timeout: int = 15) -> bool:  # 减少默认超时
        try:
            logger.info(f"登录操作: {username}")
            self.open()
            
            # 等待页面完全加载
            time.sleep(2)

            # 输入账号密码
            username_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.USERNAME_INPUT)
            )
            username_element.send_keys(username)
            password_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.PASSWORD_INPUT)
            )
            password_element.send_keys(password)

            # 点击登录按钮
            self.click(self.LOGIN_BUTTON)
            
            # 等待登录结果 - Collect Gift按钮出现
            self.wait_for_element(self.COLLECT_GIFT_BUTTON, timeout=timeout)
            return True
        except Exception as e:
            return self.handle_exception(e, "登录操作")