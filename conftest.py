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
    parser.addoption("--fast-close", action="store", default="False",
                    help="是否启用快速关闭模式: True, False")

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
            
        # 性能优化选项 - 优化关闭速度的配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-component-extensions-with-background-pages')
        
        # 网络和安全选项 - 减少关闭时的网络等待
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-component-update')
        options.add_argument('--force-device-scale-factor=1')
        
        # 日志和调试选项
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # 窗口大小设置
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        
        logging.info("浏览器选项配置完成")
        
        if browser.lower() == "chrome":
            driver = webdriver.Chrome(options=options)
            logging.info("Chrome浏览器实例创建成功")
        else:
            raise ValueError(f"不支持的浏览器类型: {browser}")
        
        # 设置超时时间 - 优化为更短的等待时间，避免关闭时长时间等待
        driver.implicitly_wait(browser_config.get('implicit_wait', 1))  # 减少到1秒
        driver.set_page_load_timeout(browser_config.get('page_load_timeout', 8))  # 减少到8秒
        if 'script_timeout' in browser_config:
            driver.set_script_timeout(browser_config['script_timeout'])
        else:
            driver.set_script_timeout(3)  # 默认3秒脚本超时
        
        logging.info("浏览器配置完成")
        return driver
        
    except Exception as e:
        logging.error(f"创建浏览器实例失败: {str(e)}")
        raise

def safe_close_driver(driver, fast_close=False):
    """
    安全地关闭浏览器驱动
    Args:
        driver: WebDriver实例
        fast_close: 是否启用快速关闭模式
    """
    if not driver:
        return
        
    try:
        if fast_close:
            # 快速关闭模式：直接quit，不等待
            logging.info("快速关闭模式：直接终止浏览器")
            # 设置较短的超时时间
            import signal
            import threading
            
            def force_quit():
                try:
                    # driver.quit()
                    pass
                except:
                    pass
            
            # 在单独线程中执行quit，如果超时则强制终止
            quit_thread = threading.Thread(target=force_quit)
            quit_thread.daemon = True
            quit_thread.start()
            quit_thread.join(timeout=2)  # 最多等待2秒
            
            if quit_thread.is_alive():
                # 如果quit没有在2秒内完成，强制终止进程
                logging.warning("quit操作超时，强制终止进程")
                try:
                    import subprocess
                    if sys.platform.startswith('win'):
                        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], 
                                     capture_output=True, check=False, timeout=3)
                        subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe"], 
                                     capture_output=True, check=False, timeout=3)
                    else:
                        subprocess.run(["pkill", "-f", "chrome"], 
                                     capture_output=True, check=False, timeout=3)
                        subprocess.run(["pkill", "-f", "chromedriver"], 
                                     capture_output=True, check=False, timeout=3)
                    logging.info("已强制终止浏览器进程")
                except Exception as kill_error:
                    logging.error(f"强制终止进程失败: {str(kill_error)}")
        else:
            # 标准关闭模式：先关闭窗口再quit
            logging.info("标准关闭模式：逐步关闭浏览器")
            try:
                # 快速关闭所有窗口，不逐个切换
                # driver.quit()
                pass
            except Exception as e:
                logging.warning(f"关闭浏览器时出错: {str(e)}")
                # 标准模式失败时也尝试强制终止
                try:
                    import subprocess
                    if sys.platform.startswith('win'):
                        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], 
                                     capture_output=True, check=False, timeout=3)
                        subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe"], 
                                     capture_output=True, check=False, timeout=3)
                    logging.info("已强制终止Chrome相关进程")
                except Exception as kill_error:
                    logging.error(f"强制终止进程失败: {str(kill_error)}")
            
        logging.info("浏览器已成功关闭")
        
    except Exception as e:
        logging.error(f"关闭浏览器失败: {str(e)}")
        # 强制终止进程作为最后手段
        try:
            import subprocess
            if sys.platform.startswith('win'):
                subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], 
                             capture_output=True, check=False, timeout=3)
                subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe"], 
                             capture_output=True, check=False, timeout=3)
            else:
                subprocess.run(["pkill", "-f", "chrome"], 
                             capture_output=True, check=False, timeout=3)
                subprocess.run(["pkill", "-f", "chromedriver"], 
                             capture_output=True, check=False, timeout=3)
            logging.info("已强制终止浏览器相关进程")
        except Exception as kill_error:
            logging.error(f"强制终止进程失败: {str(kill_error)}")

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

@pytest.fixture(scope="session")  # 优化为会话级别，所有用例共享同一driver实例
def driver(request, config):  # 接收pytest的request對象和config配置
    """
    基础浏览器夹具 - 不执行登录
    用于需要测试未登录状态的用例
    """
    driver = None  # 初始化driver為None，確保finally塊能安全判斷
    try:
        driver = create_driver(request, config)
        # 仅在类用例时设置 request.instance.driver，函数用例跳过
        if hasattr(request, 'instance') and request.instance is not None:
            request.instance.driver = driver
        yield driver
    finally:
        # 检查是否启用快速关闭模式（通过环境变量获取）
        fast_close = os.environ.get("PYTEST_FAST_CLOSE", "false").lower() == "true"
        safe_close_driver(driver, fast_close)
                
@pytest.fixture(scope="session")  # 优化为会话级别，所有用例共享同一driver实例
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
        login_page = LoginPage(driver)
        login_result = login_page.login(env_config.get('username'), env_config.get('password'))
        if not login_result:
            pytest.fail("前置登录失败，无法继续测试")
        request.instance.driver = driver
        yield driver
    finally:
        # 检查是否启用快速关闭模式（通过环境变量获取）
        fast_close = os.environ.get("PYTEST_FAST_CLOSE", "false").lower() == "true"
        safe_close_driver(driver, fast_close)

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
        # 检查是否启用快速关闭模式（通过环境变量获取）
        fast_close = os.environ.get("PYTEST_FAST_CLOSE", "false").lower() == "true"
        safe_close_driver(driver, fast_close)

@pytest.fixture(scope="session")
def session_logged_in_driver(request, config):
    """
    会话级别的已登录状态浏览器夹具，所有用例文件共享同一driver和登录态
    """
    driver = None
    try:
        driver = create_driver(request, config)
        env_config = ConfigManager.get_instance().get_env_config(request.config.getoption("--env"))
        login_page = LoginPage(driver)
        login_result = login_page.login(env_config.get('username'), env_config.get('password'))
        if not login_result:
            pytest.fail("前置登录失败，无法继续测试")
        # 绑定driver到request.session，供不同文件共享
        request.session.driver = driver
        yield driver
    finally:
        # 检查是否启用快速关闭模式（通过环境变量获取）
        fast_close = os.environ.get("PYTEST_FAST_CLOSE", "false").lower() == "true"
        safe_close_driver(driver, fast_close)

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
