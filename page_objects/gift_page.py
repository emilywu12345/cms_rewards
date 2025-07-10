import time
import allure
import os
import sys
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pytest



# 添加项目根目录到 Python 路径，以支持独立运行
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from page_objects.base_page import BasePage
from page_objects.login_page import LoginPage
from utils.log_manager import logger

class GiftPage(BasePage):
    """Gift页面对象,包含所有Gift相关操作"""

    # 页面元素定位器
    REMARKS = (By.XPATH, '//textarea[@id="rewardRemark"]')
    POINTS_REQUIRED = (By.XPATH, '//input[@id="pointsNeeded"]')
    CATEGORY = (By.XPATH, '//input[@id="categoryCodeList"]')
    CATEGORY_LABEL = (By.XPATH, '//*[@id="main-layout"]/main/div/div/div/div/form/div[5]/div[1]/label/span')
    HOTEL_OPTION = (By.XPATH, "//li[contains(@class, 'ant-select-dropdown-menu-item') and contains(text(), 'Hotel')]")

    # 日期
    SHOWING_DATE_ICON = (By.XPATH, "//span[@id='showingDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    REDEMPTION_DATE_ICON = (By.XPATH, "//span[@id='reservationDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    EXPIRY_DATE_ICON = (By.XPATH, "//span[@id='expiryDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    EXPIRY_DATE_BUTTON = (By.XPATH, "//div[contains(@class, 'ant-calendar-footer')]//a[contains(@class, 'ant-calendar-ok-btn') and @role='button']")


    HIGHLIGHTED = (By.XPATH, '//input[@id="highlighted"]')
    GIFT_SOURCE = (By.XPATH, '//div[@id="giftSource"]//div[@class="ant-select-selection__rendered"]')
    GIFT_SOURCE_OPTION = (By.XPATH, '//div[contains(@class,"ant-select-dropdown") and not(contains(@class,"hidden"))]//li[@role="option" and contains(., "Purchase")]')
    VALUE = (By.XPATH, '//div[@class="ant-input-number-input-wrap"]//input[@id="value"]')
    COST = (By.XPATH, '//div[@class="ant-input-number-input-wrap"]//input[@id="cost"]')

    GIFT_NAME_EN = (By.XPATH, '//input[@id="en.title"]')
    GIFT_NAME_ZH_CN = (By.XPATH, '//input[@id="zh-cn.title"]')
    GIFT_NAME_ZH_HK = (By.XPATH, '//input[@id="zh-hk.title"]')

    ADD_BUTTON = (By.XPATH, '//button[@class="ant-btn sino-btn" and span/text()="Add"]')

    MAXIMUM_NUMBER_OF_SKU = (By.XPATH, '//*[@id="skuQuota"]')

    # SKU相关选择器
    # Mall选择相关
    MALL_OPTION = (By.XPATH, '//div[@id="mallCode"]//div[@role="combobox"]')
    SELECTED_MALL = (By.XPATH, '//li[@role="option" and @en="Citywalk"]')

    # Shop选择相关
    SHOP_OPTION = (By.XPATH, '//span[@class="ant-form-item-children"]//span[@class="ant-select-selection ant-select-selection--multiple"]')
    SELECTED_SHOP = (By.XPATH, '//i[@class="anticon anticon-caret-down ant-select-switcher-icon"]')
    SELECTED_LOCATION = (By.XPATH, '//span[@title="BSX" and @class="ant-select-tree-node-content-wrapper ant-select-tree-node-content-wrapper-normal"]')

    # Location选择相关
    SELECTED_LOCATION = (By.XPATH, '//span[contains(@class, "ant-select-tree-title") and contains(text(), "Play to Win")]')
    SELECTED_LOCATION_ALT = (By.XPATH, '//span[contains(text(), "Booth") or contains(text(), "Promotion")]')
    STOCK = (By.XPATH, '//input[@id="stock"]')
    
    # Tag相关选择器
    TAG_EN = (By.XPATH, '//div[@id="tagEn"]//div[@role="combobox"]')
    TAG_EN_ACTIVE = (By.XPATH, '//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//li[@role="option" and text()="Citywalk"]')

    TAG_ZH = (By.XPATH, '//div[@id="tagTc"]//div[@role="combobox"]')
    TAG_ZH_ACTIVE = (By.XPATH, '//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//li[@role="option" and text()="荃新天地"]')

    TAG_ZH_HK = (By.XPATH, '//div[@id="tagSc"]//div[@role="combobox"]')
    TAG_ZH_HK_ACTIVE = (By.XPATH, '//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//li[@role="option" and text()="荃新天地"]')
    SKU_SUBMIT_BUTTON = (By.XPATH, '//div[contains(@class,"ant-modal-wrap")]//button[span/text()="Submit"]')
    SUBMIT_BUTTON = (By.XPATH, '//section[@id="main-layout"]//button[contains(@class, "ant-btn sino-btn") and @type="submit"]')

    ADDED_GIFT_NAME = (By.XPATH, '//tbody[@class="ant-table-tbody"]//td[contains(@class, "ant-table-column-has-actions")]//p[text()="Auto Test Gift"]')

    @allure.step("创建Gift")
    def add_gift(self, gift_info):
        """创建Gift"""
        try:

            # 导航到Gift创建页面
            self.driver.get(gift_info.get("gift_create_url"))
            logger.info(f"导航到Gift创建页面: {gift_info.get('gift_create_url')}")

            # 等待页面加载完成
            logger.info("等待页面加载完成")
            self.wait_for_element((By.TAG_NAME, "form"), timeout=10)
            time.sleep(2)

            # 上传缩略图
            thumbnail_file = "C:\\Users\\User\\File\\S+\\testImage\\Gift\\thumbnailImage.png"
            if os.path.exists(thumbnail_file):
                try:
                    thumbnail_element = self.driver.find_element(By.ID, "thumbnailImage")
                    thumbnail_element.send_keys(thumbnail_file)
                    logger.info("成功上传缩略图")
                except Exception as e:
                    logger.warning(f"上传缩略图失败: {e}")

            # 上传内容图
            content_file = "C:\\Users\\User\\File\\S+\\testImage\\Gift\\contentImage.png"
            if os.path.exists(content_file):
                try:
                    content_element = self.driver.find_element(By.ID, "contentImage")
                    content_element.send_keys(content_file)
                    logger.info("成功上传内容图")
                except Exception as e:
                    logger.warning(f"上传内容图失败: {e}")
        
            # 输入备注
            logger.info("输入备注信息")
            self.input_text(self.REMARKS, gift_info.get("remarks", "自动化测试备注"))
            
            # 输入所需积分
            logger.info("输入所需积分")
            self.input_text(self.POINTS_REQUIRED, str(gift_info.get("points", 100)))

            # 选择类别
            logger.info("选择Hotel类别")
            self.find_element(self.CATEGORY).click()
            time.sleep(1) 
            self.find_element(self.HOTEL_OPTION).click()
            self.find_element(self.CATEGORY_LABEL).click()
            time.sleep(2) 

            # 设置日期信息
            logger.info("开始设置日期信息")
            current_date = datetime.now().strftime("%Y-%m-%d")
            self.set_form_value(value=[current_date, current_date], date_icon_locator=self.SHOWING_DATE_ICON, picker_type='RangePicker')
            self.set_form_value(value=[current_date, current_date], date_icon_locator=self.REDEMPTION_DATE_ICON, picker_type='RangePicker')
            self.set_form_value(value=[current_date], date_icon_locator=self.EXPIRY_DATE_ICON, picker_type='DatePicker')
            time.sleep(3)
            self.find_element(self.EXPIRY_DATE_BUTTON).click()
            time.sleep(3)

            # 移动到Highlights元素并滚动，然后点击
            # 先尝试定位元素
            highlighted_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.HIGHLIGHTED)
            )


            # 滚动到元素
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", highlighted_element)
            time.sleep(2)
            logger.info("尝试JavaScript点击HIGHLIGHTED")
            self.driver.execute_script("document.querySelector('input#highlighted').click();")
            logger.info("JavaScript点击HIGHLIGHTED成功")
                
            # 移动到gift source元素并滚动，然后点击展开下拉框
            gift_source_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.GIFT_SOURCE)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", gift_source_element)
            time.sleep(2)
            
            # 点击展开下拉框
            gift_source_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_SOURCE)
            )
            gift_source_element.click()
            logger.info("成功点击GIFT_SOURCE下拉框")
            time.sleep(2)  # 等待下拉框展开

            # 选择Purchase选项
            purchase_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_SOURCE_OPTION)
            )
            purchase_option.click()
            logger.info("成功选择Purchase选项")
                
            time.sleep(1)
            self.clear_input(self.VALUE)
            self.input_text(self.VALUE, str(gift_info.get("value")))
            self.clear_input(self.COST)
            self.input_text(self.COST, str(gift_info.get("cost")))

            # 移动到gift name English元素并滚动，然后输入英文名称
            gift_name_en_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.GIFT_NAME_EN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", gift_name_en_element)
            time.sleep(2)
            gift_name_en_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_NAME_EN)
            )
            gift_name_en_element.send_keys(gift_info.get("gift_name_en"))

            # 移动到gift name 繁体元素并滚动，然后输入繁体名称
            gift_name_zh_hk_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.GIFT_NAME_ZH_HK)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", gift_name_zh_hk_element)
            time.sleep(2)
            gift_name_zh_hk_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_NAME_ZH_HK)
            )
            gift_name_zh_hk_element.send_keys(gift_info.get("gift_name_zh_hk"))


            # 移动到gift name 简体元素并滚动，然后输入简体名称
            gift_name_zh_cn_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.GIFT_NAME_ZH_CN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", gift_name_zh_cn_element)
            time.sleep(2)
            gift_name_zh_cn_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_NAME_ZH_CN)
            )
            gift_name_zh_cn_element.send_keys(gift_info.get("gift_name_zh"))

            # 移动到Add按钮并滚动，然后点击
            add_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.ADD_BUTTON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_button)
            time.sleep(2)
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.ADD_BUTTON)
            )
            add_button.click()


            self.find_element(self.MALL_OPTION).click()
            self.find_element(self.SELECTED_MALL).click()

            self.find_element(self.SHOP_OPTION).click()
            self.find_element(self.SELECTED_SHOP).click()
            self.find_element(self.SELECTED_LOCATION).click()
            self.find_element(self.SHOP_OPTION).click()

            self.find_element(self.STOCK).clear()
            self.input_text(self.STOCK, str(gift_info.get("stock")))

            self.find_element(self.TAG_EN).click()
            self.find_element(self.TAG_EN_ACTIVE).click()

            self.find_element(self.TAG_ZH).click()
            self.find_element(self.TAG_ZH_ACTIVE).click()

            time.sleep(2)
            self.find_element(self.TAG_ZH_HK).click()

            time.sleep(2)
            self.find_element(self.TAG_ZH_HK_ACTIVE).click()
    

            # 提交SKU信息
            sku_submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.SKU_SUBMIT_BUTTON)
            )
            sku_submit_button.click()
            time.sleep(3)

            # Maximum Number of SKU to redeem
            self.MAXIMUM_NUMBER_OF_SKU = self.find_element(self.MAXIMUM_NUMBER_OF_SKU).send_keys(gift_info.get("sku_number"))

            # 提交表单信息
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.SUBMIT_BUTTON)
            )   
            time.sleep(3)
            submit_button.click()
            logger.info("成功提交Gift信息")
            return True
        except Exception as e:
            logger.error(f"创建gift失败: {e}")
            return self.handle_exception(e, "创建gift")


if __name__ == '__main__':
    pytest.main()