import pytest
import allure
from page_objects.login_page import LoginPage
from utils.logger import logger

@allure.feature("用户认证")
@allure.severity(allure.severity_level.CRITICAL)
class TestInvalidLogin:
    @allure.story("无效登录")
    @allure.description("验证使用无效凭据时的错误提示")
    @pytest.mark.parametrize("username,password,expected_error", [
        ("invalid@email.com", "wrongpass", "用户名或密码错误"),
        ("", "", "请输入用户名和密码"),
        ("test@test.com", "", "请输入密码"),
        ("", "password", "请输入用户名")
    ])
    def test_invalid_login(self, driver, username, password, expected_error):
        with allure.step(f"使用无效凭据登录 - 用户名: {username}, 密码: {'*' * len(password)}"):
            login_page = LoginPage(driver)
            result = login_page.login(username, password)
            assert not result, "无效登录不应该成功"
            error_message = login_page.get_error_message()
            assert expected_error in error_message, f"错误信息不符: 期望 '{expected_error}', 实际 '{error_message}'"
