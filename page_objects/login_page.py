import allure
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from page_objects.base_page import BasePage
from utils.log_manager import logger

class LoginPage(BasePage):
    """登入頁面類，包含所有登入相關元素定位操作""" 
    USERNAME_INPUT = (By.CSS_SELECTOR, '.el-input__inner[type="text"]')  # 使用者名稱輸入框
    PASSWORD_INPUT = (By.CSS_SELECTOR, '.el-input__inner[type="password"]')  # 密碼輸入框
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.el-button--primary')  # 登入按鈕
    MODEL_MENU = (By.XPATH, '0/html/body/div[1]/div/div[1]/div/ul/li[2]/div/span')  # 點擊AI模型

    @allure.step("執行登入操作")
    def login(self, username: str, password: str) -> bool:
        """执行登录操作"""
        try:
            logger.info(f"開始登入操作: {username}")
            
            # 打開登入頁面
            self.open()
            
            # 輸入帳號密碼
            self.find_element(self.USERNAME_INPUT).send_keys(username)
            self.find_element(self.PASSWORD_INPUT).send_keys(password)
            
            # 點擊登入按鈕
            self.find_element(self.LOGIN_BUTTON).click()
            
            # 等待AI模型菜單出現
            if self.wait_for_element(self.MODEL_MENU, timeout=10):
                self.find_element(self.MODEL_MENU).click()
                return True  # 登入成功
            else:
                logger.error('登入失敗: 未找到AI模型菜單')
                self.take_screenshot("登入失敗")
                return False

        except NoSuchElementException as e:
            logger.error(f'登入失敗: 元素未找到 - {str(e)}')
            self.take_screenshot("登入失敗")
            return False

        except Exception as e:
            logger.error(f"登入過程發生異常: {str(e)}")
            self.take_screenshot("登入異常")
            return False
