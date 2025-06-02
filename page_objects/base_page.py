"""基础页面对象类

此类为所有页面对象提供基础功能，包括：
- 元素定位和交互
- 等待机制
- 错误处理
- 截图功能
"""

from typing import Tuple, Any
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from selenium.webdriver import ActionChains
from utils.config_manager import ConfigManager
from utils.log_manager import logger
from utils.screenshot_manager import screenshot


class BasePage:
    """页面对象基类"""

    def __init__(self, driver):
        """
        初始化基础页面对象
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.config = ConfigManager.get_instance()
        self.wait_times = self.config.get_test_config().get('wait', {
            'short': 5,
            'medium': 10, 
            'long': 30
        })
        self.timeout = self.wait_times['medium']
        self.base_url = self.config.get_base_url()
        self.action_chains = ActionChains(driver)

    def open(self, url: str = None) -> None:
        """
        打开页面
        
        Args:
            url: 要打开的URL，如果未指定则使用base_url
        """
        target_url = url or self.base_url
        try:
            logger.info(f"打开页面: {target_url}")
            self.driver.get(target_url)
        except Exception as e:
            logger.error(f"打开页面失败: {str(e)}")
            screenshot.take_screenshot(self.driver, "page_load_error")
            raise

    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> Any:
        """
        查找单个元素
        
        Args:
            locator: 元素定位器元组 (定位方式, 定位表达式)
            timeout: 超时时间（秒）
            
        Returns:
            找到的元素
            
        Raises:
            TimeoutException: 在指定时间内未找到元素
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"元素未找到: {locator}")
            screenshot.take_screenshot(self.driver, "element_not_found")
            raise
        except Exception as e:
            logger.error(f"查找元素时发生错误: {str(e)}")
            screenshot.take_screenshot(self.driver, "element_find_error")
            raise

    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> list:
        """
        查找多个元素
        
        Args:
            locator: 元素定位器元组
            timeout: 超时时间（秒）
            
        Returns:
            找到的元素列表
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            logger.warning(f"未找到任何元素: {locator}")
            return []
        except Exception as e:
            logger.error(f"查找元素时发生错误: {str(e)}")
            return []

    def click(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        点击元素
        
        Args:
            locator: 元素定位器元组
            timeout: 超时时间（秒）
            
        Returns:
            bool: 点击是否成功
        """
        try:
            element = self.wait_for_clickable(locator, timeout)
            element.click()
            return True
        except ElementClickInterceptedException:
            logger.error("元素被遮挡，无法点击")
            screenshot.take_screenshot(self.driver, "click_intercepted")
            return False
        except Exception as e:
            logger.error(f"点击元素失败: {str(e)}")
            screenshot.take_screenshot(self.driver, "click_error")
            return False

    def input_text(self, locator: Tuple[str, str], text: str, clear: bool = True, timeout: int = None) -> bool:
        """
        向输入框输入文本
        
        Args:
            locator: 元素定位器元组
            text: 要输入的文本
            clear: 是否先清空输入框
            timeout: 超时时间（秒）
            
        Returns:
            bool: 输入是否成功
        """
        try:
            element = self.find_element(locator, timeout)
            if clear:
                element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            logger.error(f"输入文本失败: {str(e)}")
            screenshot.take_screenshot(self.driver, "input_error")
            return False

    def wait_for_element(self, locator: Tuple[str, str], timeout: int = None, visible: bool = True) -> bool:
        """
        等待元素出现
        
        Args:
            locator: 元素定位器元组
            timeout: 超时时间（秒）
            visible: 是否要求元素可见
            
        Returns:
            bool: 元素是否出现
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            if visible:
                wait.until(EC.visibility_of_element_located(locator))
            else:
                wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            logger.warning(f"等待元素超时: {locator}")
            return False
        except Exception as e:
            logger.error(f"等待元素时发生错误: {str(e)}")
            return False

    def wait_for_clickable(self, locator: Tuple[str, str], timeout: int = None) -> Any:
        """
        等待元素可点击
        
        Args:
            locator: 元素定位器元组
            timeout: 超时时间（秒）
            
        Returns:
            可点击的元素
            
        Raises:
            TimeoutException: 在指定时间内元素未变为可点击状态
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            logger.error(f"元素未变为可点击状态: {locator}")
            screenshot.take_screenshot(self.driver, "element_not_clickable")
            raise
        except Exception as e:
            logger.error(f"等待元素可点击时发生错误: {str(e)}")
            screenshot.take_screenshot(self.driver, "wait_clickable_error")
            raise

    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """
        获取元素文本
        
        Args:
            locator: 元素定位器元组
            timeout: 超时时间（秒）
            
        Returns:
            元素的文本内容
        """
        try:
            element = self.find_element(locator, timeout)
            return element.text
        except Exception as e:
            logger.error(f"获取元素文本失败: {str(e)}")
            return ""

    def is_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        检查元素是否可见
        
        Args:
            locator: 元素定位器元组 (定位方式, 定位值)
            timeout: 超时时间(秒)
            
        Returns:
            bool: 是否可见
        """
        try:
            return self.wait_for_element_visible(locator, timeout)
        except Exception as e:
            logger.error(f"检查元素可见性失败: {str(e)}")
            return False

    def take_screenshot(self, name: str) -> None:
        """
        获取页面截图
        
        Args:
            name: 截图名称
        """
        screenshot.take_screenshot(self.driver, name)

    def mouse_hover(self, locator: Tuple[str, str]) -> bool:
        """
        在元素上执行鼠标悬停操作
        
        Args:
            locator: 元素定位器元组 (定位方式, 定位值)
            
        Returns:
            bool: 操作是否成功
        """
        try:
            element = self.find_element(locator)
            self.action_chains.move_to_element(element).perform()
            return True
        except Exception as e:
            logger.error(f"鼠标悬停失败: {str(e)}")
            self.take_screenshot("mouse_hover_failed")
            return False

    def wait_for_url_contains(self, text: str, timeout: int = None) -> bool:
        """
        等待URL包含指定文本
        
        Args:
            text: 要等待的文本
            timeout: 超时时间(秒)
            
        Returns:
            bool: 是否成功
        """
        try:
            timeout = timeout or self.timeout
            WebDriverWait(self.driver, timeout).until(
                lambda driver: text in driver.current_url.lower()
            )
            return True
        except TimeoutException:
            logger.warning(f"等待URL包含 {text} 超时")
            return False
        except Exception as e:
            logger.error(f"等待URL错误: {str(e)}")
            return False

    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        等待元素可见
        
        Args:
            locator: 元素定位器元组 (定位方式, 定位值)
            timeout: 超时时间(秒)
            
        Returns:
            bool: 是否可见
        """
        try:
            timeout = timeout or self.timeout
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            logger.warning(f"等待元素超时: {locator}")
            return False
        except Exception as e:
            logger.error(f"等待元素错误: {str(e)}")
            return False