import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from handler.functions_handler.base_handler import waitWithSec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from handler.excel_handler.excel import EXECL_HANDLER
from handler.web_handler.web import WEB_HANDLER
from handler.email_handler.emil import EMAIL_HANDLER
from handler.functions_handler.json_handler import JASON_HANDLER

class MAIN_HANDLER:
    def __init__(self, uiApp, dowloadPath, condition, findOrders, tag, template):
        self.uiApp = uiApp
        self.condition = condition
        self.findOrders = findOrders
        # self.excelData = getExcelData(
        #     condition=condition, findOrders=findOrders)
        self.dowloadPath = dowloadPath
        self.path = 'Downloads'
        self.downloadFilePath = os.path.join(
            os.path.expanduser("~"), self.path) + '\\'

        self.tag = tag
        self.template = template
        self.longWaitSec = 5
        self.reloadDownlaodPageSec = 20
        self.WEB_HANDLER = WEB_HANDLER()
        self.EXECL_HANDLER = EXECL_HANDLER()

    def checkIsDownloaded(self, beforeLength):
        currentLength = len(os.listdir(self.downloadFilePath))
        self.uiApp.returnUiMessageHandler(
            f'Starting to check whether the download is complete', 'Note')
        self.uiApp.returnUiMessageHandler(
            f'Current the number of files is : {currentLength}', 'Note')

        if (currentLength > beforeLength):
            self.EXECL_HANDLER.xlsToxlsx()
            self.uiApp.returnUiMessageHandler(
                'download completed. close processing', 'Note')
        else:
            self.uiApp.returnUiMessageHandler(
                f'The download has not completed, check again after {self.longWaitSec} sec.', 'Note')
            waitWithSec(sec=self.longWaitSec)
            self.checkIsDownloaded(beforeLength)

    def checkDownloadBtnAvailable(self, driver):
        waitWithSec()
        status = self.WEB_HANDLER.elementTarget(
            driver, '//table//tr/td/div[@ng-class="getLabelClass(job.status)"]', By.XPATH).text
        beforeLength = len(os.listdir(self.downloadFilePath))

        if (status == '執行完成'):
            self.uiApp.returnUiMessageHandler(
                f'Checking the number of files before downloading is {beforeLength}', 'Note')
            self.WEB_HANDLER.elementTarget(
                driver, '//table//tr/td/div[@ng-click="getResultFiles(job.options.files_s3_url, job.name)"]', By.XPATH).click()

            waitWithSec(sec=3)
            self.checkIsDownloaded(beforeLength)

        else:
            self.uiApp.returnUiMessageHandler(
                f'The download button not ready, will refresh page after {self.reloadDownlaodPageSec} sec.', 'Note')
            waitWithSec(sec=self.reloadDownlaodPageSec)
            driver.refresh()
            self.checkDownloadBtnAvailable(driver)

    def inputAndSaveTag_remarkController(self, text, driver):

        remark = self.WEB_HANDLER.elementTarget(
            driver, '//textarea[@placeholder="請輸入顧客備註"]', By.XPATH)

        remark.click()
        waitWithSec()
        remark.send_keys(Keys.CONTROL, 'a')
        waitWithSec()
        remark.send_keys(text)
        self.WEB_HANDLER.elementTarget(
            driver, '//div[@ng-if="editAccess()"]/a[@ng-click="save()"]', By.XPATH).click()

    def inputAndSaveTag(self, driver):
        waitWithSec(sec=2)

        USERURL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/users/'

        waitWithSec(sec=3)
        excelData = getExcelData(
            self.uiApp, condition=self.condition, findOrders=self.findOrders)

        for i in excelData:
            driver.get(USERURL+i[0])
            waitWithSec()

            try:
                text = self.WEB_HANDLER.elementTarget(
                    driver, '//p[@ng-bind-html="user.memo"]', By.XPATH).text + f'.{self.tag}'

                self.WEB_HANDLER.elementTarget(
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
        driver.get(self.WEB_HANDLER.driverURL)

        # export user data
        exportUserData = ['//div[@data-e2e-id="sidebar_customer_management_menu"]',
                          '//a[@data-e2e-id="sidebar_customer_management_submenu_users"]',
                          '//a[@ng-click="showExportPicker()"]',
                          '//div[@class="option-report"]/input[@name="allCustomers"]',
                          '//div/a[@ng-click="onSelectAllFields()"]',
                          '//button[@ng-click="export()"]'
                          ]

        # for i in exportUserData:
        #     self.WEB_HANDLER.elementTarget(driver, f'{i}', By.XPATH).click()

        self.uiApp.returnUiMessageHandler(
            f'Already Export file. will processing download file after {self.longWaitSec} sec.', 'Note')

        # download
        waitWithSec(sec=self.longWaitSec)
        self.uiApp.returnUiMessageHandler('Starting : Download file processing.')
        self.WEB_HANDLER.elementTarget(driver,
                                       '//div[@data-e2e-id="sidebar_report_and_analytis_menu"]', By.XPATH).click()
        self.WEB_HANDLER.elementTarget(driver,
                                       '//a[@data-e2e-id="sidebar_report_and_analytis_submenu_jobs"]', By.XPATH).click()

        self.checkDownloadBtnAvailable(driver)
    
    def exportXlsxData(self):
        return self.EXECL_HANDLER.exportXlsxData(self.uiApp, condition=self.condition, findOrders=self.findOrders)
