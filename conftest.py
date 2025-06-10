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
from utils.config_manager import ConfigManager
from page_objects.login_page import LoginPage

# 确保项目根目录被正确添加到 PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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
    return ConfigManager.get_instance()._config

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
        logging.info("开始创建浏览器实例")
        browser = request.config.getoption("--browser")
        headless = request.config.getoption("--headless")
        browser_config = config.get('browser', {})
        
        logging.info(f"浏览器类型: {browser}, 无头模式: {headless}")
        
        options = Options()
        
        # 配置无头模式
        if headless.lower() == "true" or browser_config.get('headless', False):
            options.add_argument("--headless=new")
            
        # 添加SSL证书处理选项
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--disable-web-security')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # 添加其他必要的选项
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        logging.info("浏览器选项配置完成")
        
        if browser.lower() == "chrome":
            driver = webdriver.Chrome(options=options)
            logging.info("Chrome浏览器实例创建成功")
        else:
            raise ValueError(f"不支持的浏览器类型: {browser}")
        
        # 设置超时时间
        driver.implicitly_wait(browser_config.get('implicit_wait', 10))
        driver.set_page_load_timeout(browser_config.get('page_load_timeout', 30))
        if 'script_timeout' in browser_config:
            driver.set_script_timeout(browser_config['script_timeout'])
        
        logging.info("浏览器配置完成")
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

@pytest.fixture(scope="function")  # 標記這是一個函數級別的fixture，每個測試函數執行一次
def driver(request, config):  # 接收pytest的request對象和config配置
    """
    基础浏览器夹具 - 不执行登录
    用于需要测试未登录状态的用例
    """
    driver = None  # 初始化driver為None，確保finally塊能安全判斷
    try:
        # 創建瀏覽器實例（根據命令行參數和config配置）
        driver = create_driver(request, config)  
        # 將driver綁定到測試類實例（方便測試類中直接使用self.driver）
        request.instance.driver = driver  
        yield driver  # 返回driver給測試函數使用
    finally:
        if driver:  # 確保driver存在才執行退出
            try:
                driver.quit()  # 關閉瀏覽器
            except Exception as e:
                logging.error(f"关闭浏览器失败: {str(e)}")  # 記錄關閉失敗的錯誤
                
@pytest.fixture(scope="function")  # 函數級別的fixture
def logged_in_driver(request, config):  # 接收request和config
    """
    已登录状态的浏览器夹具
    用于需要测试已登录状态的用例
    """
    driver = None
    try:
        # 創建瀏覽器實例（與driver fixture相同）
        driver = create_driver(request, config)  
        # 根據命令行參數--env加載對應環境的配置（如UAT或QA環境的用戶名/密碼）
        env_config = ConfigManager.get_instance().get_env_config(request.config.getoption("--env"))  
        
        # 執行登錄操作
        login_page = LoginPage(driver)  # 初始化登錄頁面對象
        login_result = login_page.login(  # 調用登錄方法
            env_config.get('username'),  # 從配置讀取用戶名
            env_config.get('password')   # 從配置讀取密碼
        )
        
        # 登錄失敗處理
        if not login_result:
            screenshot = safe_screenshot(driver, "login_failed")  # 截圖保存失敗場景
            if screenshot:
                allure.attach(  # 將截圖附加到Allure報告
                    screenshot,
                    name="login_failed",
                    attachment_type=allure.attachment_type.PNG
                )
            pytest.fail("前置登录失败，无法继续测试")  # 主動標記測試失敗
        
        # 綁定driver並返回（與driver fixture相同）
        request.instance.driver = driver  
        yield driver  
    finally:
        if driver:  # 關閉瀏覽器（與driver fixture相同）
            try:
                driver.quit()  
            except Exception as e:
                logging.error(f"关闭浏览器失败: {str(e)}")  

@pytest.fixture(scope="class")
def class_logged_in_driver(request, config):
    """
    类级别的已登录状态浏览器夹具
    用于需要在类级别共享登录状态的用例
    """
    driver = None
    try:
        # 创建浏览器实例
        driver = create_driver(request, config)
        # 根据命令行参数--env加载对应环境的配置
        env_config = ConfigManager.get_instance().get_env_config(request.config.getoption("--env"))
        # 初始化登录页面对象
        from page_objects.login_page import LoginPage
        login_page = LoginPage(driver)
        # 执行登录操作
        login_result = login_page.login(env_config.get('username'), env_config.get('password'))
        # 登录失败处理
        if not login_result:
            pytest.fail("前置登录失败，无法继续测试")
        # 绑定driver到测试类实例
        request.cls.driver = driver
        yield driver
    finally:
        if driver:
            driver.quit()

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
