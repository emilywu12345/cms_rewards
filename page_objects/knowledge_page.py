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

class KnowledgePage(BasePage):
    """知识库页面对象，包含所有知识库相关操作"""
    
    # 导航知识库
    KNOWLEDGE = (By.XPATH, '//*[@class="title" and text()="知识库"]')  
    KNOWLEDGE_TITLE = (By.XPATH, '//*[@class="title" and text()="知识库管理"]')   
    MODEL_MENU = (By.XPATH, '/html/body/div[1]/div/div[1]/div/ul/li[2]/div/span')                  

    # 知识库创建
    CREATE_KB_BUTTON = (By.XPATH, '//button[.//span[text()="新建"]]')
    KB_NAME_INPUT = (By.XPATH, '//input[@placeholder="请输入知识库名称"]')
    KB_PROMPT_INPUT = (By.XPATH, '/html/body/div[1]/div/main/div/div[3]/div/div/div/form/div[2]/div/div/div/input')

    VECTOR_MODEL_DROPDOWN = (By.XPATH, '//span[text()="请选择模型"]/parent::div')
    SELECT_MODEL_DROPDOWN = (By.XPATH, "//li[contains(@class, 'el-select-dropdown__item') and (contains(text(), 'Embedding') or contains(text(), '嵌入') or contains(text(), '向量'))]")
    SLIDER = (By.CSS_SELECTOR, 'div.el-slider__button.el-tooltip__trigger')
    CONFIRM_CREATE_BUTTON = (By.XPATH, '/html/body/div[1]/div/main/div/div[3]/div/div/footer/div/button[2]/span')

    # 创建成功提示信息
    CREATE_SUCCESS_MESSAGE = (By.XPATH, '//p[contains(@class, "el-message__content") and contains(text(), "保存成功")]')

    @allure.step("进入知识库管理页面")
    def navigate_knowledge(self):
        """导航到知识库管理页面"""
        try:
            # 先等待loading遮罩消失
            self.wait_loading_disappear(timeout=15)
            self.wait_and_click(self.KNOWLEDGE)
            if not self.wait_for_element(self.KNOWLEDGE_TITLE, timeout=self.timeout):
                logger.error('知识库页面标题未出现，导航失败')
                self.take_screenshot('navigation_failed')
                return False
            logger.info('成功导航到知识库页面')
            return True
        except NoSuchElementException as e:
            logger.error(f'导航失败: 元素未找到 - {str(e)}')
            self.take_screenshot("进入导航页面失败")
            return False
        except TimeoutException as e:
            logger.error(f'导航失败: 等待元素超时 - {str(e)}')
            self.take_screenshot("进入导航页面失败")
            return False
        except Exception as e:
            logger.error(f"导航失败: 发生未知异常 - {str(e)}")
            self.take_screenshot("进入导航页面失败")
            return False


    @allure.step("创建新的知识库")
    def create_knowledge(self, name, prompt):
        """
        创建新的知识库
        """
        try:
            self.wait_and_click(self.CREATE_KB_BUTTON)
            self.input_text(self.KB_NAME_INPUT, name)
            self.input_text(self.KB_PROMPT_INPUT, prompt)

            # 定位“向量模型”下拉框并点击展开选项
            select_model_dropdown = self.find_element(self.VECTOR_MODEL_DROPDOWN)  
            select_model_dropdown.click()
            # 调试：打印所有下拉选项文本，辅助定位
            # time.sleep(1)  # 等待下拉菜单渲染
            # options = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'el-select-dropdown__item')]")
            # logger.error(f"下拉选项数量: {len(options)}")
            # for i, opt in enumerate(options):
            #     logger.error(f"选项{i}: {opt.text}")
            # 直接点击第一个下拉选项，保证流程健壮
            options = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'el-select-dropdown__item')]")
            if options:
                options[0].click()
            else:
                logger.error("未找到任何下拉选项，无法选择模型！")
                self.take_screenshot("select_model_failed")
                return False

            # 滑动滑块前调试：打印页面源码和截图，辅助排查
            # logger.error(f"滑块前页面源码片段：{self.driver.page_source[:1000]}")
            # self.take_screenshot("before_slider")
            slider = self.find_element(self.SLIDER)
            # 使用 ActionChains 拖动滑块，模拟真实滑动
            actions = ActionChains(self.driver)
            actions.click_and_hold(slider).move_by_offset(50, 0).release().perform()
            # time.sleep(1)
            
            # 点击确认创建按钮
            self.wait_and_click(self.CONFIRM_CREATE_BUTTON)
            # time.sleep(1) 
            # 等待创建成功提示出现
            self.wait_for_element(self.CREATE_SUCCESS_MESSAGE, timeout=10)
            time.sleep(1)
            self.take_screenshot("创建知识库成功")
            return True
        except NoSuchElementException as e:
            logger.error(f'创建知识库失败: 元素未找到 - {str(e)}')
            self.take_screenshot("create_kb_failed")
            return False
        except TimeoutException as e:
            logger.error(f'创建知识库失败: 等待元素超时 - {str(e)}')
            self.take_screenshot("create_kb_failed")
            return False
        except Exception as e:
            logger.error(f"创建知识库失败: 发生未知异常 - {str(e)}")
            self.take_screenshot("create_kb_failed")
            return False

