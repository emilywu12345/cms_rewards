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
            self._wait_for_page_ready()
            
            # 等待用户名输入框出现并输入
            self._input_with_wait(self.USERNAME_INPUT, username, "用户名")
            
            # 等待密码输入框出现并输入
            self._input_with_wait(self.PASSWORD_INPUT, password, "密码")
            
            # 点击登录按钮
            logger.info("点击登录按钮")
            self.click(self.LOGIN_BUTTON)
            
            # 等待登录结果 - Collect Gift按钮出现
            if not self.wait_for_element(self.COLLECT_GIFT_BUTTON, timeout=timeout):
                logger.error("登录失败: 未找到Collect Gift按钮")
                self.take_screenshot("登录失败")
                return False
                
            logger.info("登录成功")
            self.take_screenshot("登录成功")
            return True
            
        except Exception as e:
            return self.handle_exception(e, "登录操作")
    
    def _wait_for_page_ready(self, timeout: int = 10):
        """等待页面准备就绪"""
        try:
            # 等待DOM加载完成
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.info("页面DOM加载完成")
            
            # 等待可能的loading遮罩消失 - 减少等待时间
            self.wait_loading_disappear(timeout=5)
            
            # 等待用户名输入框可见 - 这是页面准备好的标志
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.USERNAME_INPUT)
            )
            logger.info("登录页面准备就绪")
            
        except TimeoutException:
            logger.warning(f"等待页面准备超时({timeout}秒)，继续执行")
    
    def _input_with_wait(self, locator: tuple, text: str, field_name: str, timeout: int = 5):
        """等待元素可见并输入文本"""
        try:
            logger.info(f"等待{field_name}输入框")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.clear()
            element.send_keys(text)
            logger.info(f"成功输入{field_name}")
        except TimeoutException:
            logger.error(f"等待{field_name}输入框超时")
            raise


