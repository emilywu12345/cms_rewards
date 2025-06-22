import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from page_objects.base_page import BasePage
from utils.log_manager import logger

class LoginPage(BasePage):
    """登录页面操作封装"""

    # 正常登录元素定位
    USERNAME_INPUT = (By.CSS_SELECTOR, '.el-input__inner[type="text"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '.el-input__inner[type="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.el-button--primary')
    MODEL_MENU = (By.XPATH, '/html/body/div[1]/div/div[1]/div/ul/li[2]/div/span')

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
            # 等待 AI 模型菜单出现
            if not self.wait_for_element(self.MODEL_MENU, timeout=timeout):
                logger.error("登录失败: 未找到 AI 模型菜单")
                self.take_screenshot("登录失败")
                return False
            logger.info("登录成功")
            return True
        except NoSuchElementException as e:
            logger.error(f'登录失败: 元素未找到 - {str(e)}')
            self.take_screenshot("登录失败")
            return False
        except TimeoutException as e:
            logger.error(f'登录失败: 等待元素超时 - {str(e)}')
            self.take_screenshot("登录失败")
            return False
        except Exception as e:
            logger.error(f"登录失败: 发生未知异常 - {str(e)}")
            self.take_screenshot("登录异常")
            return False


