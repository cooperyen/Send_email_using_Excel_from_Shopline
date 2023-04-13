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
from email_handler.send_email import EMAIL_HANDLER


class AutoEmailingAndDownlaoding:
    # 建構式
    def __init__(self, uiApp, dowloadPath, condition, findOrders, tag, template):
        self.uiApp = uiApp
        self.condition = condition
        self.findOrders = findOrders
        # self.excelData = getExcelData(
        #     condition=condition, findOrders=findOrders)
        self.dowloadPath = dowloadPath
        self.path = 'Downloads'
        self.downloadFilePath = os.path.join(os.path.expanduser("~"), self.path) + '\\'

        self.tag = tag
        self.template = template
        self.longWaitSec = 5
        self.reloadDownlaodPageSec = 20

    # 方法(Method)
    def checkIsDownloaded(self, beforeLength):
        currentLength = len(os.listdir(self.downloadFilePath))
        self.uiApp.returnUiMessage(f'Starting to check whether the download is complete', 'Note')
        self.uiApp.returnUiMessage(f'Current the number of files is : {currentLength}', 'Note')

        if (currentLength > beforeLength):
            self.uiApp.returnUiMessage('download completed. close processing', 'Note')
        else:
            self.uiApp.returnUiMessage(
                f'The download has not completed, check again after {self.longWaitSec} sec.', 'Note')
            waitWithSec(sec=self.longWaitSec)
            self.checkIsDownloaded(beforeLength)

    def checkDownloadIsAvailable(self, driver):
        waitWithSec()
        status = elementTarget(
            driver, '//table//tr/td/div[@ng-class="getLabelClass(job.status)"]', By.XPATH).text
        beforeLength = len(os.listdir(self.downloadFilePath))

        if (status == '執行完成'):
            self.uiApp.returnUiMessage(
                f'Checking the number of files before downloading is {beforeLength}', 'Note')
            elementTarget(
                driver, '//table//tr/td/div[@ng-click="getResultFiles(job.options.files_s3_url, job.name)"]', By.XPATH).click()

            waitWithSec(sec=3)
            self.checkIsDownloaded(beforeLength)

        else:
            self.uiApp.returnUiMessage(
                f'The download button not ready, will refresh page after {self.reloadDownlaodPageSec} sec.', 'Note')
            waitWithSec(sec=self.reloadDownlaodPageSec)
            driver.refresh()
            self.checkDownloadIsAvailable(driver)

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
        excelData = getExcelData(self.uiApp, condition=self.condition, findOrders=self.findOrders)

        for i in excelData:
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

        self.uiApp.returnUiMessage(
            f'Already Export file. will processing download file after {self.longWaitSec} sec.', 'Note')

        # download
        waitWithSec(sec=self.longWaitSec)
        self.uiApp.returnUiMessage('Starting : Download file processing.')
        elementTarget(driver,
                      '//div[@data-e2e-id="sidebar_report_and_analytis_menu"]', By.XPATH).click()
        elementTarget(driver,
                      '//a[@data-e2e-id="sidebar_report_and_analytis_submenu_jobs"]', By.XPATH).click()

        self.checkDownloadIsAvailable(driver)

    def sendingEmails(self, uiApp, saveJsonData):

        excelData = self.excelData()
        
        if(excelData != False):
            for i in excelData:
                name = i[1]
                email = i[3]
                userData = {'name': name,
                            'email': email,
                            'template': self.template,
                            'tag': self.tag,
                            'subject': f'Hi {name}, 清明連假來囉,  準備好好和家人來一場輕旅行了嗎？'
                            }
                email = EMAIL_HANDLER(saveJsonData)
                email.sendtemplateMessage(uiApp, userData)
                i.append(self.tag)

    def excelData(self):
        return getExcelData(self.uiApp, condition=self.condition, findOrders=self.findOrders)    

