"""登录功能测试模块

此模块包含所有与用户登录相关的测试用例，包括：
- 成功登录测试
- 登出功能测试
"""

import pytest
import allure
from utils.config_loader import ConfigLoader
from utils.log_manager import logger
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage


@allure.feature("用户认证")
class TestLogin:
    """登录功能测试类"""
    
    @allure.story("成功登录")
    @allure.title("使用有效凭据登录")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_login(self, driver):
        """测试用户使用有效凭据能否成功登录系统
        
        步骤:
        1. 加载测试环境配置
        2. 打开登录页面
        3. 输入有效的用户名和密码
        4. 点击登录按钮
        5. 验证是否成功进入系统
        """
        # 加载环境配置
        env_config = ConfigLoader.get_env_config("uat")
        assert env_config, "无法加载环境配置"
        
        username = env_config.get("username")
        password = env_config.get("password")
        assert username and password, "环境配置缺少用户名或密码"
        
        # 执行登录操作
        with allure.step(f"使用账号 {username} 登录系统"):
            login_page = LoginPage(driver)
            logger.info(f"开始登录测试: {username}")
            
            result = login_page.login(
                username=username,
                password=password
            )
            assert result, "登录失败：无法完成登录操作"
        
        # 验证登录结果
        with allure.step("验证登录状态"):
            dashboard = DashboardPage(driver)
            assert dashboard.is_login_success(), "登录失败：未能进入系统主页"
            logger.info("登录测试完成")

    @allure.story("成功退出")
    @allure.title("已登录用户退出系统")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_logout(self, logged_in_driver):
        """测试已登录用户能否正常退出系统
        
        步骤:
        1. 点击退出按钮
        2. 验证是否返回登录页面
        """
        with allure.step("退出系统"):
            dashboard = DashboardPage(logged_in_driver)
            assert dashboard.logout(), "退出操作失败"
        
        with allure.step("验证退出结果"):
            current_url = logged_in_driver.current_url.lower()
            assert "login" in current_url, "退出失败：未能返回登录页面"
            logger.info("退出测试完成")