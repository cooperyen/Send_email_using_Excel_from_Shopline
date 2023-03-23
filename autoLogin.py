import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# default setting.
#
proxy = '127.0.0.1'
port = '9527'
ip = f'{proxy}:{port}'


# cmd setting.
#
# ** (A). automatically open chrome and login as a user
def createChrome():
    chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    chromeUserLoginTemporaryData = 'C:/selenium/AutomationProfile'
    cmdCommand = f'"{chromePath}" --remote-debugging-port={port} --user-data-dir="{chromeUserLoginTemporaryData}"'
    os.popen(cmdCommand)


createChrome()

# webdriver handler
#
# ** control (A) and go to admin page
chromeOptions = Options()
chromeOptions.add_experimental_option("debuggerAddress", ip)
chromeService = Service(r'./chromedriver.exe')
driver = webdriver.Chrome(service=chromeService, options=chromeOptions)
URL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/'
driver.get(URL)

a = driver.find_element(
    By.XPATH, '//div[@data-e2e-id="sidebar_customer_management_menu"]')

print(a.text)
input()
