import os
import unittest

from pageobjects.account_section import AccountSection
from pageobjects.explore_section import ExploreSection
from pageobjects.read_section import ReadSection
from pageobjects.watch_section import WatchSection
from pageobjects.welcome_overlay import WelcomeOverlay
from webdriver.webdriver import Driver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class SimpleAndroidTests(unittest.TestCase):

    def setUp(self):
        self.driver = Driver()
        welcome_overlay = WelcomeOverlay(self.driver)
        welcome_overlay.click_skip_button()

    def test_user_taps_read_button(self):
        read_section = ReadSection(self.driver)
        read_section.click_read_button()
        read_section.verify_user_is_in_read_section()

    def test_user_taps_watch_button(self):
        read_section = ReadSection(self.driver)
        read_section.click_watch_button()

        watch_section = WatchSection(self.driver)
        watch_section.verify_user_is_in_watch_section()

    def test_user_taps_explore_button(self):
        read_section = ReadSection(self.driver)
        read_section.click_explore_button()

        explore_section = ExploreSection(self.driver)
        explore_section.verify_user_is_in_explore_section()

    def test_user_taps_account_button(self):
        read_section = ReadSection(self.driver)
        read_section.click_account_button()

        account_section = AccountSection(self.driver)
        account_section.verify_user_is_in_account_section()

    def tearDown(self):
        # end the session
        self.driver.instance.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)