import pytest
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.base_page import BasePage


class ExploreSection(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver
        self.channels_view = WebDriverWait(self.driver.instance, 5).until(
            EC.visibility_of_element_located((
                MobileBy.ID, "com.vice.viceforandroid:id/channel_recycler_view")))
        self.channels = None
        self.topics = None
        # self.channels = WebDriverWait(self.driver.instance, 10).until(
        #     EC.visibility_of_all_elements_located((
        #         MobileBy.ID, "com.vice.viceforandroid:id/explore_channel_background_image")))
        # self.topics = WebDriverWait(self.driver.instance, 10).until(
        #     EC.visibility_of_all_elements_located((
        #         MobileBy.ID, "com.vice.viceforandroid:id/explore_topic_background_image")))

    @pytest.allure.step("Verify the user is in the EXPLORE Section")
    def verify_user_is_in_explore_section(self):
        self.channels = WebDriverWait(self.driver.instance, 10).until(
            EC.visibility_of_all_elements_located((
                MobileBy.ID, "com.vice.viceforandroid:id/explore_channel_background_image")))

        # Scroll down
        actions = TouchAction(self.driver.instance)
        actions.press(self.channels[8]).move_to(x=100, y=100).release().perform()

        self.topics = WebDriverWait(self.driver.instance, 10).until(
            EC.visibility_of_all_elements_located((
                MobileBy.ID, "com.vice.viceforandroid:id/explore_topic_background_image")))
        channel_count = len(self.channels)
        topic_count = len(self.topics)
        assert channel_count == 14, "The amount of channels is not 14, it is: {}".format(channel_count)
        assert topic_count == 7, "The amount of topics is not 7, it is: {}".format(topic_count)
