import pytest
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.base_page import BasePage


class ReadSection(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver
        self.popular_tab = WebDriverWait(self.driver.instance, 15).until(
            EC.visibility_of_element_located((
                MobileBy.XPATH, "//android.support.v7.app.ActionBar.Tab[1]/android.widget.TextView")))
        self.latest_tab = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.XPATH, "//android.support.v7.app.ActionBar.Tab[2]/android.widget.TextView")))

    @pytest.allure.step("Verify the user is in the READ Section")
    def verify_user_is_in_read_section(self):
        assert self.popular_tab.text == "POPULAR", "Tab is not a POPULAR tab."
        assert self.latest_tab.text == "LATEST", "Tab is not a LATEST tab."
