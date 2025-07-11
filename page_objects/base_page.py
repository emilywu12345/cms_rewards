from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from utils.log_manager import logger
from utils.config_manager import ConfigManager
from datetime import datetime
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
        
    def clear_input(self, locator, timeout=None):
        """仅清空输入框"""
        element = self.find_element(locator, timeout)
        element.clear()
        time.sleep(0.2)  # 小延迟确保清空完成

    def input_text(self, locator, text, timeout=None):
        """仅输入文本"""
        element = self.find_element(locator, timeout)
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

        self.take_screenshot(self.driver, f"{action_name}_异常截图")
        return False

    def set_form_value(self, value, date_icon_locator, picker_type):
        """
        设置表单字段的值
        :param value: 要设置的值
        :param type: 字段类型
        """
        try:
            if picker_type == 'RangePicker':
                logger.info("设置 RangePicker 日期范围: %s", value)
                # 先点击日期选择器图标激活组件
                self.driver.find_element(*date_icon_locator).click()
                # 等待日期选择器激活
                time.sleep(2)

                # 後期優化 -----------
                start_date = value[0]
                end_date = value[1]  

                # 解析为 datetime 对象（注意格式匹配）
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")


                # 格式化为目标字符串 (Windows兼容格式)
                start_date_formatted_date = start_date_obj.strftime("%B %d, %Y").replace(' 0', ' ')
                end_date_formatted_date = end_date_obj.strftime("%B %d, %Y").replace(' 0', ' ')

                logger.info(f"设置 RangePicker 日期范围: {start_date_formatted_date} - {end_date_formatted_date}")
            
                # 当天日期按钮的 XPath，点击当天日期按钮
                start_date_button = (By.XPATH, "//table[@class='ant-calendar-table']//td[contains(@title, '" + start_date_formatted_date + "')]")
                end_date_button = (By.XPATH, "//table[@class='ant-calendar-table']//td[contains(@title, '" + end_date_formatted_date + "')]")

                logger.info(f"点击开始日期按钮: {start_date_button}, 结束日期按钮: {end_date_button}")
                self.driver.find_element(*start_date_button).click()
                self.driver.find_element(*end_date_button).click()

            elif picker_type == 'DatePicker':
                logger.info("设置 DatePicker 日期: %s", value)
                # 先点击日期选择器图标激活组件
                self.driver.find_element(*date_icon_locator).click()
                # 等待日期选择器激活
                time.sleep(2)
                date_obj = value[0]

                # 解析为 datetime 对象（注意格式匹配）
                date_obj = datetime.strptime(date_obj, "%Y-%m-%d")

                # 格式化为目标字符串 (Windows兼容格式)
                date_formatted = date_obj.strftime("%B %d, %Y").replace(' 0', ' ')

                logger.info(f"设置 DatePicker 日期: {date_formatted}")

                # 当天日期按钮的 XPath，点击当天日期按钮
                date_button = (By.XPATH, "//table[@class='ant-calendar-table']//td[contains(@title, '" + date_formatted + "')]")

                logger.info(f"点击日期按钮: {date_button}")
                self.driver.find_element(*date_button).click()
            return True
        except Exception as e:
            self.handle_exception(e, f"设置{picker_type}值")
            return False
        


    def scroll_to_element(self, locator=None, element=None, timeout=15) -> bool:
        """
        滚动到指定元素使其可见
        
        Args:
            locator: 元素定位器元组 (By.ID, "element_id")
            element: 已找到的WebElement对象
            timeout: 等待元素的超时时间
        
        Returns:
            操作成功返回True，失败返回False
        """
        try:
            # 根据传入参数选择元素获取方式
            target_element = element
            if locator and not element:
                target_element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
            
            if not target_element:
                raise ValueError("必须提供locator或element参数之一")
                
            # 滚动到元素
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                target_element
            )
            # 等待页面滚动完成
            time.sleep(1)
            return True
            
        except TimeoutException:
            logger.error(f"等待元素超时: {locator}")
            return False
        except ValueError as e:
            logger.error(str(e))
            return False
        except Exception as e:
            logger.error(f"滚动到元素时出错: {e}")
            return False

    def upload_thumbnail(self, file_path: str, element_id: str = "thumbnailImage") -> bool:
        """
        上传图片到指定元素
        
        Args:
            file_path: 图片文件的完整路径
            element_id: 上传元素的ID，默认为"thumbnailImage"
        
        Returns:
            上传成功返回True，失败返回False
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                return False
                
            # 查找上传元素并发送文件路径
            upload_element = self.driver.find_element(By.ID, element_id)
            upload_element.send_keys(file_path)
            
            logger.info(f"成功上传图片: {os.path.basename(file_path)}")
            return True
            
        except FileNotFoundError:
            logger.error(f"文件未找到: {file_path}")
            return False
        except NoSuchElementException:
            logger.error(f"找不到上传元素: ID={element_id}")
            return False
        except WebDriverException as e:
            logger.error(f"WebDriver操作异常: {e}")
            return False
        except Exception as e:
            logger.error(f"上传图片时发生未知错误: {e}")
            return False

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
            
            # 等待用户名输入框可见
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.USERNAME_INPUT)
            )
            logger.info("登录页面准备就绪")
                        
        except TimeoutException:
            logger.warning(f"等待页面准备超时({timeout}秒)，继续执行")