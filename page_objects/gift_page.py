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

    # 缩略图上传
    THUMBNAIL = (By.XPATH, '//input[@id="thumbnailImage"]')

    # 内容图上传
    CONTENT = (By.XPATH, '//input[@id="contentImage"]')

    # Remarks输入框
    REMARKS = (By.XPATH, '//textarea[@id="rewardRemark"]')

    # Points Required输入框
    POINTS_REQUIRED = (By.XPATH, '//input[@id="pointsNeeded"]')

    # Category下拉框
    CATEGORY = (By.XPATH, '//input[@id="categoryCodeList"]')
    # Category 选项值(Hotel)
    HOTEL_OPTION = (By.XPATH, "//li[contains(@class, 'ant-select-dropdown-menu-item') and contains(text(), 'Hotel')]")
    # Category 字段名
    CATEGORY_LABEL = (By.XPATH, '//*[@id="main-layout"]/main/div/div/div/div/form/div[5]/div[1]/label/span')

    # Showing Date日期
    SHOWING_DATE_ICON = (By.XPATH, "//span[@id='showingDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    # Redemption Date日期
    REDEMPTION_DATE_ICON = (By.XPATH, "//span[@id='reservationDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    # Expiry Date日期
    EXPIRY_DATE_ICON = (By.XPATH, "//span[@id='expiryDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    # Expiry Date的OK按钮
    EXPIRY_DATE_BUTTON = (By.XPATH, "//div[contains(@class, 'ant-calendar-footer')]//a[contains(@class, 'ant-calendar-ok-btn') and @role='button']")

    # HIGHLIGHTED复选框
    HIGHLIGHTED = (By.XPATH, '//input[@id="highlighted"]')

    # Gift Source下拉框
    GIFT_SOURCE = (By.XPATH, '//div[@id="giftSource"]//div[@class="ant-select-selection__rendered"]')
    # Gift Source选项值(Purchase)
    GIFT_SOURCE_OPTION = (By.XPATH, '//div[contains(@class,"ant-select-dropdown") and not(contains(@class,"hidden"))]//li[@role="option" and contains(., "Purchase")]')
    # value和cost输入框
    VALUE = (By.XPATH, '//div[@class="ant-input-number-input-wrap"]//input[@id="value"]')
    COST = (By.XPATH, '//div[@class="ant-input-number-input-wrap"]//input[@id="cost"]')

    # Gift Name输入框（EN、TC、SC）
    GIFT_NAME_EN = (By.XPATH, '//input[@id="en.title"]')
    GIFT_NAME_ZH_CN = (By.XPATH, '//input[@id="zh-cn.title"]')
    GIFT_NAME_ZH_HK = (By.XPATH, '//input[@id="zh-hk.title"]')

    # SKU添加按钮
    ADD_BUTTON = (By.XPATH, '//button[@class="ant-btn sino-btn" and span/text()="Add"]')

    # Maximum Number of SKU输入框    
    MAXIMUM_NUMBER_OF_SKU = (By.XPATH, '//*[@id="skuQuota"]')

    # Mall下拉框
    MALL_OPTION = (By.XPATH, '//div[@id="mallCode"]//div[@role="combobox"]')
    # Mall选项值(Citywalk)
    SELECTED_MALL = (By.XPATH, '//li[@role="option" and @en="Citywalk"]')

    # Shop下拉框
    SHOP_OPTION = (By.XPATH, '//span[@class="ant-form-item-children"]//span[@class="ant-select-selection ant-select-selection--multiple"]')
    # Shop 下拉Icon
    SELECTED_SHOP = (By.XPATH, '//i[@class="anticon anticon-caret-down ant-select-switcher-icon"]')
    # 选择的Location
    SELECTED_LOCATION = (By.XPATH, '//span[@title="BSX" and @class="ant-select-tree-node-content-wrapper ant-select-tree-node-content-wrapper-normal"]')

    # # Location选择相关
    # SELECTED_LOCATION = (By.XPATH, '//span[contains(@class, "ant-select-tree-title") and contains(text(), "Play to Win")]')
    # SELECTED_LOCATION_ALT = (By.XPATH, '//span[contains(text(), "Booth") or contains(text(), "Promotion")]')
    
    # Stock输入框
    STOCK = (By.XPATH, '//input[@id="stock"]')
    
    # Tag 下拉框
    TAG_EN = (By.XPATH, '//div[@id="tagEn"]//div[@role="combobox"]')
    #Tag 选项值(Citywalk)
    TAG_EN_ACTIVE = (By.XPATH, '//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//li[@role="option" and text()="Citywalk"]')

    # Tag 繁体中文输入框
    TAG_ZH = (By.XPATH, '//div[@id="tagTc"]//div[@role="combobox"]')
    # Tag 繁体中文选项值(荃新天地)
    TAG_ZH_ACTIVE = (By.XPATH, '//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//li[@role="option" and text()="荃新天地"]')
   
    # Tag 繁体中文输入框
    TAG_ZH_HK = (By.XPATH, '//div[@id="tagSc"]//div[@role="combobox"]')
    # Tag 繁体中文选项值(荃新天地)
    TAG_ZH_HK_ACTIVE = (By.XPATH, '//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//li[@role="option" and text()="荃新天地"]')
    
    # SKU提交按钮
    SKU_SUBMIT_BUTTON = (By.XPATH, '//div[contains(@class,"ant-modal-wrap")]//button[span/text()="Submit"]')
    # Gift  提交按钮
    SUBMIT_BUTTON = (By.XPATH, '//section[@id="main-layout"]//button[contains(@class, "ant-btn sino-btn") and @type="submit"]')

    # 已添加的Gift名称
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

            # # 上传缩略图
            logger.info("上传缩略图")
            self.upload_thumbnail(gift_info.get("thumbnail_file"), "thumbnailImage")

            # 上传内容图
            logger.info("上传内容图")
            self.upload_thumbnail(gift_info.get("content_file"), "contentImage")
        
            # 输入remarks
            logger.info("输入remarks信息")
            self.input_text(self.REMARKS, gift_info.get("remarks", "自动化测试备注"))
            
            # 输入Points Required
            logger.info("输入Points Required信息")
            self.input_text(self.POINTS_REQUIRED, str(gift_info.get("points", 100)))

            # 选择Category为Hotel
            logger.info("选择Category为Hotel")
            self.find_element(self.CATEGORY).click()
            time.sleep(1) 
            self.find_element(self.HOTEL_OPTION).click()
            self.find_element(self.CATEGORY_LABEL).click()
            time.sleep(2) 

            # 设置日期信息
            logger.info("开始设置日期信息,包括Showing Date, Redemption Date和Expiry Date")
            current_date = datetime.now().strftime("%Y-%m-%d")
            self.set_form_value(value=[current_date, current_date], date_icon_locator=self.SHOWING_DATE_ICON, picker_type='RangePicker')
            self.set_form_value(value=[current_date, current_date], date_icon_locator=self.REDEMPTION_DATE_ICON, picker_type='RangePicker')
            self.set_form_value(value=[current_date], date_icon_locator=self.EXPIRY_DATE_ICON, picker_type='DatePicker')
            time.sleep(3)
            self.find_element(self.EXPIRY_DATE_BUTTON).click()
            time.sleep(3)

            # 勾选HIGHLIGHTED复选框
            logger.info("勾选HIGHLIGHTED复选框")
            self.scroll_to_element(locator=self.HIGHLIGHTED)
            # 尝试JavaScript点击HIGHLIGHTED
            self.driver.execute_script("document.querySelector('input#highlighted').click();")
            logger.info("JavaScript点击HIGHLIGHTED成功")
                
            # 选择gift source
            self.scroll_to_element(locator=self.GIFT_SOURCE)
            # 点击展开gift source下拉框
            gift_source_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_SOURCE)
            )
            gift_source_element.click()
            logger.info("成功点击GIFT_SOURCE下拉框")
            time.sleep(2)

            # 选择Purchase选项,输入value、cost
            purchase_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_SOURCE_OPTION)
            )
            purchase_option.click()
            time.sleep(1)
            self.clear_input(self.VALUE)
            self.input_text(self.VALUE, str(gift_info.get("value")))
            self.clear_input(self.COST)
            self.input_text(self.COST, str(gift_info.get("cost")))

            # 输入gift name英文名称
            logger.info("输入gift name英文名称")
            self.scroll_to_element(locator=self.GIFT_NAME_EN)
            # 等待gift name英文输入框可点击
            gift_name_en_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_NAME_EN)
            )
            gift_name_en_element.send_keys(gift_info.get("gift_name_en"))

            # 输入gift name繁体名称
            logger.info("输入gift name繁体名称")
            self.scroll_to_element(locator=self.GIFT_NAME_ZH_HK)
            # 等待gift name繁体中文输入框可点击
            gift_name_zh_hk_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_NAME_ZH_HK)
            )
            gift_name_zh_hk_element.send_keys(gift_info.get("gift_name_zh_hk"))


            # 输入gift name简体名称
            logger.info("输入gift name简体名称")
            self.scroll_to_element(locator=self.GIFT_NAME_ZH_CN)
            # 等待gift name简体中文输入框可点击
            gift_name_zh_cn_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.GIFT_NAME_ZH_CN)
            )
            gift_name_zh_cn_element.send_keys(gift_info.get("gift_name_zh"))

            # 点击Add按钮
            logger.info("点击Add按钮添加SKU")
            self.scroll_to_element(locator=self.ADD_BUTTON)
            # 等待Add按钮可点击
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.ADD_BUTTON)
            )
            add_button.click()

            # Add SKU表单
            # Mall下拉框
            self.find_element(self.MALL_OPTION).click()
            # Mall 选项值(Citywalk)
            self.find_element(self.SELECTED_MALL).click()

            # Shop下拉框
            self.find_element(self.SHOP_OPTION).click()
            # Shop 选项值(Citywalk)
            self.find_element(self.SELECTED_SHOP).click()
            # 选择Location
            time.sleep(2)
            self.find_element(self.SELECTED_LOCATION).click()
            # 点击shop下拉框
            self.find_element(self.SHOP_OPTION).click()

            # 输入Stock
            self.find_element(self.STOCK).clear()
            # 输入Stock数量
            self.input_text(self.STOCK, str(gift_info.get("stock")))

            # Tag下拉框EN
            self.find_element(self.TAG_EN).click()
            # Tag 选项值(Citywalk)
            self.find_element(self.TAG_EN_ACTIVE).click()

            # Tag下拉框繁体中文
            self.find_element(self.TAG_ZH).click()
            # Tag 繁体中文选项值(荃新天地)
            self.find_element(self.TAG_ZH_ACTIVE).click()
            time.sleep(2)

            # Tag下拉框简体中文
            self.find_element(self.TAG_ZH_HK).click()
            time.sleep(2)
            # Tag 简体中文选项值(荃新天地)
            self.find_element(self.TAG_ZH_HK_ACTIVE).click()
    
            # 提交SKU表单信息
            sku_submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.SKU_SUBMIT_BUTTON)
            )
            sku_submit_button.click()
            time.sleep(3)

            # Maximum Number of SKU to redeem
            self.MAXIMUM_NUMBER_OF_SKU = self.find_element(self.MAXIMUM_NUMBER_OF_SKU).send_keys(gift_info.get("sku_number"))

            # 提交Gift表单信息
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