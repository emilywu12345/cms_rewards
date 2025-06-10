import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from page_objects.base_page import BasePage
from utils.log_manager import logger

class LoginPage(BasePage):
    """登入頁面操作封裝"""

    # 正常登入元素定位
    USERNAME_INPUT = (By.CSS_SELECTOR, '.el-input__inner[type="text"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '.el-input__inner[type="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.el-button--primary')
    MODEL_MENU = (By.XPATH, '/html/body/div[1]/div/div[1]/div/ul/li[2]/div/span')

    @allure.step("執行正常登入操作")
    def login(self, username: str, password: str, timeout: int = 30) -> bool:
        try:
            logger.info(f"登入操作: {username}")
            self.open()
            # 輸入賬號密碼
            self.input_text(self.USERNAME_INPUT, username)
            self.input_text(self.PASSWORD_INPUT, password)
            # 點擊登入按鈕
            self.click(self.LOGIN_BUTTON)
            # 等待AI模型菜單出現
            if not self.wait_for_element(self.MODEL_MENU, timeout=timeout):
                logger.error("登入失敗: 未找到AI模型菜單")
                self.take_screenshot("登入失敗")
                return False
            logger.info("登入成功")
            return True
        except NoSuchElementException as e:
            logger.error(f'登入失敗: 元素未找到 - {str(e)}')
            self.take_screenshot("登入失敗")
            return False
        except TimeoutException as e:
            logger.error(f'登入失敗: 等待元素超時 - {str(e)}')
            self.take_screenshot("登入失敗")
            return False
        except Exception as e:
            logger.error(f"登入失敗: 發生未知異常 - {str(e)}")
            self.take_screenshot("登入異常")
            return False


