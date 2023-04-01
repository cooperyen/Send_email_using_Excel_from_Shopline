from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from web_handler.setting import ip


driverURL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/'


class Driver:
    def __init__(self):
        self.service = r'./chromedriver.exe'

    def run(self):
        chromeOptions = Options()
        chromeOptions.add_experimental_option("debuggerAddress", ip)
        chromeService = Service(self.service)
        driver = webdriver.Chrome(service=chromeService, options=chromeOptions)
        return driver
