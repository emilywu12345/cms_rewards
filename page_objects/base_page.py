from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.log_manager import logger
from utils.screenshot_manager import screenshot
from utils.config_manager import ConfigManager


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.config = ConfigManager.get_instance()
        self.timeout = self.config.get_wait_time('medium')
        self.base_url = self.config.get_base_url()
        
    def open(self):
        self.driver.get(self.base_url)
        
    def find_element(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"元素定位失败: {locator}")
            screenshot(self.driver, "element_not_found")
            raise
            
    def click(self, locator):
        self.find_element(locator).click()
        
    def input_text(self, locator, text):
        self.find_element(locator).send_keys(text)
        
    def wait_for_element(self, locator, timeout=None):
        """等待元素可见"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception as e:
            logger.error(f"等待元素失败: {locator} - {str(e)}")
            return False

    def take_screenshot(self, name):
        screenshot.take_screenshot(self.driver, name)
        
    def wait_and_click(self, locator, timeout=None):
        """等待元素出现并点击"""
        if self.wait_for_element(locator, timeout):
            self.click(locator)
            return True
        return False