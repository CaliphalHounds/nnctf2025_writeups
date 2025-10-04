from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from os import devnull, environ
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class UserSimulator():

    options = Options()
    options.set_capability("pageLoadStrategy","eager")
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--user-agent=CTF/AdminUser')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-translate')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--metrics-recording-only')
    options.add_argument('--no-first-run')
    options.add_argument('--safebrowsing-disable-auto-update')
    options.add_argument('--media-cache-size=1')
    options.add_argument('--disk-cache-size=1')
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"),options=options)


    def init(self):
        try:
            self.driver.get("http://127.0.0.1:5002/")
            user_input = self.driver.find_element(By.ID, "username")
            password_input = self.driver.find_element(By.ID, "password")

            admin_password = environ.get("ADMIN_PASS")
            user_input.send_keys("admin")
            password_input.send_keys(admin_password)

            self.driver.find_element(By.ID, "submitBtn").click()
            print(self.driver.get_cookies())
            print(self.driver.current_url)

        except Exception as e:
            print(e)

    def visit_url(self, user_id):
        try:
            self.driver.get("http://127.0.0.1:5002/support?id={}".format(user_id))
            sleep(int(environ.get("BROWSER_SLEEP")))


        except Exception as e:
            print(e)
