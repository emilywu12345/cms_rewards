import os
from datetime import datetime
from typing import Optional, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
import allure
from .log_manager import logger


class ScreenshotManager:
    """统一的截图管理类"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls, screenshot_dir: str):
        """单例模式获取实例"""
        if cls._instance is None:
            cls._instance = ScreenshotManager(screenshot_dir)
        return cls._instance
    
    def __init__(self, screenshot_dir: str):
        """初始化截图管理器"""
        self.screenshot_dir = screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def take_screenshot(
        self,
        driver: WebDriver,
        name: str,
        allure_attach: bool = True
    ) -> Optional[Union[bytes, str]]:
        """
        获取页面截图
        Args:
            driver: WebDriver实例
            name: 截图名称
            allure_attach: 是否添加到Allure报告
        Returns:
            bytes或str: 截图数据或文件路径，失败则返回None
        """
        try:
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # 获取截图
            screenshot_data = self._capture_screenshot(driver)
            if not screenshot_data:
                return None
                
            # 保存文件
            with open(filepath, "wb") as f:
                f.write(screenshot_data)
                
            # 添加到Allure报告
            if allure_attach:
                with allure.step(f"截图: {name}"):
                    allure.attach(
                        screenshot_data,
                        name=filename,
                        attachment_type=allure.attachment_type.PNG
                    )
                    
            logger.screenshot_log(f"截图已保存: {name}", filepath)
            logger.info(f"截图保存路径: {self.screenshot_dir}")
            logger.info(f"截图文件名: {filename}")
            return filepath
            
        except Exception as e:
            logger.error(f"截图失败 {name}: {str(e)}")
            return None
    
    def _capture_screenshot(self, driver: WebDriver) -> Optional[bytes]:
        """
        捕获屏幕截图
        Args:
            driver: WebDriver实例
        Returns:
            bytes: 截图数据
        """
        try:
            return driver.get_screenshot_as_png()
        except WebDriverException as e:
            logger.error(f"获取截图数据失败: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"截图过程发生未知错误: {str(e)}")
            return None


# 创建全局截图管理器实例
screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
screenshot = ScreenshotManager.get_instance(screenshot_dir)
