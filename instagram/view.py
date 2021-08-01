from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Viewer:
    """Viewer: can login and view stories and post media. Returns page html"""

    def __init__(self, username, password, driver=None):
        self.username = username
        self.password = password
        self.driver = driver if driver else Viewer.get_driver()

    @staticmethod
    def get_driver():
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        return webdriver.Firefox(options=options)

    def close_driver(self):
        self.driver.quit()

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        sleep(5)
        try:
            self.driver.find_element_by_xpath(
                "//input[@name='username']").send_keys(self.username)
            self.driver.find_element_by_xpath(
                "//input[@name='password']").send_keys(self.password)
            self.driver.find_element_by_xpath(
                "//button[contains(.,'Log In')]").click()
            sleep(10)
            self.driver.get('https://www.instagram.com/')
        except NoSuchElementException:
            raise LookupError(
                (
                    "Login elements haven't found: bad timings or page_source "
                    "has changed"
                )
            )

    def get_story_html(self, story_url):
        self.driver.get(story_url)
        sleep(2)
        try:
            self.driver.find_element_by_xpath(
                "//button[contains(.,'View Story')]").click()
            sleep(1)
            return self.driver.page_source
        except NoSuchElementException:
            raise LookupError(
                (
                    "Story elements haven't found: bad timings or page_source "
                    "has changed"
                )
            )
