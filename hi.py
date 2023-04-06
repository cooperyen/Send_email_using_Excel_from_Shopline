import tkinter as tk
from main import AutoEmailingAndDownlaoding
from web_handler.create_chrome import createChrome
from web_handler.webdriver_setting import Driver, driverURL
import json
import os


def running(downloadPath, condition, findOrders, tag, template):

    if (condition == '' or findOrders == ''):
        print('Condition or Find orders can\'t be empty')

    else:
        run = AutoEmailingAndDownlaoding(
            downloadPath, condition, findOrders, tag, template)

        # setting chrome
        print('Starting : Open chrome porcessing')
        createChrome(downloadPath)
        driver = Driver().run()
        print('Done : Open chrome porcessing')

        # print('Starting : Get all customer data porcessing')
        # run.getAllCustomerData(driver)
        # print('Done : Get all customer data porcessing')

        # print('Starting : Send emails.')
        # run.sendingEmails()
        # print('Done : Send emails.')
        # driver.close()
        # print(len(run.excelData))
        # createChrome()
        # driver = Driver().run()

        # run.inputAndSaveTag(driver)
        # createNewExcelWithData(run.excelData, types=run.tag)
        # driver.close()


# if En.get() == '1' and En1.get() == '1':  # 用get獲得帳密去判斷能不能登入
#     l = tk.Label(root1, text='Login successful！', bg="#7AFEC6", fg='#FFD306',
#                  font=("Viner Hand ITC", 15, "bold"), anchor='c', width=50, height=10)
#     l.pack()
#     # running("blue", '=', 0, '0401_festival', '0401_festival')
# else:
#     l = tk.Label(root1, text='Login Error！', bg="#7AFEC6", fg='#CE0000',
#                  font=("Viner Hand ITC", 15, "bold"), width=50, height=10, anchor='c')
#     l.pack()

# {downloadPath, condition, findOrders, tag, template}


class tks:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x600+100+100")
        self.root.resizable(0, 0)
        self.root.title('S')
        # self.root.configure(bg="#7AFEC6")
        # self.root.iconbitmap('heart_green.ico')
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)

        self.downloadPath = tk.Entry(self.root, width=70, bg="#7AFEC6")
        self.condition = tk.Entry(self.root, width=70)
        self.findOrders = tk.Entry(self.root, width=70)
        self.tag = tk.Entry(self.root, width=70)
        self.template = tk.Entry(self.root, width=70)
        self.top_frame = tk.Frame(self.root, bg='cyan',
                                  width=450, height=50, pady=3)
        self.center = tk.Frame(self.root, bg='gray2', width=50,
                               height=40, padx=3, pady=3)

        self.datas = {
            'downloadPath': {
                'en': 'Browser download path',
                'ch': '瀏覽器下載路徑',
            },
            'condition': {
                'en': 'Condition',
                'ch': '匹配條件',
            },
            'findOrders': {
                'en': 'Find orders',
                'ch': '匹配訂單數',
            },
            'tag': {
                'en': 'Tag Name',
                'ch': '標籤名稱',
            },
            'template': {
                'en': 'Template Name',
                'ch': '套版名稱',
            },
        }
        self.labelsss = ''
        self.datassfsf = {}
        self.JSON_FILE = 'setting.json'

    def labelSetting(self, text):
        return tk.Label(self.root, text=text, width=25,
                        font=("Algerian", 14, "bold"), anchor='c')

    def writeJsonFile(self, data):
        with open(self.JSON_FILE, 'w') as json_file:
            json.dump(data, json_file)

        json_file.close()

    def sending(self):
        with open(self.JSON_FILE, 'r') as json_file:
            saveJsonData = json.load(json_file)

        running(saveJsonData['downloadPath']['value'], saveJsonData['condition']['value'],
                saveJsonData['findOrders']['value'], saveJsonData['tag']['value'], saveJsonData['template']['value'])

    def dataOptions(self):

        if (os.path.exists(self.JSON_FILE) == False):
            self.writeJsonFile(self.datas)

        with open(self.JSON_FILE, 'r') as json_file:
            saveJsonData = json.load(json_file)

        def Info():
            inputDatas = self.datas
            inputDatas['downloadPath']['value'] = self.downloadPath.get()
            inputDatas['condition']['value'] = self.condition.get()
            inputDatas['findOrders']['value'] = self.findOrders.get()
            inputDatas['tag']['value'] = self.tag.get()
            inputDatas['template']['value'] = self.template.get()
            self.writeJsonFile(inputDatas)
            self.sending()

        def returnValues(saveJsonData, item):
            result = saveJsonData[item]['value'] if 'value' in saveJsonData[item] else 'x'
            print(result)
            return result

        inputList = {'downloadPath': self.downloadPath,
                     'condition': self.condition,
                     'findOrders': self.findOrders,
                     'tag': self.tag,
                     'template': self.template}

        num = 0
        for labels in self.datas:
            self.labelSetting(self.datas[labels]['en']).grid(row=num)
            inputList[labels].insert(0, returnValues(saveJsonData, labels))
            inputList[labels].grid(row=num, column=1, columnspan=2)
            num = num + 1

        b = tk.Button(self.root, text='cancel', anchor='c', width=6, height=1,
                      command=self.root.quit, justify="right")  # quit可以讓pyhon shell結束
        b.grid(row=len(self.datas), column=0)

        b1 = tk.Button(self.root, text='save&run', relief="flat", bg='#4da35a', fg='#ffffff',
                       anchor='w', height=1, command=Info)

        b1.grid(row=len(self.datas), column=1)

    def run(self):
        self.dataOptions()
        self.root.mainloop()


run = tks()
run.run()
