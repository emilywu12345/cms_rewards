import allure
import os

def take_screenshot(driver, name):
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    file_path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(file_path)
    
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )