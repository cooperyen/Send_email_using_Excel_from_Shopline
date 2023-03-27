

import pyperclip as pc
import string
import pyautogui
from excel_xls2xlsx import formatXlsToXLSX
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


def checkStatus(driver):
    time.sleep(1)
    status = elementTarget(driver,
                           '//table//tr/td/div[@ng-class="getLabelClass(job.status)"]', By.XPATH).text

    if (status == '執行完成'):
        elementTarget(driver,
                      '//table//tr/td/div[@ng-click="getResultFiles(job.options.files_s3_url, job.name)"]', By.XPATH).click()
    else:
        print('not yet')
        driver.refresh()
        checkStatus(driver)


def getAllCustomerData(driver):
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

    checkStatus(driver)


# getAllCustomerData(driver)
formatXlsToXLSX()
