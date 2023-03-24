

import pyperclip as pc
import string
import pyautogui
from web_handler.create_chrome import createChrome
from web_handler.el_func import elementTarget
from web_handler.webdriver_setting import driver, driverURL
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import excel
import time
from datetime import datetime as date


# ** (1). automatically open chrome and login as a user
createChrome()


# ** (2). control (1) and go to admin page
driver = driver()
driver.maximize_window()
time.sleep(2)
driver.get(driverURL)
time.sleep(2)

# export user data
elementTarget(driver,
              '//div[@data-e2e-id="sidebar_customer_management_menu"]', By.XPATH).click()
elementTarget(driver,
              '//a[@data-e2e-id="sidebar_customer_management_submenu_users"]', By.XPATH).click()
elementTarget(driver,
              '//a[@ng-click="showExportPicker()"]', By.XPATH).click()
elementTarget(driver,
              '//div[@class="option-report"]/input[@name="allCustomers"]', By.XPATH).click()
elementTarget(driver,
              '//div/a[@ng-click="onSelectAllFields()"]', By.XPATH).click()
elementTarget(driver,
              '//button[@ng-click="export()"]', By.XPATH).click()

# download
elementTarget(driver,
              '//div[@data-e2e-id="sidebar_report_and_analytis_menu"]', By.XPATH).click()
elementTarget(driver,
              '//a[@data-e2e-id="sidebar_report_and_analytis_submenu_jobs"]', By.XPATH).click()


def checkStatus():
    time.sleep(1)
    status = elementTarget(driver,
                           '//table//tr/td/div[@ng-class="getLabelClass(job.status)"]', By.XPATH).text

    if (status == '執行完成'):
        elementTarget(driver,
                      '//table//tr/td/div[@ng-click="getResultFiles(job.options.files_s3_url, job.name)"]', By.XPATH).click()
    else:
        print('not yet')
        time.sleep(1)
        driver.refresh()
        checkStatus()


checkStatus()


a = str(date.today().date())
out = a.translate(str.maketrans('', '', string.punctuation))

# copying text to clipboard
pc.copy(out+'.xls')

# pasting the text from clipboard
text2 = pc.paste()
time.sleep(2)
for num in text2:
    time.sleep(0.2)
    pyautogui.press(num)

time.sleep(2)
pyautogui.press('enter')

# excel.run()
