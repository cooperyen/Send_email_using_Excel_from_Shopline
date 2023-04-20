import customtkinter
from handler.main import MAIN_HANDLER, EXECL_HANDLER,WEB_HANDLER, EMAIL_HANDLER, JASON_HANDLER
import os
import time
import re
# from handler.excel_handler.excel import EXECL_HANDLER
# from handler.web_handler.web import WEB_HANDLER
# from handler.email_handler.emil import EMAIL_HANDLER
# from handler.functions_handler.json_handler import JASON_HANDLER, saveJsonFileName


warningColor = '#D05B5B'
lightBTN = '#54d68e'
darkBTN = '#319960'
mainBgColor = '#2a734b'
mainHoverColor = '#357a54'
secBgColor = '#1e5738'
optionBTNColor = '#124529'

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
# customtkinter.set_default_color_theme('blue')


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configure window.
        self.displayWidth = self.winfo_screenwidth()  # <-- Width of the screen
        self.displayHeight = self.winfo_screenheight() # <-- Height of the screen
        self.width = 400
        self.height = 300
        self.x = (self.displayWidth/2) - (self.width/2)
        self.y = (self.displayHeight/2) - (self.height/2)
        self.title("All for one")
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.minsize(self.width, self.height)
        self.resizable(False, False)

        self.label = customtkinter.CTkLabel(self, text="direct send email")
        self.label.pack(padx=20, pady=20)
        # self.protocol("WM_DELETE_WINDOW", self.closed) # <-- adding the protocol

        self.entry = customtkinter.CTkEntry(master=self, placeholder_text="email", width=300)
        self.entry.pack(padx=20, pady=0 )

        self.entryInfo = customtkinter.CTkLabel(master=self, text="If testing multiple emails at the same time, use ' , ' to \nconnect emails.", justify="left", width=500)
        self.entryInfo.pack(pady=5)

        self.entryWarning = customtkinter.CTkLabel(master=self, text="", text_color=warningColor, font=customtkinter.CTkFont(weight="bold"))
        self.entryWarning.pack(padx=20, pady=20)

        self.btn = customtkinter.CTkButton(self, command=self.email)
        self.btn.pack(padx=20, pady=10)
        self.btn.configure(text='SEND')
        self.parentModule = ''

    def closed(self):
        self.destroy()

    def email(self):
        entry = self.entry.get()
        self.entryWarning.configure(text='')
        if(entry != ''):
            entrySplit = entry.split(',')
            includeAtSymbol = True
            emails = []
            
            for i in entrySplit:
                includeAtSymbol = '@' in i 

            if(includeAtSymbol):
                # remove any spaces
                for i in entrySplit:
                    emails.append(i.replace(' ',''))
                xs = self.parentModule.directSendEmailFunc(emails)
                  
            else:
                self.entryWarning.configure(text='must be include "@"')
        
        else:
            self.entryWarning.configure(text='emails can\'t not be empty')

    def getParentModule(self, module):
        self.parentModule = module



class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.EXECL_HANDLER = EXECL_HANDLER()
        self.JASON_HANDLER = JASON_HANDLER()
        # configure window.
        self.displayWidth = self.winfo_screenwidth()  # Width of the screen
        self.displayHeight = self.winfo_screenheight() # Height of the screen
        self.width = 1400
        self.height = 800
        self.x = (self.displayWidth/2) - (self.width/2)
        self.y = (self.displayHeight/2) - (self.height/2)
        self.title("All for one")
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.minsize(self.width, self.height)
        self.appTitle = 'ALL FOR ONE.'
        # self.resizable(False, False)

        # configure grid layout (4x4).
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.font = customtkinter.CTkFont(family='Microsoft JhengHei')
        self.WEB_HANDLER = WEB_HANDLER()

        self.datas = {
            'target': {
                'condition': {
                    'en': 'Condition',
                    'ch': '匹配條件',
                    'info': '',
                    'value': ''
                },
                'findOrders': {
                    'en': 'Find orders',
                    'ch': '匹配訂單數',
                    'info': '',
                    'value': ''
                },
                'tag': {
                    'en': 'Tag Name',
                    'ch': '標籤名稱',
                    'info': '',
                    'value': ''
                },
                'subject': {
                    'en': 'Mail subject',
                    'ch': '郵件主旨',
                    'info': 'enter {name} display user name.eg. "Hi {name}, how are you?"',
                    'value': ''
                },
                'template': {
                    'en': 'Template Name',
                    'ch': '套版名稱',
                    'info': '套版名稱',
                    'value': ''
                },
            },
            'setting': {
                'chromePath': {
                    'en': 'Chrome path',
                    'ch': 'Chrome 路徑',
                    'info': 'C:/Program Files/Google/Chrome/Application/chrome.exe',
                    'value': ''
                }
            },
            'mailgun': {
                'sender': {
                    'en': 'sender',
                    'ch': '寄件人',
                    'info': 'RafaGo Rafa牽著吉娃娃',
                    'value': ''
                },
                'senderEmail': {
                    'en': 'sender email',
                    'ch': '寄件人郵箱',
                    'info': 'service.rafago@gmail.com',
                    'value': ''
                },
                'apiKey': {
                    'en': 'api key',
                    'ch': 'api key',
                    'info': 'key-7317a30a70357cf6309ab4fead46637d',
                    'value': ''
                },
                'domain': {
                    'en': 'domain',
                    'ch': 'domain',
                    'info': 'rafagotest.a2hosted.com',
                    'value': ''
                },
            },
            'title': {
                'target': {
                    'en': 'Send target',
                    'ch': '發送目標',
                },
                'setting': {
                    'en': 'Setting options',
                    'ch': '基本設定',
                },
                'mailgun': {
                    'en': 'Mailgun setting options',
                    'ch': 'Mailgun 設定',
                },
            },
        }

        # toplevel_window
        self.toplevel_window = None
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text=self.appTitle, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=[
            "Dark", "System", "Light"],
            command=self.changeAppearanceModeHandler,
            fg_color=secBgColor,
            button_color=optionBTNColor,
            button_hover_color=optionBTNColor
            )

        self.appearance_mode_optionemenu.grid(
            row=9, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")

        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, 
            values=["100%", "110%", "120%"], 
            command=self.changeScalingHandler,
            fg_color=secBgColor,
            button_color=optionBTNColor,
            button_hover_color=optionBTNColor
            )
        
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(
            self, width=250, height=250, state='disabled')
        self.textbox.grid(row=0, column=1, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        # configure color tag.
        self.textbox.tag_config("Warning", foreground=warningColor)
        self.textbox.tag_config("Note", foreground="#B88347")
        self.textbox.tag_config("time", foreground="#8B8B8B")
        self.tabName_email = 'target'
        self.tabName_setting = 'setting'
        self.tabName_mailgun = 'mailgun'

        self.mainButtons()
        self.settingOptionAreaContent()

    def mainButtons(self):
        ary = [
            {
                'command': self.saveSettingOptionToFileBTN,
                'text': 'save setting options'
            },
            {
                'command': self.downloadUserDataBTN,
                'text': 'download user data'
            },
            {
                'command': self.sendEmailBTN,
                'text': 'send email'
            },
            {
                'command': self.saveToExcelBTN,
                'text': 'save user data to excel'
            },
            {
                'command': self.fullProcessBTN,
                'text': 'Do all of the above'
            },
            # {
            #     'command': self.directSendEmailBTN,
            #     'text': 'Send test email'
            # }
        ]

        for i in range(len(ary)):
            locals()[i] = customtkinter.CTkButton(
                self.sidebar_frame, command=ary[i]['command'], fg_color=mainBgColor, hover_color=mainHoverColor)
            locals()[i].configure(text=ary[i]['text'])
            locals()[i].grid(row=i+1, column=0, padx=20, pady=10)

        directSendEmailBTN = customtkinter.CTkButton(self.sidebar_frame, command=self.directSendEmailBTN, fg_color='transparent', hover_color=mainHoverColor, border_color=mainHoverColor, border_width=2)
        directSendEmailBTN.configure(text='Send test email', height=50)
        directSendEmailBTN.grid(row=7, column=0, padx=20, pady=10)

    def settingOptionAreaContent(self):
        self.tabview = customtkinter.CTkTabview(self, width=250, segmented_button_selected_color='white', text_color='black',segmented_button_selected_hover_color='white')
        self.tabview.grid(row=1, column=1, padx=(
            20, 20), pady=(0, 0), sticky="nsew")
        self.tabview.add(self.tabName_email)
        self.tabview.add(self.tabName_setting)
        self.tabview.add(self.tabName_mailgun)

        tableView_tab_1 = self.tabview.tab(self.tabName_email)
        # tableView_tab_1.configure(fg_color=tagColor)  # configure grid of individual tabs
        tableView_tab_2 = self.tabview.tab(self.tabName_setting)
        tableView_tab_3 = self.tabview.tab(self.tabName_mailgun)

        if (os.path.exists(self.JASON_HANDLER.saveJsonFileName) == False):
            # self.writeJsonFile(self.datas)
            self.JASON_HANDLER.writeJsonFile(self.datas)

        loadJsonData = self.JASON_HANDLER.loadJasonFile()

        def emailOption(tableView, tagName):
            mainRowNum = 1
            infoRowNum = 2

            # Title
            customtkinter.CTkLabel(
                tableView, text=self.datas['title'][tagName]['en'], font=customtkinter.CTkFont(size=16, weight="bold")).grid(
                    row=0, column=0, padx=20, pady=(20, 5), sticky='w')

            for labels in self.datas[tagName]:
                # items label
                customtkinter.CTkLabel(
                    tableView, text=f"{self.datas[tagName][labels]['en']}", anchor="w", font=self.font).grid(
                    row=1 if mainRowNum == 1 else mainRowNum, column=0, padx=20, pady=(0, 0), sticky='w')

                # informations label
                customtkinter.CTkLabel(
                    tableView, text=f"{self.datas[tagName][labels]['info']}", anchor="w", font=self.font).grid(row=infoRowNum, column=1, sticky='w')

                globals()[f'__ui_labelsData_{labels}'] = customtkinter.CTkEntry(tableView, width=400, font=self.font)

                if (labels == 'condition'):
                    globals()[f'__ui_labelsData_{labels}'] = customtkinter.CTkOptionMenu(
                        master=tableView,
                        values=['>', '<', '=', '>=', '<='],
                        fg_color=secBgColor,
                        button_color=optionBTNColor,
                        button_hover_color=optionBTNColor
                        )
                    
                    globals()[f'__ui_labelsData_{labels}'].set(loadJsonData[tagName][labels]['value'])
                    globals()[f'__ui_labelsData_{labels}'].grid(row=1, column=1, pady=(10, 0), sticky='w')
                else:
                    globals()[f'__ui_labelsData_{labels}'].grid(row=mainRowNum, column=1, pady=(10, 0))
                    globals()[f'__ui_labelsData_{labels}'].insert(0, loadJsonData[tagName][labels]['value'])

                infoRowNum = infoRowNum + 2
                mainRowNum = mainRowNum + 2

        emailOption(tableView_tab_1, self.tabName_email)
        emailOption(tableView_tab_2, self.tabName_setting)
        emailOption(tableView_tab_3, self.tabName_mailgun)

    def changeAppearanceModeHandler(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def changeScalingHandler(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    # show message in self.textbox
    def returnUiMessageHandler(self, value, tag=''):
        text = tag + ' : ' if tag != '' else ''
        self.textbox.configure(state='normal')
        self.textbox.insert("0.0", f'\n{text}{value}\n\n', tag)
        self.textbox.insert(
            "0.0", f'{time.strftime("%m/%d %H:%M:%S", time.localtime())}', 'time')
        self.textbox.configure(state='disabled')
        self.textbox.update()
        print(value)

    # BTN funs.
    def fullProcessBTN(self):
        saveSettingOptionToFile = self.saveSettingOptionToFileFunc()

        if (saveSettingOptionToFile):
            loadJsonData = self.JASON_HANDLER.loadJasonFile()
            run = self.runSetting()

            # opean chrome
            self.downloadUserDataFunc()

            self.saveToExcelFunc() if self.sendEmailFunc() else None

    # send test mail.
    #
    def directSendEmailBTN(self):

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.grab_set() 
        else:
            self.toplevel_window.focus()  # if window exists focus it

        self.toplevel_window.getParentModule(self)
        
          
    # send email handler
    #

    def sendEmailBTN(self):
        sendEmail = self.sendEmailFunc()

        if (sendEmail):
            self.saveToExcelBTN()

    def sendEmailFunc(self):
        saveSettingOptionToFile = self.saveSettingOptionToFileFunc()

        if (saveSettingOptionToFile):
            msg = 'sending Emails processing.'
            self.returnUiMessageHandler(f'Starting : {msg}')

            loadJsonData = self.JASON_HANDLER.loadJasonFile()

            run = self.runSetting()
            emailH = EMAIL_HANDLER(self, loadJsonData, run.exportXlsxData())
            sendingEmails = emailH.sendingEmails()
            # sendingEmails = run.sendingEmails(self, loadJsonData)

            if(run.exportXlsxData() and sendingEmails['state']):
                self.returnUiMessageHandler(f'A total of {len(run.exportXlsxData())} emails were sent')
                self.returnUiMessageHandler(f'Done : {msg}')

            return sendingEmails['state']
        else:
            return False

    def directSendEmailFunc(self, email):
        saveSettingOptionToFile = self.saveSettingOptionToFileFunc()

        if (saveSettingOptionToFile):
            msg = 'direct sending Email processing.'
            self.returnUiMessageHandler(f'Starting : {msg}')

            loadJsonData = self.JASON_HANDLER.loadJasonFile()
            run = self.runSetting()
            emailH = EMAIL_HANDLER(self, loadJsonData, run.exportXlsxData())
            sendingEmails = emailH.directSendEmails(email)

            if(sendingEmails['state']):
                self.returnUiMessageHandler(f'Done : {msg}')
                self.returnUiMessageHandler(f'A total of {sendingEmails["num"]} emails were sent') 

            return sendingEmails['num']
        else:
            return False


    # save GUI options to file handler
    #

    def saveSettingOptionToFileBTN(self):
        saveSetting = self.saveSettingOptionToFileFunc()
        if (saveSetting):
            self.returnUiMessageHandler('Setting options saved.')

    def saveSettingOptionToFileFunc(self):

        def checkSettingAllTrue(ary):
            array = []
            for i in range(len(ary)):
                array.append(ary[i]['bool'])
            return all(array)

        def checkSettingOptionNotEmpty():
            array = []
            for labels in self.datas[self.tabName_email]:
                array.append(self.datas[self.tabName_email][labels]['value'])

            return all(array)

        # append setting option value.
        ary = [self.tabName_email, self.tabName_setting, self.tabName_mailgun]
        for tab in ary:
            for labels in self.datas[tab]:
                self.datas[tab][labels]['value'] = globals(
                )[f'__ui_labelsData_{labels}'].get()

        # verify 'findOrders' is integer or not.
        try:
            int(self.datas[self.tabName_email]['findOrders']['value'])
            findOrdersBool = True
        except:
            findOrdersBool = False

        # verify and Warning setting options.
        verifySettingList = [
            {
                'title': 'settingOption',
                'text': 'Setting options can\'t not be empty, please try again.',
                'bool': checkSettingOptionNotEmpty()
            },
            {
                'title': 'tag',
                'text': 'Tag have symbols, please remove and try again.',
                'bool': True if re.search(r"\W", self.datas[self.tabName_email]['tag']['value']) == None else False
            },
            {
                'title': 'findOrders',
                'text': '"Find orders" is not type of integer, make sure only input numbers without any character and symbols that try again.',
                'bool': findOrdersBool
            },
            {
                'title': 'chromePath',
                'text': f'Chrome path not found, please check "{self.tabName_setting}" and try again.',
                'bool': self.WEB_HANDLER.pathCheckChrome(self.datas[self.tabName_setting]['chromePath']['value'])
            },
            {
                'title': 'sender',
                'text': f'Sender can\'t not be empty, please check "{self.tabName_mailgun}" and try again.',
                'bool': True if self.datas[self.tabName_mailgun]['sender']['value'] != '' else False
            },
            {
                'title': 'senderEmail',
                'text': f'Sender\'s email have to include "@" and without any space. please check "{self.tabName_mailgun}" and try again.',
                'bool': '@' in self.datas[self.tabName_mailgun]['senderEmail']['value'] and ' ' not in self.datas[self.tabName_mailgun]['senderEmail']['value']
            },
            {
                'title': 'apiKey',
                'text': f'Apikey should start with "key-", please check "{self.tabName_mailgun}" and try again.',
                'bool': self.datas[self.tabName_mailgun]['apiKey']['value'].startswith('key-')
            },
            {
                'title': 'domain',
                'text': f'Domain can\'t not be empty, please check "{self.tabName_mailgun}" and try again.',
                'bool': True if self.datas[self.tabName_mailgun]['domain']['value'] != '' else False
            },
        ]

        # Verifies that each option Boolean and displays a Warning message if FALSE.
        for i in range(len(verifySettingList)):
            if (verifySettingList[i]['bool'] == False):
                self.returnUiMessageHandler(verifySettingList[i]['text'], 'Warning')
                break

        # if all options are True that save data to json.
        if (checkSettingAllTrue(verifySettingList)):
            self.JASON_HANDLER.writeJsonFile(self.datas)
            return True

    # download users data handler
    #

    def downloadUserDataBTN(self):
        self.downloadUserDataFunc()

    def downloadUserDataFunc(self):

        saveSettingOptionToFile = self.saveSettingOptionToFileFunc()

        if (saveSettingOptionToFile):
            loadJsonData = self.JASON_HANDLER.loadJasonFile()
            run = self.runSetting()

            # start
            self.returnUiMessageHandler(
                'starting process, please do not control you\'re computer before finish process.', 'Note')
            self.returnUiMessageHandler(
                'starting process, please do not control you\'re computer before finish process.', 'Note')

            # opean chrome
            self.returnUiMessageHandler('Starting : Open chrome processing.')

            self.WEB_HANDLER.createChrome(
                loadJsonData[self.tabName_setting]['chromePath']['value'])

            driver = self.WEB_HANDLER.driver()
            self.returnUiMessageHandler('Done : Open chrome processing.')

            # get and download user data from shopline
            self.returnUiMessageHandler(
                'Starting : Get all customer data processing.')
            run.getAllCustomerData(driver)
            self.returnUiMessageHandler('Done : Get all customer data processing.')

            driver.close()

    # save to Excel handler
    #

    def saveToExcelBTN(self):
        self.saveToExcelFunc()

    def saveToExcelFunc(self):
        msg = 'saving user\'s data to excel.'
        self.returnUiMessageHandler(f'Starting : {msg}')
        run = self.runSetting()
        self.EXECL_HANDLER.createNewExcelWithData(self, run.exportXlsxData(), types=run.tag)
        self.returnUiMessageHandler(f'Done : {msg}')

    # functions
    #

    def runSetting(self):
        loadJsonData = self.JASON_HANDLER.loadJasonFile()
        run = MAIN_HANDLER(
            self,
            loadJsonData[self.tabName_setting]['chromePath']['value'],
            loadJsonData[self.tabName_email]['condition']['value'],
            loadJsonData[self.tabName_email]['findOrders']['value'],
            loadJsonData[self.tabName_email]['tag']['value'],
            loadJsonData[self.tabName_email]['template']['value']
        )
        return run

    def returnUiMessageHandler(self, value, tag=''):
        text = tag + ' : ' if tag != '' else ''
        self.textbox.configure(state='normal')
        self.textbox.insert("0.0", f'\n{text}{value}\n\n', tag)
        self.textbox.insert(
            "0.0", f'{time.strftime("%m/%d %H:%M:%S", time.localtime())}', 'time')
        self.textbox.configure(state='disabled')
        self.textbox.update()
        print(value)



# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#         # configure window.
#         self.displayWidth = self.winfo_screenwidth()  # Width of the screen
#         self.displayHeight = self.winfo_screenheight()  # Height of the screen
#         self.width = 1400
#         self.height = 800
#         self.x = (self.displayWidth/2) - (self.width/2)
#         self.y = (self.displayHeight/2) - (self.height/2)
#         self.title("All for one")
#         self.geometry('%dx%d+%d+%d' %
#                       (self.width, self.height, self.x, self.y))
#         self.minsize(self.width, self.height)
#         self.appTitle = 'ALL FOR ONE.'

#         self.button = customtkinter.CTkButton(master=self,
#                                               width=120,
#                                               height=32,
#                                               border_width=0,
#                                               corner_radius=8,
#                                               text="CTkButton",
#                                               command=self.button_events)
#         self.button.place(relx=0.5, rely=0.5, anchor='center')
#         self.toplevel_window = None

#     def button_events(self):
#         if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
#             # create window if its None or destroyed
#             self.toplevel_window = ToplevelWindows(self)
#             self.toplevel_window.grab_set() 
#         else:
#             self.toplevel_window.focus()  # if window exists focus it


