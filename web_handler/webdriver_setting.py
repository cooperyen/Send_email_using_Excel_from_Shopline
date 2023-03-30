from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from web_handler.setting import ip


driverURL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/'


def driver():
    chromeOptions = Options()
    chromeOptions.add_experimental_option("debuggerAddress", ip)
    chromeService = Service(r'./chromedriver.exe')
    driver = webdriver.Chrome(service=chromeService, options=chromeOptions)
    return driver
