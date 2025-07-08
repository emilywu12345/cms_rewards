from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from utils.log_manager import logger
from utils.config_manager import ConfigManager


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.config = ConfigManager.get_instance()
        self.timeout = self.config.get_wait_time('medium')
        self.base_url = self.config.get_base_url()
        
    def open(self):
        self.driver.get(self.base_url)
        
    def find_element(self, locator, timeout=None):
        """等待并查找元素"""
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"元素定位失败: {locator}")
            self.take_screenshot("element_not_found")
            raise
    
    def find_elements(self, locator, timeout=None):
        """等待并查找多个元素"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            logger.error(f"元素定位失败: {locator}")
            return []
            
    def click(self, locator, timeout=None):
        """点击元素"""
        self.find_element(locator, timeout).click()
        
    def input_text(self, locator, text, clear=True, timeout=None):
        """输入文本"""
        element = self.find_element(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)
        
    def get_text(self, locator, timeout=None):
        """获取元素文本"""
        return self.find_element(locator, timeout).text
        
    def wait_for_element(self, locator, timeout=None):
        """等待元素可见"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception as e:
            logger.error(f"等待元素失败: {locator} - {str(e)}")
            return False
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """等待元素可点击"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            return True
        except Exception as e:
            logger.error(f"等待元素可点击失败: {locator} - {str(e)}")
            return False

    def take_screenshot(self, name):
        """
        调用全局 screenshot 管理器进行截图
        """
        from utils.screenshot_manager import screenshot
        screenshot.take_screenshot(self.driver, name)
        
    def wait_and_click(self, locator, timeout=None):
        """等待元素出现并点击"""
        if self.wait_for_element_clickable(locator, timeout):
            self.click(locator, timeout)
            return True
        return False
    
    
    def wait_loading_disappear(self, timeout=15):
        """
        等待全局 loading 遮罩消失（适配 element-ui/el-loading-mask)
        """
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.el-loading-mask'))
            )
            return True
        except Exception as e:
            logger.warning(f"等待 loading 遮罩消失超时: {str(e)}")
            return False
            
    def handle_exception(self, e, action_name=""):
        """
        统一处理页面操作异常
        :param e: 异常对象
        :param action_name: 操作名称
        """
        from selenium.common.exceptions import NoSuchElementException, TimeoutException
        
        error_msg = f'{action_name}失败' if action_name else '操作失败'
        
        if isinstance(e, NoSuchElementException):
            logger.error(f'{error_msg}: 元素未找到 - {str(e)}')
            self.take_screenshot(f"{action_name}_元素未找到")
        elif isinstance(e, TimeoutException):
            logger.error(f'{error_msg}: 等待元素超时 - {str(e)}')
            self.take_screenshot(f"{action_name}_等待元素超时")
        else:
            logger.error(f"{error_msg}: 发生未知异常 - {str(e)}")
            self.take_screenshot(f"{action_name}_发生未知异常")
        return False