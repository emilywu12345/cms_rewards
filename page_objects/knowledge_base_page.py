from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By
import logging
import time

class KnowledgeBasePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
      # 元素定位器
    CREATE_KB_BUTTON = ('xpath', '//span[text()="新建知识库"]')
    KB_NAME_INPUT = ('xpath', '//input[contains(@placeholder, "知识库名称")]')
    KB_DESC_INPUT = ('xpath', '//textarea[contains(@placeholder, "知识库描述")]')
    CONFIRM_CREATE_BUTTON = ('xpath', '//button[contains(@class, "ant-btn-primary")]')
    
    # 编辑知识库元素
    FIRST_KB_ITEM = ('xpath', '//div[contains(@class, "knowledge-card")][1]')
    EDIT_KB_BUTTON = ('xpath', '//button[contains(@class, "edit-btn")]')
    KB_LIST = ('xpath', '//div[contains(@class, "knowledge-list")]')
    SUCCESS_MESSAGE = ('xpath', '//div[contains(@class, "success-message")]')
      def create_knowledge_base(self, name, description):
        """创建知识库"""
        try:
            logging.info(f'开始创建知识库: {name}')
            logging.info('等待创建按钮可点击')
            if not self.wait_and_click(self.CREATE_KB_BUTTON):
                logging.error('找不到或无法点击创建知识库按钮')
                return False
                
            logging.info('输入知识库名称')
            if not self.input_text(self.KB_NAME_INPUT, name):
                logging.error('无法输入知识库名称')
                return False
                
            logging.info('输入知识库描述')
            if not self.input_text(self.KB_DESC_INPUT, description):
                logging.error('无法输入知识库描述')
                return False
                
            logging.info('点击确认按钮')
            if not self.click(self.CONFIRM_CREATE_BUTTON):
                logging.error('无法点击确认按钮')
                return False
            
            # 等待成功提示
            success = self.wait_for_element(self.SUCCESS_MESSAGE)
            if success:
                logging.info('知识库创建成功')
                return True
            else:
                logging.error('未找到创建成功提示')
                return False
                
        except Exception as e:
            logging.error(f'创建知识库失败: {str(e)}')
            self.getScreenShot('创建知识库失败')
            return False
    
    def edit_knowledge_base(self, new_name, new_description):
        """编辑知识库"""
        try:
            logging.info(f'开始编辑知识库: {new_name}')
            # 等待知识库列表加载
            self.wait_for_element(self.KB_LIST)
            # 点击第一个知识库
            self.click(self.FIRST_KB_ITEM)
            # 点击编辑按钮
            self.click(self.EDIT_KB_BUTTON)
            
            # 清除并输入新的内容
            self.clear_and_input_text(self.KB_NAME_INPUT, new_name)
            self.clear_and_input_text(self.KB_DESC_INPUT, new_description)
            
            # 保存修改
            self.click(self.CONFIRM_CREATE_BUTTON)
            
            # 验证修改成功
            success = self.wait_for_element(self.SUCCESS_MESSAGE)
            if success:
                logging.info('知识库编辑成功')
                return True
            else:
                logging.error('未找到编辑成功提示')
                return False
                
        except Exception as e:
            logging.error(f'编辑知识库失败: {str(e)}')
            self.getScreenShot('编辑知识库失败')
            return False
            
    def get_first_kb_name(self):
        """获取第一个知识库的名称"""
        try:
            element = self.find_element(self.FIRST_KB_ITEM)
            return element.text
        except:
            return ""
            
    def clear_and_input_text(self, locator, text):
        """清除并输入文本"""
        element = self.find_element(locator)
        element.clear()
        time.sleep(0.5)  # 等待清除完成
        element.send_keys(text)
