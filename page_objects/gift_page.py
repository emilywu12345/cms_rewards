import time
import allure
import os
import sys
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 添加项目根目录到 Python 路径，以支持独立运行
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from page_objects.base_page import BasePage
from utils.log_manager import logger

class GiftPage(BasePage):
    """礼物页面对象，包含所有礼物相关操作"""

    # 页面元素定位器 - 使用更通用的定位方式
    REMARKS = (By.XPATH, '//textarea[@id="rewardRemark"]')
    POINTS_REQUIRED = (By.XPATH, '//input[@id="pointsNeeded"]')
    CATEGORY = (By.XPATH, '//input[@id="categoryCodeList"]')
    CATEGORY_LABEL = (By.XPATH, '//*[@id="main-layout"]/main/div/div/div/div/form/div[5]/div[1]/label/span')
    HOTEL_OPTION = (By.XPATH, "//li[contains(@class, 'ant-select-dropdown-menu-item') and contains(text(), 'Hotel')]")

    # 日期字段定位器 - 根据实际HTML结构优化
    # Showing Date (日期范围选择器)
    SHOWING_DATE_START = (By.XPATH, "//span[@id='showingDate']//input[@placeholder='Start date']")
    SHOWING_DATE_END = (By.XPATH, "//span[@id='showingDate']//input[@placeholder='End date']")
    SHOWING_DATE_ICON = (By.XPATH, "//span[@id='showingDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    
    # Redemption Date (兑换日期范围选择器) - 注意实际id是reservationDate
    REDEMPTION_DATE_CONTAINER = (By.ID, "reservationDate")
    REDEMPTION_DATE_START = (By.XPATH, "//span[@id='reservationDate']//input[@placeholder='Start date']")
    REDEMPTION_DATE_END = (By.XPATH, "//span[@id='reservationDate']//input[@placeholder='End date']")
    REDEMPTION_DATE_ICON = (By.XPATH, "//span[@id='reservationDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    
    # Expiry Date (过期日期单选择器)
    EXPIRY_DATE_CONTAINER = (By.ID, "expiryDate")
    EXPIRY_DATE_INPUT = (By.XPATH, "//span[@id='expiryDate']//input[contains(@class, 'ant-calendar-picker-input')]")
    EXPIRY_DATE_ICON = (By.XPATH, "//span[@id='expiryDate']//i[contains(@class, 'ant-calendar-picker-icon')]")
    
    # 日期选择器相关按钮
    CALENDAR_OK_BUTTON = (By.XPATH, "//a[contains(@class, 'ant-calendar-ok-btn')]")
    CALENDAR_TODAY_BUTTON = (By.XPATH, "//a[contains(@class, 'ant-calendar-today-btn')]")
    CALENDAR_CLEAR_BUTTON = (By.XPATH, "//a[contains(@class, 'ant-calendar-clear-btn')]")


    # 复选框 - 使用更通用的定位器
    HIGHLIGHTED = (By.XPATH, '//input[@id="highlighted"]')
    HIGHLIGHTED_ALT = (By.XPATH, '//input[@type="checkbox" and contains(@id, "highlighted")]')
    HIGHLIGHTED_LABEL = (By.XPATH, '//label[contains(text(), "Highlighted")]//input')
    
    ENABLED = (By.XPATH, '//input[@id="enabled"]')
    ENABLED_ALT = (By.XPATH, '//input[@type="checkbox" and contains(@id, "enabled")]')
    ENABLED_LABEL = (By.XPATH, '//label[contains(text(), "Enabled")]//input')
    
    CAN_RESERVE_IN_APP = (By.XPATH, '//input[@id="canReserveInApp"]')
    CAN_RESERVE_IN_APP_ALT = (By.XPATH, '//input[@type="checkbox" and contains(@id, "canReserveInApp")]')
    CAN_RESERVE_IN_APP_LABEL = (By.XPATH, '//label[contains(text(), "Can Reserve In App")]//input')
    
    CAN_RESERVE_IN_CMS = (By.XPATH, '//input[@id="canReserveInCms"]')
    CAN_RESERVE_IN_CMS_ALT = (By.XPATH, '//input[@type="checkbox" and contains(@id, "canReserveInCms")]')
    CAN_RESERVE_IN_CMS_LABEL = (By.XPATH, '//label[contains(text(), "Can Reserve In CMS")]//input')
    
    # 其他字段
    GIFT_SOURCE = (By.XPATH, '//div[contains(@class, "ant-select-selection__rendered")]/div[contains(@class, "ant-select-selection-selected-value")]')
    GIFT_SOURCE_ALT = (By.XPATH, '//span[text()="Purchase"]')
    VALUE = (By.XPATH, '//input[contains(@class, "ant-input-number")]')
    COST = (By.XPATH, '//input[@id="cost"]')

    GIFT_NAME_EN = (By.XPATH, '//input[@id="en.title"]')
    GIFT_NAME_ZH = (By.XPATH, '//input[@id="zh-cn.title"]')
    GIFT_NAME_ZH_HK = (By.XPATH, '//input[@id="zh-hk.title"]')

    ADD_BUTTON = (By.XPATH, '//button[@class="ant-btn sino-btn" and span/text()="Add"]')
    
    # SKU相关选择器 - 更通用的定位器，支持动态查找
    # Mall选择相关
    MALL_OPTION = (By.XPATH, '//li[contains(@class, "ant-select-dropdown-menu-item") and text()="Mall"]')
    SELECTED_MALL = (By.XPATH, '//span[contains(@class, "ant-select-tree-title") and text()="Citywalk"]')

    # Shop选择相关
    SHOP_OPTION = (By.XPATH, '//li[contains(@class, "ant-select-dropdown-menu-item") and text()="Shop"]')
    SELECTED_SHOP = (By.XPATH, '//span[contains(@class, "ant-select-tree-title") and contains(text(), "Shop")]')
    
    # Location选择相关
    SELECTED_LOCATION = (By.XPATH, '//span[contains(@class, "ant-select-tree-title") and contains(text(), "Play to Win")]')
    SELECTED_LOCATION_ALT = (By.XPATH, '//span[contains(text(), "Booth") or contains(text(), "Promotion")]')
    
    STOCK = (By.XPATH, '//input[@id="stock"]')
    
    # Tag相关选择器 - 增加更具体的定位器
    TAG_EN = (By.XPATH, '//i[contains(@class, "anticon-down")]//svg')
    TAG_EN_ACTIVE = (By.XPATH, '//li[@role="option" and text()="Citywalk"]')
    SELECTED_TAG_EN = (By.XPATH, '//li[@role="option" and text()="Citywalk"]')

    TAG_ZH = (By.XPATH, '//span[contains(@class, "ant-select-arrow")]//i[contains(@class, "anticon-down")]')
    TAG_ZH_ACTIVE = (By.XPATH, '//li[@role="option" and text()="荃新天地"]')
    SELECTED_TAG_ZH = (By.XPATH, '//li[@role="option" and text()="荃新天地" and @aria-selected="false"]')

    TAG_ZH_HK = (By.XPATH, '//i[contains(@class, "anticon-down")]//svg')
    TAG_ZH_HK_ACTIVE = (By.XPATH, '//li[@role="option" and text()="荃新天地"]')
    SELECTED_TAG_ZH_HK = (By.XPATH, '//li[@role="option" and text()="荃新天地"]')
    SKU_SUBMIT_BUTTON = (By.XPATH, '//button[span/text()="Submit"]')

    SUBMIT_BUTTON = (By.XPATH, '//button[@type="submit" and span/text()="Submit"]')

    @allure.step("添加礼物")
    def add_gift(self, gift_info):
        """添加礼物"""
        try:
            # 导航到礼物创建页面
            gift_create_url = "https://admincms-uat-cicd.splusrewards.com.hk/gift/create"
            self.driver.get(gift_create_url)
            logger.info(f"导航到礼物创建页面: {gift_create_url}")
            
            # 等待页面加载完成
            logger.info("等待页面加载完成")
            self.wait_for_element((By.TAG_NAME, "form"), timeout=10)
            time.sleep(2)

            # # 上传缩略图
            # thumbnail_file = "C:\\Users\\User\\File\\S+\\testImage\\Gift\\thumbnailImage.png"
            # thumbnail_element = self.driver.find_element(By.ID, "thumbnailImage")
            # thumbnail_element.send_keys(thumbnail_file)

            # # 上传内容图
            # content_file = "C:\\Users\\User\\File\\S+\\testImage\\Gift\\contentImage.png"
            # content_element = self.driver.find_element(By.ID, "contentImage")
            # content_element.send_keys(content_file)
        
            # # 输入备注
            # logger.info("输入备注信息")
            # self.input_text(self.REMARKS, gift_info.get("remarks", "自动化测试备注"))
            
            # # 输入所需积分
            # logger.info("输入所需积分")
            # self.input_text(self.POINTS_REQUIRED, str(gift_info.get("points", 100)))

            # # 选择类别
            # logger.info("选择Hotel类别")
            # self.find_element(self.CATEGORY).click()
            # time.sleep(1) 
            # self.find_element(self.HOTEL_OPTION).click()
            # self.find_element(self.CATEGORY_LABEL).click()
            # time.sleep(2) 

            # 设置日期信息
            # logger.info("开始设置日期信息")
            # 使用优化的日期设置方法
            # self._set_date_fields_optimized()

            # 1. 定位开始日期输入框（placeholder="Start date"）
            # start_element = self.driver.find_element(
            #     By.XPATH, 
            #     "//input[contains(@class, 'ant-calendar-range-picker-input') and @placeholder='Start date']"
            # )
            # # 赋值开始日期
            # self.driver.execute_script(
            #     "arguments[0].value = '2025-07-08 12:00:00';", 
            #     start_element
            # )
            # self.driver.execute_script(
            #     "arguments[0].dispatchEvent(new Event('change'));", 
            #     start_element
            # )

            # # 定位结束日期输入框（placeholder="End date"）
            # end_element = self.driver.find_element(
            #     By.XPATH, 
            #     "//input[contains(@class, 'ant-calendar-range-picker-input') and @placeholder='End date']"
            # )
            # # 赋值结束日期（示例：比开始日期晚 1 小时）
            # self.driver.execute_script(
            #     "arguments[0].value = '2025-07-08 13:00:00';", 
            #     end_element
            # )
            # self.driver.execute_script(
            #     "arguments[0].dispatchEvent(new Event('change'));", 
            #     end_element
            # )



            # 优化的日期设置方法 - 解决清空问题
            # 先点击日期选择器图标激活组件
            self.find_element(self.SHOWING_DATE_ICON).click()
            time.sleep(2)  # 等待日期选择器激活
            
            # 设置showingDate开始日期
            start_element = self.driver.find_element(
                By.XPATH, 
                "//span[@id='showingDate']//input[contains(@class, 'ant-calendar-range-picker-input') and @placeholder='Start date']"
            )
            
            # 使用更强化的JavaScript设置方法，彻底防止清空
            self.driver.execute_script("""
                var input = arguments[0];
                var value = arguments[1];
                
                console.log('开始设置日期:', value);
                
                // 强制移除所有限制属性
                input.removeAttribute('readonly');
                input.removeAttribute('disabled');
                input.style.pointerEvents = 'auto';
                
                // 强制聚焦
                input.focus();
                input.click();
                
                // 清空当前值
                input.value = '';
                input.defaultValue = '';
                
                // 设置新值
                input.value = value;
                input.defaultValue = value;
                
                // 立即触发所有可能的事件
                var events = ['focus', 'input', 'change', 'keydown', 'keyup', 'blur'];
                events.forEach(function(eventType) {
                    var event = new Event(eventType, {
                        bubbles: true, 
                        cancelable: true,
                        view: window
                    });
                    input.dispatchEvent(event);
                });
                
                // 特别处理React组件
                if (input._reactInternalFiber || input._reactInternalInstance || input.__reactInternalInstance) {
                    // 触发React onChange
                    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    nativeInputValueSetter.call(input, value);
                    
                    var reactEvent = new Event('input', { bubbles: true });
                    input.dispatchEvent(reactEvent);
                }
                
                // 设置多重备用属性
                input.setAttribute('data-value', value);
                input.setAttribute('title', value);
                input.setAttribute('aria-valuenow', value);
                
                // 防止组件重新渲染时清空
                Object.defineProperty(input, 'value', {
                    get: function() { return value; },
                    set: function(newValue) { 
                        if (newValue !== value && newValue !== '') {
                            this.setAttribute('value', newValue);
                        }
                    }
                });
                
                console.log('日期设置完成:', input.value);
                return true;
            """, start_element, "2025-07-08")
            
            time.sleep(2)  # 等待设置完成
            
            # 设置showingDate结束日期
            end_element = self.driver.find_element(
                By.XPATH, 
                "//span[@id='showingDate']//input[contains(@class, 'ant-calendar-range-picker-input') and @placeholder='End date']"
            )
            
            # 使用相同的强化方法设置结束日期
            self.driver.execute_script("""
                var input = arguments[0];
                var value = arguments[1];
                
                console.log('开始设置结束日期:', value);
                
                input.removeAttribute('readonly');
                input.removeAttribute('disabled');
                input.style.pointerEvents = 'auto';
                
                input.focus();
                input.click();
                
                input.value = '';
                input.defaultValue = '';
                
                input.value = value;
                input.defaultValue = value;
                
                var events = ['focus', 'input', 'change', 'keydown', 'keyup', 'blur'];
                events.forEach(function(eventType) {
                    var event = new Event(eventType, {
                        bubbles: true, 
                        cancelable: true,
                        view: window
                    });
                    input.dispatchEvent(event);
                });
                
                if (input._reactInternalFiber || input._reactInternalInstance || input.__reactInternalInstance) {
                    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    nativeInputValueSetter.call(input, value);
                    
                    var reactEvent = new Event('input', { bubbles: true });
                    input.dispatchEvent(reactEvent);
                }
                
                input.setAttribute('data-value', value);
                input.setAttribute('title', value);
                input.setAttribute('aria-valuenow', value);
                
                Object.defineProperty(input, 'value', {
                    get: function() { return value; },
                    set: function(newValue) { 
                        if (newValue !== value && newValue !== '') {
                            this.setAttribute('value', newValue);
                        }
                    }
                });
                
                console.log('结束日期设置完成:', input.value);
                return true;
            """, end_element, "2025-07-09")

            time.sleep(2)  # 等待设置完成
            
            # 点击页面其他地方关闭日期选择器
            self.driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(1)
            

            # 设置Redemption Date开始日期
            start_element = self.driver.find_element(
                By.XPATH, 
                "//span[@id='reservationDate']//input[contains(@class, 'ant-calendar-range-picker-input') and @placeholder='Start date']"
            )
            
            # 使用更强化的JavaScript设置方法，彻底防止清空
            self.driver.execute_script("""
                var input = arguments[0];
                var value = arguments[1];
                
                console.log('开始设置日期:', value);
                
                // 强制移除所有限制属性
                input.removeAttribute('readonly');
                input.removeAttribute('disabled');
                input.style.pointerEvents = 'auto';
                
                // 强制聚焦
                input.focus();
                input.click();
                
                // 清空当前值
                input.value = '';
                input.defaultValue = '';
                
                // 设置新值
                input.value = value;
                input.defaultValue = value;
                
                // 立即触发所有可能的事件
                var events = ['focus', 'input', 'change', 'keydown', 'keyup', 'blur'];
                events.forEach(function(eventType) {
                    var event = new Event(eventType, {
                        bubbles: true, 
                        cancelable: true,
                        view: window
                    });
                    input.dispatchEvent(event);
                });
                
                // 特别处理React组件
                if (input._reactInternalFiber || input._reactInternalInstance || input.__reactInternalInstance) {
                    // 触发React onChange
                    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    nativeInputValueSetter.call(input, value);
                    
                    var reactEvent = new Event('input', { bubbles: true });
                    input.dispatchEvent(reactEvent);
                }
                
                // 设置多重备用属性
                input.setAttribute('data-value', value);
                input.setAttribute('title', value);
                input.setAttribute('aria-valuenow', value);
                
                // 防止组件重新渲染时清空
                Object.defineProperty(input, 'value', {
                    get: function() { return value; },
                    set: function(newValue) { 
                        if (newValue !== value && newValue !== '') {
                            this.setAttribute('value', newValue);
                        }
                    }
                });
                
                console.log('日期设置完成:', input.value);
                return true;
            """, start_element, "2025-07-08")
            
            time.sleep(2)  # 等待设置完成

            # 设置Redemption Date结束日期
            end_element = self.driver.find_element(
                By.XPATH, 
                "//span[@id='reservationDate']//input[contains(@class, 'ant-calendar-range-picker-input') and @placeholder='End date']"
            )
            
            # 使用相同的强化方法设置结束日期
            self.driver.execute_script("""
                var input = arguments[0];
                var value = arguments[1];
                
                console.log('开始设置结束日期:', value);
                
                input.removeAttribute('readonly');
                input.removeAttribute('disabled');
                input.style.pointerEvents = 'auto';
                
                input.focus();
                input.click();
                
                input.value = '';
                input.defaultValue = '';
                
                input.value = value;
                input.defaultValue = value;
                
                var events = ['focus', 'input', 'change', 'keydown', 'keyup', 'blur'];
                events.forEach(function(eventType) {
                    var event = new Event(eventType, {
                        bubbles: true, 
                        cancelable: true,
                        view: window
                    });
                    input.dispatchEvent(event);
                });
                
                if (input._reactInternalFiber || input._reactInternalInstance || input.__reactInternalInstance) {
                    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    nativeInputValueSetter.call(input, value);
                    
                    var reactEvent = new Event('input', { bubbles: true });
                    input.dispatchEvent(reactEvent);
                }
                
                input.setAttribute('data-value', value);
                input.setAttribute('title', value);
                input.setAttribute('aria-valuenow', value);
                
                Object.defineProperty(input, 'value', {
                    get: function() { return value; },
                    set: function(newValue) { 
                        if (newValue !== value && newValue !== '') {
                            this.setAttribute('value', newValue);
                        }
                    }
                });
                
                console.log('结束日期设置完成:', input.value);
                return true;
            """, end_element, "2025-07-09")


            # 点击页面其他地方关闭日期选择器
            self.driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(1)


            # 设置Expiry Date开始日期
            start_element = self.driver.find_element(
                By.XPATH, 
                "//span[@id='expiryDate']//input[contains(@class, 'ant-calendar-picker')]"
            )
            
            # 使用更强化的JavaScript设置方法，彻底防止清空
            self.driver.execute_script("""
                var input = arguments[0];
                var value = arguments[1];
                
                console.log('开始设置日期:', value);
                
                // 强制移除所有限制属性
                input.removeAttribute('readonly');
                input.removeAttribute('disabled');
                input.style.pointerEvents = 'auto';
                
                // 强制聚焦
                input.focus();
                input.click();
                
                // 清空当前值
                input.value = '';
                input.defaultValue = '';
                
                // 设置新值
                input.value = value;
                input.defaultValue = value;
                
                // 立即触发所有可能的事件
                var events = ['focus', 'input', 'change', 'keydown', 'keyup', 'blur'];
                events.forEach(function(eventType) {
                    var event = new Event(eventType, {
                        bubbles: true, 
                        cancelable: true,
                        view: window
                    });
                    input.dispatchEvent(event);
                });
                
                // 特别处理React组件
                if (input._reactInternalFiber || input._reactInternalInstance || input.__reactInternalInstance) {
                    // 触发React onChange
                    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    nativeInputValueSetter.call(input, value);
                    
                    var reactEvent = new Event('input', { bubbles: true });
                    input.dispatchEvent(reactEvent);
                }
                
                // 设置多重备用属性
                input.setAttribute('data-value', value);
                input.setAttribute('title', value);
                input.setAttribute('aria-valuenow', value);
                
                // 防止组件重新渲染时清空
                Object.defineProperty(input, 'value', {
                    get: function() { return value; },
                    set: function(newValue) { 
                        if (newValue !== value && newValue !== '') {
                            this.setAttribute('value', newValue);
                        }
                    }
                });
                
                console.log('日期设置完成:', input.value);
                return true;
            """, start_element, "2025-07-30")


            


            self.find_element(self.CATEGORY_LABEL).click()
            # time.sleep(3)

            logger.info("礼物添加流程成功完成")
            return True

        except Exception as e:
            logger.error(f"添加礼物失败: {e}")
            return self.handle_exception(e, "添加gift")

    