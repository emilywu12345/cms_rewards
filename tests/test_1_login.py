import pytest
import allure
from utils.config_manager import ConfigManager
from utils.log_manager import logger
from page_objects.login_page import LoginPage



@allure.feature("登录")
@allure.story("成功登录")
@allure.title("使用有效账号登录")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
class TestLogin:
    """登录功能测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, request):
        """自动加载环境配置"""

        # 从命令行获取环境
        self.env = request.config.getoption("--env")  
        self.env_config = ConfigManager.get_instance().get_env_config(self.env)
        assert self.env_config, f"无法加载 {self.env} 环境配置"
        assert self.env_config.get("username") and self.env_config.get("password"), "环境配置缺少账号或密码"
 
    def test_login_success(self, driver):
        """
        测试User使用有效账号密码能否成功登录系统
        
        步骤:
        1. 加载测试环境配置
        2. 打开登录页面
        3. 输入有效的用户名和密码
        4. 点击登录按钮
        5. 验证是否成功进入系统
        """
        login_page = LoginPage(driver)
        username = self.env_config["username"]
        password = self.env_config["password"]

        with allure.step(f"使用账号 {username} 登录系统"):
            assert login_page.login(username, password), "登录失败"
            logger.info("登录测试完成，成功登录系统")