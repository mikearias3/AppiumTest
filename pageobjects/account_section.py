import pytest
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.base_page import BasePage


class AccountSection(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver
        self.about_header = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.ID, "com.vice.viceforandroid:id/about_section_header")))

    @pytest.allure.step("Verify the user is in the ACCOUNT Section")
    def verify_user_is_in_account_section(self):
        assert self.about_header.is_displayed(), "About header is not showing up"
