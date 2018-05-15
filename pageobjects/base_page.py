import pytest
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.logo = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.ID, "com.vice.viceforandroid:id/imageview_viceland_toolbar")))
        self.read_button = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.ID, "com.vice.viceforandroid:id/nav_read")))
        self.watch_button = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.ID, "com.vice.viceforandroid:id/nav_watch")))
        self.explore_button = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.ID, "com.vice.viceforandroid:id/nav_explore")))
        self.account_button = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.ID, "com.vice.viceforandroid:id/nav_account")))

    @pytest.allure.step("Click Read button")
    def click_read_button(self):
        self.read_button.click()

    @pytest.allure.step("Click Watch button")
    def click_watch_button(self):
        self.watch_button.click()

    @pytest.allure.step("Click Explore button")
    def click_explore_button(self):
        self.explore_button.click()

    @pytest.allure.step("Click Account button")
    def click_account_button(self):
        self.account_button.click()
