"""控制面板页面对象类

此类负责系统主页/控制面板相关的所有操作，包括：
- 验证登录状态
- 导航菜单操作
- 退出登录
- 用户信息管理
"""

import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from page_objects.base_page import BasePage
from utils.log_manager import logger

class DashboardPage(BasePage):
    """控制面板页面类"""
    
    # 页面元素定位器
    DASHBOARD_TITLE = (By.CSS_SELECTOR, '.el-menu-item.is-active')
    USER_MENU = (By.CSS_SELECTOR, '.el-dropdown')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '.el-dropdown-menu__item')
    USER_INFO = (By.CSS_SELECTOR, '.el-dropdown-link')
    
    # 导航菜单
    NAV_KNOWLEDGE = (By.ID, 'menu-knowledge')
    NAV_SETTINGS = (By.ID, 'menu-settings')
    NAV_DOCS = (By.ID, 'menu-docs')
    
    def __init__(self, driver):
        """初始化控制面板页面对象"""
        super().__init__(driver)
    
    @allure.step("验证登录状态")
    def is_login_success(self) -> bool:
        """
        验证是否成功登录到控制面板
        
        Returns:
            bool: 是否成功登录
        """
        try:
            # 等待页面加载完成
            self.wait_for_element_visible((By.CSS_SELECTOR, '.el-container'))
            
            # 检查是否存在活动菜单项
            if not self.is_element_visible(self.DASHBOARD_TITLE):
                logger.warning("未找到活动菜单项")
                
            # 检查用户菜单是否可用
            if not self.is_element_visible(self.USER_MENU):
                logger.error("未找到用户菜单")
                return False
                
            # 验证成功
            logger.info("成功进入控制面板")
            return True
            
        except Exception as e:
            logger.error(f"验证登录状态失败: {str(e)}")
            self.take_screenshot("login_verify_failed")
            return False
    
    @allure.step("退出登录")
    def logout(self) -> bool:
        """
        执行退出登录操作
        
        Returns:
            bool: 退出是否成功
        """
        try:
            # 确保菜单可见并可交互
            if not self.wait_for_element_visible(self.USER_MENU):
                logger.error("用户菜单不可见")
                return False
                
            # 触发下拉菜单
            menu = self.find_element(self.USER_MENU)
            self.action_chains.move_to_element(menu).perform()
              # 等待下拉菜单显示并点击退出选项
            self.wait_for_url_contains("/dashboard")  # 等待进入控制面板
            
            # 使用JavaScript点击用户菜单
            menu = self.find_element(self.USER_MENU)
            self.driver.execute_script("arguments[0].click();", menu)
            
            # 定位并点击退出按钮
            logout_button = (By.CSS_SELECTOR, '.el-dropdown-menu__item:last-child')
            if not self.wait_for_element_visible(logout_button, timeout=5):
                logger.error("退出按钮不可见")
                return False
            
            if not self.click(logout_button):
                logger.error("无法点击退出按钮")
                return False
            
            # 等待返回登录页
            self.wait_for_url_contains("login")
            
            logger.info("成功退出登录")
            return True
            
        except Exception as e:
            logger.error(f"退出登录失败: {str(e)}")
            self.take_screenshot("logout_failed")
            return False
    
    @allure.step("获取用户信息")
    def get_user_info(self) -> dict:
        """
        获取当前登录用户信息
        
        Returns:
            dict: 用户信息字典
        """
        try:
            user_info = {}
            info_element = self.find_element(self.USER_INFO)
            
            # 解析用户信息
            user_info['username'] = info_element.get_attribute('data-username')
            user_info['role'] = info_element.get_attribute('data-role')
            
            logger.info(f"获取用户信息成功: {user_info}")
            return user_info
            
        except Exception as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            return {}
    
    @allure.step("导航到知识库")
    def goto_knowledge_base(self) -> bool:
        """
        导航到知识库页面
        
        Returns:
            bool: 导航是否成功
        """
        try:
            if not self.click(self.NAV_KNOWLEDGE):
                logger.error("无法点击知识库菜单")
                return False
                
            logger.info("成功导航到知识库页面")
            return True
            
        except Exception as e:
            logger.error(f"导航到知识库失败: {str(e)}")
            self.take_screenshot("nav_knowledge_failed")
            return False
    
    @allure.step("导航到设置")
    def goto_settings(self) -> bool:
        """
        导航到设置页面
        
        Returns:
            bool: 导航是否成功
        """
        try:
            if not self.click(self.NAV_SETTINGS):
                logger.error("无法点击设置菜单")
                return False
                
            logger.info("成功导航到设置页面")
            return True
            
        except Exception as e:
            logger.error(f"导航到设置页面失败: {str(e)}")
            self.take_screenshot("nav_settings_failed")
            return False
    
    @allure.step("导航到文档")
    def goto_docs(self) -> bool:
        """
        导航到文档页面
        
        Returns:
            bool: 导航是否成功
        """
        try:
            if not self.click(self.NAV_DOCS):
                logger.error("无法点击文档菜单")
                return False
                
            logger.info("成功导航到文档页面")
            return True
            
        except Exception as e:
            logger.error(f"导航到文档页面失败: {str(e)}")
            self.take_screenshot("nav_docs_failed")
            return False
