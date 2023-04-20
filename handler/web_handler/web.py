from ..functions_handler.base_handler import wait
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class WEB_HANDLER:

    def __init__(self):
        self.proxy = '127.0.0.1'
        self.port = '9527'
        self.ip = f'{self.proxy}:{self.port}'
        self.service = r'./chromedriver.exe'
        self.driverURL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/'

    def createChrome(self, chromePath):
        # chromePath = 'C:/Users/coope/AppData/Local/Google/Chrome/Application/chrome.exe'
        # chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        chromeUserLoginTemporaryData = 'C:/selenium/AutomationProfile'
        cmdCommand = f'"{chromePath}" --remote-debugging-port={self.port} --user-data-dir="{chromeUserLoginTemporaryData}"'
        os.popen(cmdCommand)

    def pathCheckChrome(self, chromePath):
        return os.path.exists(chromePath)

    def elementTarget(self, driver, dom, way):
        wait()
        return driver.find_element(way, dom)

    def driver(self):
        chromeOptions = Options()
        chromeOptions.add_experimental_option("debuggerAddress", self.ip)
        chromeService = Service(self.service)
        driver = webdriver.Chrome(service=chromeService, options=chromeOptions)
        return driver
