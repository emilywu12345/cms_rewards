import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import pytest
import allure
from selenium import webdriver
from configparser import ConfigParser
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage
from utils.retry import retry_on_failure
from utils.logger import logger
import os


config = ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.ini')
config.read(config_path)

@pytest.fixture(scope="class", autouse=True)
def driver(request):
    options = webdriver.ChromeOptions()
    if config['DRIVER'].getboolean('headless'):
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.quit()

@allure.feature("用户认证")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.usefixtures("driver")
class TestLogin:
    @allure.story("成功登录")
    @allure.description("验证用户能否使用有效凭据成功登录系统")
    @allure.severity(allure.severity_level.BLOCKER)
    @retry_on_failure(retries=2)
    def test_login(self):
        with allure.step(f"使用账号 {config['ENV']['username']} 执行登录操作"):
            login_page = LoginPage(self.driver)
            result = login_page.login(
                config['ENV']['username'],
                config['ENV']['password']
            )
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="登录操作截图",
                attachment_type=allure.attachment_type.PNG
            )
            assert result, "登录失败"
            logger.info("登录流程已执行")
            
        with allure.step("验证登录成功"):
            dashboard_page = DashboardPage(self.driver)
            assert dashboard_page.is_login_success(), "登录后首页校验失败"
            logger.info("登录测试成功")    @allure.story("成功退出")
    @allure.description("验证已登录用户能否正常退出系统")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout(self):
        with allure.step("执行退出操作"):
            dashboard_page = DashboardPage(self.driver)
            dashboard_page.logout()
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="退出操作截图",
                attachment_type=allure.attachment_type.PNG
            )
            
        with allure.step("验证退出成功"):
            assert "login" in self.driver.current_url.lower(), "退出后未能返回登录页面"
            logger.info("退出测试成功")