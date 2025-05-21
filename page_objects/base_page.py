from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import logger
from utils.screenshot import take_screenshot
import configparser
import os


config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.ini')
config.read(config_path)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = int(config['ENV']['timeout'])
        self.base_url = config['ENV']['base_url']
        
    def open(self):
        self.driver.get(self.base_url)
        
    def find_element(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"元素定位失败: {locator}")
            take_screenshot(self.driver, "element_not_found")
            raise
            
    def wait_and_click(self, locator):
        """等待元素可点击并点击"""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except Exception as e:
            logger.error(f"点击元素失败: {locator}, 错误: {str(e)}")
            take_screenshot(self.driver, "click_failed")
            return False

    def wait_for_element(self, locator):
        """等待元素出现"""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            logger.error(f"等待元素超时: {locator}")
            take_screenshot(self.driver, "wait_timeout")
            return False

    def input_text(self, locator, text):
        """输入文本"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            logger.error(f"输入文本失败: {locator}, 错误: {str(e)}")
            take_screenshot(self.driver, "input_failed")
            return False

    def is_element_visible(self, locator):
        """检查元素是否可见"""
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except:
            return False

    def get_text(self, locator):
        """获取元素文本"""
        try:
            element = self.find_element(locator)
            return element.text
        except:
            return ""

    def click(self, locator):
        """点击元素"""
        try:
            element = self.find_element(locator)
            element.click()
            return True
        except Exception as e:
            logger.error(f"点击元素失败: {locator}, 错误: {str(e)}")
            take_screenshot(self.driver, "click_failed")
            return False