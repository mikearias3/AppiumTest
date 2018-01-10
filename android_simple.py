import os
from time import sleep

import unittest
import pytest

from appium import webdriver

# Returns abs path relative to this file and not cwd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

userName = "michaelarias1"
accessKey = "kWuyYHGyh4YJG1fkqYhw"


class SimpleAndroidTests(unittest.TestCase):

    def test_find_elements(self):
        desired_caps = {
            'os_version': '7.1',
            'device': 'Google Pixel',
            'automationName': 'Appium',
            'app': 'bs://17291db3f312c9f7d3bc84822c6335df04837776'
        }

        self.driver = webdriver.Remote(
            "http://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)

        WebDriverWait(self.driver, 40).until(EC.visibility_of_element_located((MobileBy.ID, "com.vice.viceforandroid:id/textview_skip_btn")))
        with pytest.allure.step("Click Skip button"):
            el = self.driver.find_element_by_id("com.vice.viceforandroid:id/textview_skip_btn")
            el.click()
        with pytest.allure.step("Verify Logo is present"):
            el = self.driver.find_element_by_id("com.vice.viceforandroid:id/imageview_viceland_toolbar")
            el.click()
        with pytest.allure.step("Verify Popular Tab is present"):
            el = self.driver.find_element_by_xpath("//android.widget.TextView[@text='POPULAR']")
            el.click()
        with pytest.allure.step("Verify Latest Tab is present"):
            el = self.driver.find_element_by_xpath("//android.widget.TextView[@text='LATEST']")
            el.click()
        with pytest.allure.step("Verify footer is present"):
            el = self.driver.find_element_by_id("com.vice.viceforandroid:id/bb_bottom_bar_item_container")
            assert el.is_displayed()
        with pytest.allure.step("Click Read button"):
            el = self.driver.find_element_by_id("com.vice.viceforandroid:id/nav_read")
            el.click()
        with pytest.allure.step("Click Watch button"):
            el = self.driver.find_element_by_id("com.vice.viceforandroid:id/nav_watch")
            el.click()
        with pytest.allure.step("Click Explore button"):
            el = self.driver.find_element_by_id("com.vice.viceforandroid:id/nav_explore")
            el.click()
        with pytest.allure.step("Click Account button"):
            el = self.driver.find_element_by_id("com.vice.viceforandroid:id/nav_account")
            el.click()

    def tearDown(self):
        # end the session
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)