import pyperclip as pc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import string
import pyautogui
from web_handler.create_chrome import createChrome
from web_handler.el_func import elementTarget
from web_handler.funcs import waitWithSec
from web_handler.webdriver_setting import Driver, driverURL
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time
from datetime import datetime as date
from excel_handler.xlrdtest import getExcelData, createNewExcelWithData
from email_handler.send_email import send_template_message


# excelData = getExcelData(condition='=', findOrders=1)

# path = 'Downloads'
# fullPath = os.path.join(os.path.expanduser("~"), path) + '\\'


# def checkDownloadIsAvailable(driver):
#     time.sleep(1)
#     status = elementTarget(driver,
#                            '//table//tr/td/div[@ng-class="getLabelClass(job.status)"]', By.XPATH).text
#     length = len(os.listdir(fullPath))
#     print(length)

#     def checkIsDownloaded():
#         checkLength = len(os.listdir(fullPath))
#         print(f'check length {checkLength}')
#         waitWithSec(10)
#         if (checkLength > length):
#             driver.close()
#         else:
#             checkIsDownloaded()

#     if (status == '執行完成'):
#         elementTarget(driver,
#                       '//table//tr/td/div[@ng-click="getResultFiles(job.options.files_s3_url, job.name)"]', By.XPATH).click()

#         checkIsDownloaded()

#     else:
#         print('not yet')
#         driver.refresh()
#         checkDownloadIsAvailable(driver)


# def inputAndSaveTags(tag, driver):
#     createChrome()
#     driver = driver()
#     USERURL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/users/'

#     def inputAndSaveTag():

#         remark = elementTarget(
#             driver, '//textarea[@placeholder="請輸入顧客備註"]', By.XPATH)

#         remark.click()
#         waitWithSec(0.5)
#         remark.send_keys(Keys.CONTROL, 'a')
#         waitWithSec(0.5)
#         remark.send_keys(text)
#         elementTarget(
#             driver, '//div[@ng-if="editAccess()"]/a[@ng-click="save()"]', By.XPATH).click()

#     for i in excelData:
#         driver.get(USERURL+i[0])
#         waitWithSec()

#         try:
#             text = elementTarget(
#                 driver, '//p[@ng-bind-html="user.memo"]', By.XPATH).text + f'.{tag}'

#             elementTarget(
#                 driver, '//a[@ng-click="edit()"]', By.XPATH).click()

#             inputAndSaveTag()

#         except NoSuchElementException:
#             text = tag
#             inputAndSaveTag()

#     driver.close()


# def getAllCustomerData(driver):

#     createChrome()
#     driver = driver()
#     driver.maximize_window()
#     time.sleep(2)
#     driver.get(driverURL)

#     # export user data
#     exportUserData = ['//div[@data-e2e-id="sidebar_customer_management_menu"]',
#                       '//a[@data-e2e-id="sidebar_customer_management_submenu_users"]',
#                       '//a[@ng-click="showExportPicker()"]',
#                       '//div[@class="option-report"]/input[@name="allCustomers"]',
#                       '//div/a[@ng-click="onSelectAllFields()"]',
#                       '//button[@ng-click="export()"]'
#                       ]

#     for i in exportUserData:
#         elementTarget(driver, f'{i}', By.XPATH).click()

#     # download
#     elementTarget(driver,
#                   '//div[@data-e2e-id="sidebar_report_and_analytis_menu"]', By.XPATH).click()
#     elementTarget(driver,
#                   '//a[@data-e2e-id="sidebar_report_and_analytis_submenu_jobs"]', By.XPATH).click()

#     checkDownloadIsAvailable(driver)


# def sendingEmails(tag, template):

#     for i in excelData:
#         name = i[1]
#         email = i[3]
#         userData = {'name': name,
#                     'email': email,
#                     'template': template,
#                     'tag': tag,
#                     'subject': f'好久不見. {name}'
#                     }
#         send_template_message(userData)
#         i.append(tag)


# def run(tag='', template=''):

#     if (template == '' or tag == ''):
#         print('plz enter template name, it\'s coulden\'t be empty')
#         exit()

#     # first step get all user data
#     getAllCustomerData(driver)

#     # Second step. send email
#     sendingEmails(tag, template)

#     # Thrid step. set up each user's remark on shopline
#     inputAndSaveTags(tag, driver)

#     # Fourth step. creat excel at Desketop
#     createNewExcelWithData(excelData, types=tag)


# run(tag='auto_test_230331_1', template='one_order')


# 汽車類別


class AutoEmailingAndDownlaoding:
    # 建構式
    def __init__(self, dowloadPath, condition, findOrders, tag, template):

        self.excelData = getExcelData(
            condition=condition, findOrders=findOrders)
        self.dowloadPath = dowloadPath
        self.path = 'Downloads'
        self.fullPath = os.path.join(os.path.expanduser("~"), self.path) + '\\'

        self.tag = tag
        self.template = template

    # 方法(Method)
    def checkIsDownloaded(self, beforeLength):
        waitWithSec(sec=10)
        currentLength = len(os.listdir(self.fullPath))
        print(f'check current length is {currentLength}')

        if (currentLength > beforeLength):
            print('already downloaded. colsed driver')
        else:
            self.checkIsDownloaded(beforeLength)
            print('download not yet, check it again.')

    def checkDownloadIsAvailable(self, driver):
        waitWithSec()
        status = elementTarget(
            driver, '//table//tr/td/div[@ng-class="getLabelClass(job.status)"]', By.XPATH).text
        beforeLength = len(os.listdir(self.fullPath))
        print(f'check before doucuments length is {beforeLength}')

        if (status == '執行完成'):
            elementTarget(
                driver, '//table//tr/td/div[@ng-click="getResultFiles(job.options.files_s3_url, job.name)"]', By.XPATH).click()

            self.checkIsDownloaded(beforeLength)

        else:
            print('download button not ready, will refresh after 10 sec.')
            waitWithSec(sec=10)
            driver.refresh()
            self.checkDownloadIsAvailable()

    def inputAndSaveTag_remarkController(self, text, driver):

        remark = elementTarget(
            driver, '//textarea[@placeholder="請輸入顧客備註"]', By.XPATH)

        remark.click()
        waitWithSec()
        remark.send_keys(Keys.CONTROL, 'a')
        waitWithSec()
        remark.send_keys(text)
        elementTarget(
            driver, '//div[@ng-if="editAccess()"]/a[@ng-click="save()"]', By.XPATH).click()

    def inputAndSaveTag(self, driver):
        waitWithSec(sec=2)

        USERURL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/users/'

        waitWithSec(sec=3)
        for i in self.excelData:
            driver.get(USERURL+i[0])
            waitWithSec()

            try:
                text = elementTarget(
                    driver, '//p[@ng-bind-html="user.memo"]', By.XPATH).text + f'.{self.tag}'

                elementTarget(
                    driver, '//a[@ng-click="edit()"]', By.XPATH).click()

                self.inputAndSaveTag_remarkController(text)

            except NoSuchElementException:
                text = self.tag
                self.inputAndSaveTag_remarkController(text)

        waitWithSec(sec=2)
        driver.close()

    def getAllCustomerData(self, driver):

        self.createChrome
        waitWithSec(sec=2)
        driver.maximize_window()
        waitWithSec()
        driver.get(driverURL)

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
        waitWithSec(sec=10)
        elementTarget(driver,
                      '//div[@data-e2e-id="sidebar_report_and_analytis_menu"]', By.XPATH).click()
        elementTarget(driver,
                      '//a[@data-e2e-id="sidebar_report_and_analytis_submenu_jobs"]', By.XPATH).click()

        self.checkDownloadIsAvailable()

    def sendingEmails(self):

        for i in self.excelData:
            name = i[1]
            email = i[3]
            userData = {'name': name,
                        'email': email,
                        'template': self.template,
                        'tag': self.tag,
                        'subject': f'Hi {name}, 清明連假來囉,  準備好好和家人來一場輕旅行了嗎？'
                        }
            send_template_message(userData)
            i.append(self.tag)

    def run(self):
        # self.getAllCustomerData()
        # self.sendingEmails()
        waitWithSec()

        # self.inputAndSaveTag()
        # createNewExcelWithData(self.excelData, types=self.tag)


def running(dowloadPath, condition, findOrders, tag, template):
    run = AutoEmailingAndDownlaoding(
        dowloadPath, condition, findOrders, tag, template)

    # createChrome()
    # driver = Driver().run()
    # run.getAllCustomerData()
    run.sendingEmails()
    # driver.close()
    # print(len(run.excelData))
    # createChrome()
    # driver = Driver().run()

    # run.inputAndSaveTag(driver)
    # createNewExcelWithData(run.excelData, types=run.tag)
    # driver.close()


running("blue", '>=', 0, '0401_festival', '0401_festival')
