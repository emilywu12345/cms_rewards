from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By
import logging

class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
    # 页面元素定位
    PROFILE_MENU = ('xpath', '//span[text()="个人中心"]')
    USERNAME_FIELD = ('id', 'username')
    EMAIL_FIELD = ('id', 'email')
    NICKNAME_INPUT = ('id', 'nickname')
    PHONE_INPUT = ('id', 'phone')
    SAVE_BUTTON = ('xpath', '//button[text()="保存"]')
    UPDATE_MESSAGE = ('class name', 'success-message')
    
    def navigate_to_profile(self):
        """导航到个人信息页面"""
        try:
            logging.info('导航到个人信息页面')
            self.click(self.PROFILE_MENU)
            self.wait_for_element(self.USERNAME_FIELD)
            return True
        except Exception as e:
            logging.error(f'导航到个人信息页面失败: {str(e)}')
            self.getScreenShot('导航失败')
            return False
            
    def get_username(self):
        """获取用户名"""
        return self.get_text(self.USERNAME_FIELD)
        
    def get_email(self):
        """获取邮箱"""
        return self.get_text(self.EMAIL_FIELD)
        
    def update_profile(self, info):
        """更新个人信息"""
        try:
            if 'nickname' in info:
                self.input_text(self.NICKNAME_INPUT, info['nickname'])
            if 'phone' in info:
                self.input_text(self.PHONE_INPUT, info['phone'])
            self.click(self.SAVE_BUTTON)
            return True
        except Exception as e:
            logging.error(f'更新个人信息失败: {str(e)}')
            self.getScreenShot('更新失败')
            return False
            
    def get_update_message(self):
        """获取更新提示信息"""
        return self.get_text(self.UPDATE_MESSAGE)
