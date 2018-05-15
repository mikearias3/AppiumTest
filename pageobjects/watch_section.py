import pytest
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.base_page import BasePage


class WatchSection(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver

    def verify_user_is_in_watch_section(self):
        # TODO: Not yet implemented
        assert False
