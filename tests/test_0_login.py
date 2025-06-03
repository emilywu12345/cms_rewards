import pytest
import allure
from utils.config_manager import ConfigManager
from utils.log_manager import logger
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.screenshot_manager import ScreenshotManager


@allure.feature("登入")
class TestLogin:
    """登入功能測試類"""
    @allure.story("成功登入")
    @allure.title("使用有效賬號登入")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_login(self, driver):
        """
        測試User使用有效賬號密碼能否成功登入系統
        
        步驟:
        1. 加載測試環境配置
        2. 打開登入頁面
        3. 輸入有效的使用者名稱和密碼
        4. 點擊登入按鈕
        5. 驗證是否成功進入系統
        """
        # 加載環境配置
        env_config = ConfigManager.get_instance().get_env_config("uat")
        assert env_config, "無法加載環境配置"
        
        username = env_config.get("username")
        password = env_config.get("password")
        assert username and password, "環境配置缺少User賬號或密碼"
        
        # 執行登入操作
        with allure.step(f"使用帳號 {username} 登入系統"):
            login_page = LoginPage(driver)
            logger.info(f"開始登入測試: {username}")
            
            result = login_page.login(
                username=username,
                password=password
            )
            assert result, "登入失敗：無法完成登入操作"