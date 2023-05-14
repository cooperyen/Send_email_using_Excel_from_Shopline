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


"""
1. Combine each handlers in class MERGE_HANDLER.
2. make handler router for export.
"""
class MERGE_HANDLER:
    def __init__(self, ary = {
        'uiApp':None,
        'dowloadPath':None,
        'condition':None,
        'findOrders':None,
        'tag':None,
        'template':None
        }):

        self.uiApp = ary['uiApp']
        self.condition = ary['condition']
        self.findOrders = ary['findOrders']
        self.dowloadPath = ary['dowloadPath']
        self.path = 'Downloads'
        self.downloadFilePath = os.path.join(
            os.path.expanduser("~"), self.path) + '\\'

        self.tag = ary['tag']
        self.template = ary['template']
        self.longWaitSec = 5
        self.reloadDownlaodPageSec = 20
        self.WEB_HANDLER = WEB_HANDLER()
        self.EXECL_HANDLER = EXECL_HANDLER()

        
    """
    check the download button is ready on the page.
    """
    def checkDownloadBtnAvailable(self, driver):
        waitWithSec()

        statesOfdownloadBTN = self.WEB_HANDLER.elementTarget(
            driver, '//table//tr/td/div[@ng-class="getLabelClass(job.status)"]', By.XPATH).text
        
        # number of current files before check is downloaded.
        beforeLength = len(os.listdir(self.downloadFilePath))

        # states: 執行完成, 處理中
        if (statesOfdownloadBTN == '執行完成'):
            self.uiApp.displayUiMessageHandler(
                f'Checking the number of files before downloading is {beforeLength}', 'Note')
            
            self.WEB_HANDLER.elementTarget(
                driver, '//table//tr/td/div[@ng-click="getResultFiles(job.options.files_s3_url, job.name)"]', By.XPATH).click()

            waitWithSec(sec=3)

            self.checkIsDownloaded(beforeLength)

        else:
            self.uiApp.displayUiMessageHandler(
                f'The download button not ready, will refresh page after {self.reloadDownlaodPageSec} sec.', 'Note')
            
            waitWithSec(sec=self.reloadDownlaodPageSec)
            
            # refresh web page. 
            driver.refresh()

            # do check again.
            self.checkDownloadBtnAvailable(driver)


    """
    check the file is downloaded.
    """
    def checkIsDownloaded(self, beforeLength):

        # number of current files.
        currentLength = len(os.listdir(self.downloadFilePath))

        self.uiApp.displayUiMessageHandler(
            f'Starting to check whether the download is complete', 'Note')
        self.uiApp.displayUiMessageHandler(
            f'Current the number of files is : {currentLength}', 'Note')

        # check if the current file count is higher than before or not.
        if (currentLength > beforeLength):

            self.EXECL_HANDLER.xlsToXlsx()

            self.uiApp.displayUiMessageHandler(
                'download completed. close processing', 'Note')
            
        else:
            self.uiApp.displayUiMessageHandler(
                f'The download has not completed, check again after {self.longWaitSec} sec.', 'Note')
            waitWithSec(sec=self.longWaitSec)
            # do check again.
            self.checkIsDownloaded(beforeLength)

    
    # def inputAndSaveTag_remarkController(self, text, driver):

    #     remark = self.WEB_HANDLER.elementTarget(
    #         driver, '//textarea[@placeholder="請輸入顧客備註"]', By.XPATH)

    #     remark.click()
    #     waitWithSec()
    #     remark.send_keys(Keys.CONTROL, 'a')
    #     waitWithSec()
    #     remark.send_keys(text)
    #     self.WEB_HANDLER.elementTarget(
    #         driver, '//div[@ng-if="editAccess()"]/a[@ng-click="save()"]', By.XPATH).click()

    # def inputAndSaveTag(self, driver):
    #     waitWithSec(sec=2)

    #     USERURL = 'https://admin.shoplineapp.com/admin/rafagogorafa154/users/'

    #     waitWithSec(sec=3)
    #     excelData = getExcelData(
    #         self.uiApp, condition=self.condition, findOrders=self.findOrders)

    #     for i in excelData:
    #         driver.get(USERURL+i[0])
    #         waitWithSec()

    #         try:
    #             text = self.WEB_HANDLER.elementTarget(
    #                 driver, '//p[@ng-bind-html="user.memo"]', By.XPATH).text + f'.{self.tag}'

    #             self.WEB_HANDLER.elementTarget(
    #                 driver, '//a[@ng-click="edit()"]', By.XPATH).click()

    #             self.inputAndSaveTag_remarkController(text)

    #         except NoSuchElementException:
    #             text = self.tag
    #             self.inputAndSaveTag_remarkController(text)

    #     waitWithSec(sec=2)
    #     driver.close()


    def getAllCustomerData(self, driver):

        # maximize the browser window.
        driver.maximize_window()

        waitWithSec()

        # get to shopline admin page.
        driver.get(self.WEB_HANDLER.driverURL)

        # export user data click steps.
        exportUserData = [
            '//div[@data-e2e-id="sidebar_customer_management_menu"]',
            '//a[@data-e2e-id="sidebar_customer_management_submenu_users"]',
            '//a[@ng-click="showExportPicker()"]',
            '//div[@class="option-report"]/input[@name="allCustomers"]',
            '//div/a[@ng-click="onSelectAllFields()"]',
            '//button[@ng-click="export()"]'
            ]

        for i in exportUserData:
            self.WEB_HANDLER.elementTarget(driver, f'{i}', By.XPATH).click()

        self.uiApp.displayUiMessageHandler(
            f'Already Export file. will processing download file after {self.longWaitSec} sec.', 'Note')

        # download setp
        waitWithSec(sec=self.longWaitSec)
        self.uiApp.displayUiMessageHandler('Starting : Download file processing.')

        # download user data click steps.
        self.WEB_HANDLER.elementTarget(driver, '//div[@data-e2e-id="sidebar_report_and_analytis_menu"]', By.XPATH).click()
        self.WEB_HANDLER.elementTarget(driver, '//a[@data-e2e-id="sidebar_report_and_analytis_submenu_jobs"]', By.XPATH).click()

        self.checkDownloadBtnAvailable(driver)
    

    def exportXlsxData(self):
        return self.EXECL_HANDLER.exportXlsxData(self.uiApp, condition=self.condition, findOrders=self.findOrders)
