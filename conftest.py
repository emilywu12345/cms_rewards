import pytest
import os
import allure
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="测试环境: qa, stage, prod")
    parser.addoption("--browser", action="store", default="chrome", help="浏览器类型: chrome, firefox")
    parser.addoption("--headless", action="store", default="False", help="是否使用无头模式: True, False")

@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.ini")
    config = ConfigParser()
    config.read(config_path)
    return config

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            driver = item.funcargs.get("driver")
            if driver is not None:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    attachment_type=allure.attachment_type.PNG
                )

@pytest.fixture(scope="function")
def driver(request, config):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    if browser == "chrome":
        options = Options()
        if headless == "True":
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    else:
        raise ValueError(f"不支持的浏览器类型: {browser}")
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
