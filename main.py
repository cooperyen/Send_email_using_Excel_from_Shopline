

import pyperclip as pc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import string
import pyautogui
from web_handler.create_chrome import createChrome
from web_handler.el_func import elementTarget
from web_handler.funcs import waitWithSec
from web_handler.webdriver_setting import driver, driverURL
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import excel
import time
from datetime import datetime as date
from xlrdtest import getExcelData, createNewExcelWithData
from email_handler.send_email import send_template_message

# # ** (1). automatically open chrome and login as a user
# createChrome()


# # ** (2). control (1) and go to admin page
driver = driver()
# driver.maximize_window()
# time.sleep(2)
# driver.get(driverURL)
# time.sleep(2)


excelData = getExcelData(condition='=', findOrders=1)
tag = 'only_one_order_230330'


def checkDownloadIsAvailable(driver):
    time.sleep(1)
    status = elementTarget(driver,
                           '//table//tr/td/div[@ng-class="getLabelClass(job.status)"]', By.XPATH).text

    if (status == '執行完成'):
        elementTarget(driver,
                      '//table//tr/td/div[@ng-click="getResultFiles(job.options.files_s3_url, job.name)"]', By.XPATH).click()
    else:
        print('not yet')
        driver.refresh()
        checkDownloadIsAvailable(driver)


def inputAndSaveTags(tag):
    USERURL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/users/'

    def inputAndSaveTag():

        remark = elementTarget(
            driver, '//textarea[@placeholder="請輸入顧客備註"]', By.XPATH)

        remark.click()
        waitWithSec(0.5)
        remark.send_keys(Keys.CONTROL, 'a')
        waitWithSec(0.5)
        remark.send_keys(text)
        elementTarget(
            driver, '//div[@ng-if="editAccess()"]/a[@ng-click="save()"]', By.XPATH).click()

    for i in excelData:
        driver.get(USERURL+i[0])
        waitWithSec()
        text = elementTarget(
            driver, '//p[@ng-bind-html="user.memo"]', By.XPATH).text + f'.{tag}'
        try:
            elementTarget(
                driver, '//a[@ng-click="edit()"]', By.XPATH).click()

            inputAndSaveTag()

        except NoSuchElementException:
            inputAndSaveTag()


def getAllCustomerData(driver):
    # export user data
    exportUserData = ['//div[@data-e2e-id="sidebar_customer_management_menu"]',
                      '//a[@data-e2e-id="sidebar_customer_management_submenu_users"]',
                      '//a[@ng-click="showExportPicker()"]',
                      '//div[@class="option-report"]/input[@name="allCustomers"]',
                      '//div/a[@ng-click="onSelectAllFields()"]',
                      '//button[@ng-click="export()"]'
                      ]

    for i in exportUserData:
        elementTarget(driver, f'{i}', By.XPATH).click()

        # download
        elementTarget(driver,
                      '//div[@data-e2e-id="sidebar_report_and_analytis_menu"]', By.XPATH).click()
        elementTarget(driver,
                      '//a[@data-e2e-id="sidebar_report_and_analytis_submenu_jobs"]', By.XPATH).click()

    checkDownloadIsAvailable(driver)


def sendingEmails():

    for i in excelData:
        name = i[1]
        email = i[3]
        userData = {'name': name,
                    'email': email,
                    'template': 'test',
                    'tag': tag,
                    'subject': f'subjectsubject {name}'
                    }
        send_template_message(userData)
        i.append(tag)


# # first step get all user data
# getAllCustomerData(driver)

# # Second step. send email
# sendingEmails()

# # Thrid step. set up remark
# inputAndSaveTags(tag)

# # Fourth step. creat excel
# createNewExcelWithData(excelData, types=tag)
