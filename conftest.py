"""测试配置文件

包含所有测试相关的 fixtures 和钩子函数：
- 浏览器驱动配置
- 测试环境配置 
- 日志配置
- 截图配置
"""

import sys
import os
import pytest
import allure
import logging
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from utils.config_loader import ConfigLoader
from page_objects.login_page import LoginPage

# 创建必要的目录
for dir_path in ['logs', 'screenshots', 'reports/allure-results']:
    Path(dir_path).mkdir(parents=True, exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption("--env", action="store", default="uat", 
                    help="测试环境: qa, uat")
    parser.addoption("--browser", action="store", default="chrome", 
                    help="浏览器类型: chrome, firefox")
    parser.addoption("--headless", action="store", default="False", 
                    help="是否使用无头模式: True, False")

@pytest.fixture(scope="session")
def config():
    """加载配置文件"""
    return ConfigLoader.load_config()

def create_driver(request, config):
    """
    创建 WebDriver 实例
    Args:
        request: pytest request对象
        config: 配置对象
    Returns:
        WebDriver实例
    """
    try:
        browser = request.config.getoption("--browser")
        headless = request.config.getoption("--headless")
        browser_config = config.get('browser', {})
        
        options = Options()
        
        # 配置无头模式
        if headless.lower() == "true" or browser_config.get('headless', False):
            options.add_argument("--headless=new")
            
        # 忽略证书错误
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
          # 添加SSL证书处理选项
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--disable-web-security')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # 从配置文件加载浏览器参数
        capabilities = browser_config.get('capabilities', {})
        
        # 添加浏览器启动参数
        for arg in capabilities.get('args', []):
            options.add_argument(arg)
        
        # 添加浏览器首选项
        for key, value in capabilities.get('prefs', {}).items():
            options.add_experimental_option("prefs", {key: value})
        
        if browser.lower() == "chrome":
            driver = webdriver.Chrome(options=options)
        else:
            raise ValueError(f"不支持的浏览器类型: {browser}")
        
        # 设置超时时间
        driver.implicitly_wait(browser_config.get('implicit_wait', 10))
        driver.set_page_load_timeout(browser_config.get('page_load_timeout', 30))
        if 'script_timeout' in browser_config:
            driver.set_script_timeout(browser_config['script_timeout'])
        
        return driver
        
    except Exception as e:
        logging.error(f"创建浏览器实例失败: {str(e)}")
        raise

def safe_screenshot(driver, name):
    """
    安全地获取截图
    Args:
        driver: WebDriver实例
        name: 截图名称
    Returns:
        bytes或None: 截图数据
    """
    try:
        return driver.get_screenshot_as_png()
    except WebDriverException as e:
        logging.error(f"截图失败: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"截图时发生未知错误: {str(e)}")
        return None

@pytest.fixture(scope="function")
def driver(request, config):
    """
    基础浏览器夹具 - 不执行登录
    用于需要测试未登录状态的用例
    """
    driver = None
    try:
        driver = create_driver(request, config)
        request.instance.driver = driver
        yield driver
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logging.error(f"关闭浏览器失败: {str(e)}")

@pytest.fixture(scope="function")
def logged_in_driver(request, config):
    """
    已登录状态的浏览器夹具
    用于需要测试已登录状态的用例
    """
    driver = None
    try:
        driver = create_driver(request, config)
        env_config = ConfigLoader.get_env_config(request.config.getoption("--env"))
        
        # 执行登录
        login_page = LoginPage(driver)
        login_result = login_page.login(
            env_config.get('username'),
            env_config.get('password')
        )
        
        if not login_result:
            screenshot = safe_screenshot(driver, "login_failed")
            if screenshot:
                allure.attach(
                    screenshot,
                    name="login_failed",
                    attachment_type=allure.attachment_type.PNG
                )
            pytest.fail("前置登录失败，无法继续测试")
        
        request.instance.driver = driver
        yield driver
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logging.error(f"关闭浏览器失败: {str(e)}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动截图
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            for fixture_name in ["driver", "logged_in_driver"]:
                try:
                    driver = item.funcargs.get(fixture_name)
                    if driver:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        screenshot_name = f"failure_{item.name}_{timestamp}"
                        screenshot = safe_screenshot(driver, screenshot_name)
                        if screenshot:
                            allure.attach(
                                screenshot,
                                name=screenshot_name,
                                attachment_type=allure.attachment_type.PNG
                            )
                except Exception as e:
                    logging.error(f"处理测试失败截图时发生错误: {str(e)}")

@pytest.fixture(autouse=True)
def logging_test_name(request):
    """
    自动记录每个测试用例的开始和结束
    """
    logging.info(f"开始测试: {request.node.name}")
    yield
    logging.info(f"结束测试: {request.node.name}")
