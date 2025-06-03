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
        """使用賬號密碼登入系統
        :param username: 登入賬號
        :param password: 登入密碼
        :param timeout: 等待超時時間
        :return: 登入是否成功
        """
        try:
            logger.info(f"登入操作: {username}")

            # 打開登入頁面
            self.open()

            # 輸入賬號密碼
            self.send_keys(self.USERNAME_INPUT, username)
            self.send_keys(self.PASSWORD_INPUT, password)

            # 點擊登入按鈕
            self.click(self.LOGIN_BUTTON)

            # 等待AI模型菜單出現
            logger.info("等待AI模型菜單出現...")
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.MODEL_MENU))
            time.sleep(1) 
            logger.info("登入成功: 檢測到AI模型菜單")
            self.take_screenshot("登入成功")
            return True  # 登入成功

        # 当使用 find_element 或 find_elements 方法尝试查找页面上的元素，但元素不存在时，会抛出此异常
        except NoSuchElementException as e:
            logger.error(f'登入失敗: 元素未找到 - {str(e)}')
            self.take_screenshot("登入失敗")
            return False

        # 当使用显式等待（如 WebDriverWait）等待某个元素或条件出现，但超过了指定的超时时间仍未满足条件时，会抛出此异常
        except TimeoutException as e:
            logger.error(f'登入失敗: 等待元素超時 - {str(e)}')
            self.take_screenshot("登入失敗")
            return False

        # 当上述两种特定异常（NoSuchElementException 和 TimeoutException）都不匹配时，会进入这个块来处理其他未知的异常
        except Exception as e:
            logger.error(f"登入失敗: 發生未知異常 - {str(e)}")
            self.take_screenshot("登入異常")
            return False
        

