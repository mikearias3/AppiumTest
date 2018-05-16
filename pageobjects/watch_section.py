import pytest
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.base_page import BasePage


class WatchSection(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver
        self.latest_tab = WebDriverWait(self.driver.instance, 15).until(
            EC.visibility_of_element_located((
                MobileBy.XPATH, "//android.support.v7.app.ActionBar.Tab[1]/android.widget.TextView")))
        self.shows_tab = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.XPATH, "//android.support.v7.app.ActionBar.Tab[2]/android.widget.TextView")))

    @pytest.allure.step("Verify the user is in the READ Section")
    def verify_user_is_in_watch_section(self):
        assert self.latest_tab.text == "LATEST", "Tab is not a LATEST tab."
        assert self.shows_tab.text == "SHOWS", "Tab is not a SHOWS tab."
