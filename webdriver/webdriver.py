from appium import webdriver

userName = "michaelarias1"
accessKey = "kWuyYHGyh4YJG1fkqYhw"


class Driver:

    def __init__(self):
        # desired_caps = {
        #     'os_version': '7.1',
        #     'device': 'Google Pixel',
        #     'automationName': 'Appium',
        #     'app': 'bs://10db4ee5484678b9c8aa138ade5dfd041d7ee167'
        # }
        #
        # self.instance = webdriver.Remote(
        #     "http://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)

        desired_caps = {
            'platformName': 'android',
            'deviceName': 'ONEPLUS A3000',
            'appPackage': 'com.vice.viceforandroid',
            'appActivity': 'com.vice.sharedcode.UI.LaunchActivity'
        }

        self.instance = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
