import logging
from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    USERNAME_INPUT = ('xpath', '/html/body/div/div/div/div[2]/form/div[1]/div[1]/div/div/div/input')
    PASSWORD_INPUT = ('xpath', '/html/body/div/div/div/div[2]/form/div[1]/div[2]/div/div/div/input')
    LOGIN_BUTTON = ('xpath', '/html/body/div/div/div/div[2]/form/button')
    TITLE_MESSAGE = ('xpath', '/html/body/div[1]/div/main/div[1]/div/div[1]/div/div/div/div')
    ERROR_MESSAGE = ('xpath', '//div[contains(@class, "error-message")]')
    
    
    def login(self, username, password):
        try:
            logging.info('开始登录流程')
            self.open()
            logging.info(f'输入用户名: {username}')
            self.input_text(self.USERNAME_INPUT, username)
            logging.info('输入密码')
            self.input_text(self.PASSWORD_INPUT, password)
            logging.info('点击登录按钮')
            self.click(self.LOGIN_BUTTON)
            logging.info('等待页面加载完成')
            self.driver.implicitly_wait(10)
            if self.is_element_visible(self.TITLE_MESSAGE):
                self.click(self.TITLE_MESSAGE)
                logging.info('登录流程执行完成')
                return True
            else:
                logging.error('未找到登录成功后的页面元素')
                self.getScreenShot('登入失敗')
                return False
        except NoSuchElementException as e:
            logging.error(f'登入失敗: {str(e)}')
            self.getScreenShot('登入失敗')
            return False
        except Exception as e:
            logging.error(f'发生未预期的错误: {str(e)}')
            self.getScreenShot('未知错误')
            return False
    
    def get_error_message(self):
        try:
            logging.info('获取错误信息')
            self.wait_for_element(self.ERROR_MESSAGE)
            message = self.get_text(self.ERROR_MESSAGE)
            logging.info(f'错误信息: {message}')
            return message
        except Exception as e:
            logging.error(f'获取错误信息失败: {str(e)}')
            self.getScreenShot('获取错误信息失败')
            return ""