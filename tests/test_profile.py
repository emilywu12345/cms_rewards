import pytest
import allure
from page_objects.login_page import LoginPage
from page_objects.profile_page import ProfilePage
from utils.logger import logger

@allure.feature("用户信息管理")
class TestUserProfile:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        """前置条件：用户已登录"""
        login_page = LoginPage(driver)
        login_page.login(config['ENV']['username'], config['ENV']['password'])
    
    @allure.story("查看个人信息")
    @allure.description("验证用户能否正确查看个人信息")
    def test_view_profile(self, driver):
        with allure.step("进入个人信息页面"):
            profile_page = ProfilePage(driver)
            profile_page.navigate_to_profile()
            
        with allure.step("验证个人信息显示"):
            assert profile_page.get_username() == "测试用户", "用户名显示不正确"
            assert profile_page.get_email() == "1062174229@qq.com", "邮箱显示不正确"
            
    @allure.story("更新个人信息")
    @allure.description("验证用户能否成功更新个人信息")
    def test_update_profile(self, driver):
        with allure.step("更新个人信息"):
            profile_page = ProfilePage(driver)
            profile_page.navigate_to_profile()
            profile_page.update_profile({
                "nickname": "新昵称",
                "phone": "13800138000"
            })
            
        with allure.step("验证更新成功"):
            assert profile_page.get_update_message() == "更新成功", "个人信息更新失败"
