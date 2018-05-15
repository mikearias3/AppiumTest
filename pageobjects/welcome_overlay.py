import pytest
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WelcomeOverlay:

    def __init__(self, driver):
        self.driver = driver
        self.skip_button = WebDriverWait(self.driver.instance, 40).until(
            EC.visibility_of_element_located((
                MobileBy.ID, "com.vice.viceforandroid:id/textview_skip_btn")))

    @pytest.allure.step("Click Skip Button")
    def click_skip_button(self):
        self.skip_button.click()
