import pytest
import allure
from utils.config_manager import ConfigManager
from utils.log_manager import logger
from page_objects.login_page import LoginPage
@allure.feature("登入")
class TestLogin:
    """登入功能測試類"""

    @pytest.fixture(autouse=True)
    def setup(self, request):
        """自動加載環境配置"""
        self.env = request.config.getoption("--env")  # 從命令行獲取環境
        self.env_config = ConfigManager.get_instance().get_env_config(self.env)
        assert self.env_config, f"無法加載 {self.env} 環境配置"
        assert self.env_config.get("username") and self.env_config.get("password"), "環境配置缺少賬號或密碼"

    @allure.story("成功登入")
    @allure.title("使用有效賬號登入")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_0_login(self, driver):
        """測試有效賬號密碼登入"""
        login_page = LoginPage(driver)
        username = self.env_config["username"]
        password = self.env_config["password"]

        with allure.step(f"使用帳號 {username} 登入系統"):
            logger.info(f"開始登入測試: {username}")
            assert login_page.login(username, password), "登入失敗"