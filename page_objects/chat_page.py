import logging
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from page_objects.base_page import BasePage
from utils.log_manager import logger

class ChatPage(BasePage):
    """聊天页面对象，包含所有聊天相关操作"""

    # 知识库下拉框
    KNOWLEDGE_BOX= (By.XPATH, '/html/body/div[1]/div/main/div[1]/div/div[2]/div[2]/div')
    # 选值
    SELECT_KNOWLEDGE = (By.XPATH, '/html/body/div[2]/div[3]/div/div/div[1]/ul/li[1]')

    # 提交按钮
    SUBMIT_BUTTON = (By.XPATH, '/html/body/div[1]/div/main/div[1]/div/div[3]/div/div[2]/button[2]')

    # 消息输入框（优化定位，兼容 ant-design 聊天输入框）
    MESSAGE_INPUT = (By.CSS_SELECTOR, 'textarea.ant-input.ant-sender-input')

    @allure.step("AI 聊天")
    def send_message(self, message):
        """AI 聊天页面"""
        try:
            # 先等待loading遮罩消失
            self.wait_loading_disappear(timeout=15)
            self.wait_and_click(self.KNOWLEDGE_BOX)
            # 等待知识库下拉框出现
            if not self.wait_for_element(self.SELECT_KNOWLEDGE, timeout=self.timeout):
                logger.error('知识库下拉框未出现')
                self.take_screenshot('知识库下拉框未出现')
                return False
            self.wait_and_click(self.SELECT_KNOWLEDGE)
            # 输入消息内容
            self.input_text(self.MESSAGE_INPUT, message)
            self.wait_and_click(self.SUBMIT_BUTTON)
            time.sleep(1)
            self.take_screenshot("发送消息成功")
            return True
        except NoSuchElementException as e:
            logger.error(f'聊天失败: 元素未找到 - {str(e)}')
            self.take_screenshot("聊天失败")
            return False
        except TimeoutException as e:
            logger.error(f'聊天失败: 等待元素超时 - {str(e)}')
            self.take_screenshot("聊天失败")
            return False
        except Exception as e:
            logger.error(f"聊天失败: 发生未知异常 - {str(e)}")
            self.take_screenshot("聊天失败")
            return False
