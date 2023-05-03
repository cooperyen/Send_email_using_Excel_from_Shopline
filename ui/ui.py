import customtkinter
from tkinter import * 
from handler.main import MERGE_HANDLER, EXECL_HANDLER,WEB_HANDLER, EMAIL_HANDLER, JASON_HANDLER
import os
import time
import re

warningColor = '#D05B5B'
lightBTN = '#54d68e'
darkBTN = '#319960'
mainBgColor = '#2a734b'
mainHoverColor = '#357a54'
secBgColor = '#1e5738'
optionBTNColor = '#124529'

# Modes: 'System' (standard), 'Dark', 'Light'
customtkinter.set_appearance_mode('Dark')

# Themes: 'blue' (standard), 'green', 'dark-blue'
# customtkinter.set_default_color_theme('blue')


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #### Configure window.
        # Width of the screen
        self.displayWidth = self.winfo_screenwidth()  
        # Height of the screen
        self.displayHeight = self.winfo_screenheight()
        self.width = 400
        self.height = 300


        #### Setting.
        self.minsize(self.width, self.height)
        self.resizable(False, False)
        # Window title
        self.title('Send test email')


        #### Coordinate window.
        self.x = (self.displayWidth/2) - (self.width/2)
        self.y = (self.displayHeight/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))


        #### Content layout.
        # title.
        self.title = customtkinter.CTkLabel(self, text='Send test email') 
        self.title.pack(padx=20, pady=20)
        # entry.
        self.entryBox = customtkinter.CTkEntry(master=self, placeholder_text='email', width=300)
        self.entryBox.pack(padx=20, pady=0 )
        # description.
        self.entryInfo = customtkinter.CTkLabel(master=self, text='If testing multiple emails at the same time, use  \',\'  to \nconnect emails.', justify='left', width=500)
        self.entryInfo.pack(pady=5)
        # Warning info.
        self.entryWarning = customtkinter.CTkLabel(master=self, text='', text_color=warningColor, font=customtkinter.CTkFont(weight='bold'))
        self.entryWarning.pack(padx=20, pady=20)
        # confirm button
        self.btn = customtkinter.CTkButton(self, command=self.sendEmail)
        self.btn.pack(padx=20, pady=10)
        self.btn.configure(text='SEND')
        

        #### Parent module
        self.parentModule = ''


    def sendEmail(self):
        entryBoxValue = self.entryBox.get()
    
        if(entryBoxValue != ''):
            entrySplit = entryBoxValue.split(',')
            emails = []
            
            for i in entrySplit:
                includeAtSymbol = True if '@' in i and len(i) >= 3 else False
                emailFormat = True if i.split('@')[0] !='' and i.split('@')[1] !='' else False

            if(includeAtSymbol and emailFormat):
                # remove any spaces
                for i in entrySplit:
                    emails.append(i.replace(' ',''))
                    self.parentModule.sendTestEmailHandler(emails)
                  
            else:
                self.entryWarning.configure(text='email format not correct.')
        
        else:
            self.entryWarning.configure(text='emails can\'t not be empty')

    # need def sendTestEmailHandler that pass parent module.
    def getParentModule(self, module):
        self.parentModule = module


class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.EXECL_HANDLER = EXECL_HANDLER()
        self.JASON_HANDLER = JASON_HANDLER()
        self.WEB_HANDLER = WEB_HANDLER()

        #### Configure window.
        # Width of the screen
        self.displayWidth = self.winfo_screenwidth()  
        # Height of the screen
        self.displayHeight = self.winfo_screenheight() 
        self.width = 1400
        self.height = 800


        #### Setting.
        self.appTitle = 'ALL FOR ONE.'
        self.title('ALL FOR ONE.')
   
        customtkinter_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.iconbitmap(os.path.join(customtkinter_directory, "icon.ico"))


        self.minsize(self.width, self.height)
        self.font = customtkinter.CTkFont(family='Microsoft JhengHei')
        # content datas. 
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
                    'info': 'enter {name} display user name.eg. Hi {name}, how are you?',
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
                    'info': 'Cooper Yen.',
                    'value': ''
                },
                'senderEmail': {
                    'en': 'sender email',
                    'ch': '寄件人郵箱',
                    'info': 'cooperyen079@gmail.com',
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

        #### Coordinate window.
        self.x = (self.displayWidth/2) - (self.width/2)
        self.y = (self.displayHeight/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))


        #### configure grid layout (4x4).
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        #### create sidebar frame with widgets
        # Frame
        self.sidebarFrame = SidebarFrame(self)
        self.sidebarFrame.grid(row=0, column=0, rowspan=5, sticky='nsew')
        self.sidebarFrame.grid_rowconfigure(6, weight=1)


        # Logo.
        self.logoLabel = customtkinter.CTkLabel(
            self.sidebarFrame, text=self.appTitle, font=customtkinter.CTkFont(size=20, weight='bold'))
        self.logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Appearance mode.
        self.appearanceModeLabel = customtkinter.CTkLabel(
            self.sidebarFrame, text='Appearance Mode:', anchor='w')
        self.appearanceModeLabel.grid(row=8, column=0, padx=20, pady=(10, 0))

        # Appearance mode options menu
        self.AppearanceModeOptionsMenu = customtkinter.CTkOptionMenu(
            self.sidebarFrame, values=[
            'Dark', 'System', 'Light'],
            command=self.switchAppearanceModeHandler,
            fg_color=secBgColor,
            button_color=optionBTNColor,
            button_hover_color=optionBTNColor
            )
        self.AppearanceModeOptionsMenu.grid(
            row=9, column=0, padx=20, pady=(10, 10))
        
        # scaling mode
        self.scalingMode = customtkinter.CTkLabel(
            self.sidebarFrame, text='UI Scaling:', anchor='w')

        self.scalingMode.grid(row=10, column=0, padx=20, pady=(10, 0))

        # scaling mode options menu
        self.scalingModeOptionsMenu = customtkinter.CTkOptionMenu(
            self.sidebarFrame, 
            values=['100%', '110%', '120%'], 
            command=self.switchScalingModeHandler,
            fg_color=secBgColor,
            button_color=optionBTNColor,
            button_hover_color=optionBTNColor
            )
        
        self.scalingModeOptionsMenu.grid(row=11, column=0, padx=20, pady=(10, 20))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(
            self, width=250, height=250, state='disabled')
        self.textbox.grid(row=0, column=1, padx=(
            20, 20), pady=(20, 20), sticky='nsew')

        # configure color tag.
        self.textbox.tag_config('Warning', foreground=warningColor)
        self.textbox.tag_config('Note', foreground='#B88347')
        self.textbox.tag_config('time', foreground='#8B8B8B')

        # configure tag
        self.tabNameEmail = 'target'
        self.tabNameSetting = 'setting'
        self.tabNameMailgun = 'mailgun'


        self.meunButtonsContent()
        self.settingOptionAreaContent()

    # export buttons layout.
    def meunButtonsContent(self):
        configureBTNS = [
            {
                'command': self.saveSettingOptionAsFileBTN,
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
                'command': self.executeAllProcessBTN,
                'text': 'Do all of the above'
            },
        ]

        # loop configure
        for i in range(len(configureBTNS)):
            # Global = locals()
            locals()[i] = customtkinter.CTkButton(
                self.sidebarFrame, command=configureBTNS[i]['command'], fg_color=mainBgColor, hover_color=mainHoverColor)
            locals()[i].configure(text=configureBTNS[i]['text'])
            locals()[i].grid(row=i+1, column=0, padx=20, pady=10)

        # alone configure
        sendTestEmailBTN = customtkinter.CTkButton(self.sidebarFrame, command=self.sendTestEmailBTN, fg_color='transparent', hover_color=mainHoverColor, border_color=mainHoverColor, border_width=2)
        sendTestEmailBTN.configure(text='Send test email', height=50)
        sendTestEmailBTN.grid(row=7, column=0, padx=20, pady=10)


    # export setting table layout.
    def settingOptionAreaContent(self):
        # create table view.
        self.tabview = customtkinter.CTkTabview(self, width=250, segmented_button_selected_color='white', text_color='black',segmented_button_selected_hover_color='white')
        self.tabview.grid(row=1, column=1, padx=(
            20, 20), pady=(0, 0), sticky='nsew')
        
        # add table table tag.
        self.tabview.add(self.tabNameEmail)
        self.tabview.add(self.tabNameSetting)
        self.tabview.add(self.tabNameMailgun)

        # tag configure.
        tableViewEmail = self.tabview.tab(self.tabNameEmail)
        tableViewSetting = self.tabview.tab(self.tabNameSetting)
        tableViewMailgun = self.tabview.tab(self.tabNameMailgun)

        # make sure will write file when first running.
        if (os.path.exists(self.JASON_HANDLER.saveJsonFileName) == False):
            self.JASON_HANDLER.writeJsonFile(self.datas)

        loadJsonData = self.JASON_HANDLER.loadJasonFile()
    
        # output tags layout.
        def tagsOption(tableView, tagName):
            mainRowNum = 1
            infoRowNum = 2
            
            # tag title.
            customtkinter.CTkLabel(
                tableView, text=self.datas['title'][tagName]['en'], font=customtkinter.CTkFont(size=16, weight='bold')).grid(
                    row=0, column=0, padx=20, pady=(20, 5), sticky='w')


            for labels in self.datas[tagName]:
                # items label
                customtkinter.CTkLabel(
                    tableView, text=f'{self.datas[tagName][labels]["en"]}', anchor='w', font=self.font).grid(
                    row=1 if mainRowNum == 1 else mainRowNum, column=0, padx=20, pady=(0, 0), sticky='w')

                # informations label
                customtkinter.CTkLabel(
                    tableView, text=f'{self.datas[tagName][labels]["info"]}', anchor='w', font=self.font).grid(row=infoRowNum, column=1, sticky='w')

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

        tagsOption(tableViewEmail, self.tabNameEmail)
        tagsOption(tableViewSetting, self.tabNameSetting)
        tagsOption(tableViewMailgun, self.tabNameMailgun)


    # Switch appearance mode.
    def switchAppearanceModeHandler(self, newAppearanceMode: str):
        customtkinter.set_appearance_mode(newAppearanceMode)


    # Switch scaling mode.
    def switchScalingModeHandler(self, newScaling: str):
        new_scaling_float = int(newScaling.replace('%', '')) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    # Display message in "self.textbox" container.
    def displayUiMessageHandler(self, value, tag=''):
        text = tag + ' : ' if tag != '' else ''
        self.textbox.configure(state='normal')
        self.textbox.insert('0.0', f'\n{text}{value}\n\n', tag)
        self.textbox.insert(
            '0.0', f'{time.strftime("%m/%d %H:%M:%S", time.localtime())}', 'time')
        self.textbox.configure(state='disabled')
        self.textbox.update()
        print(value)


    # Execute all process btn.
    def executeAllProcessBTN(self):
        saveSettingOptionAsFile = self.saveSettingOptionAsFileHandler()

        if (saveSettingOptionAsFile):
            loadJsonData = self.JASON_HANDLER.loadJasonFile()
            mergeHandler = self.mergeHandler()

            # opean chrome
            self.downloadUserDataHandler()

            self.saveAsExcelHanlder() if self.sendEmailHandler() else None

    
    # send email handler.
    # @return Value or False.
    def sendEmailHandler(self):
        saveSettingOptionAsFile = self.saveSettingOptionAsFileHandler()

        if (saveSettingOptionAsFile):
            msg = 'sending Emails processing.'
            self.displayUiMessageHandler(f'Starting : {msg}')

            loadJsonData = self.JASON_HANDLER.loadJasonFile()

            mergeHandler = self.mergeHandler()
            exportXlsxData = mergeHandler.exportXlsxData()

            emailHandler = EMAIL_HANDLER(self, loadJsonData, exportXlsxData)
            sendingEmails = emailHandler.sendingEmails()

            if(exportXlsxData and sendingEmails['state']):
                self.displayUiMessageHandler(f'A total of {len(exportXlsxData)} emails were sent')
                self.displayUiMessageHandler(f'Done : {msg}')

            return sendingEmails['state']
        else:
            return False
    def sendEmailBTN(self):
        sendEmail = self.sendEmailHandler()

        if (sendEmail):
            self.saveToExcelBTN()


    # send a test mail.
    # @return Value or False.
    def sendTestEmailHandler(self, email):
        saveSettingOptionAsFile = self.saveSettingOptionAsFileHandler()

        if (saveSettingOptionAsFile):
            msg = 'direct sending Email processing.'
            self.displayUiMessageHandler(f'Starting : {msg}')

            loadJsonData = self.JASON_HANDLER.loadJasonFile()
            mergeHandler = self.mergeHandler()
            emailHandler = EMAIL_HANDLER(self, loadJsonData)
            sendingEmails = emailHandler.directSendEmails(email)

            if(sendingEmails['state']):
                self.displayUiMessageHandler(f'Done : {msg}')
                self.displayUiMessageHandler(f'A total of {sendingEmails["num"]} emails were sent') 

            return sendingEmails['num']
        else:
            return False
    def sendTestEmailBTN(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = ToplevelWindow(self)  
            self.toplevel_window.grab_set() 
        else:
            # if window exists focus it.
            self.toplevel_window.focus()  

        self.toplevel_window.getParentModule(self)
        

    # save GUI options as a file.
    # @return boolen.
    def saveSettingOptionAsFileHandler(self):

        def checkSettingAllTrue(ary):
            array = []
            for i in range(len(ary)):
                array.append(ary[i]['bool'])
            return all(array)

        def checkSettingOptionNotEmpty():
            array = []
            for labels in self.datas[self.tabNameEmail]:
                array.append(self.datas[self.tabNameEmail][labels]['value'])

            return all(array)

        # append setting option value.
        ary = [self.tabNameEmail, self.tabNameSetting, self.tabNameMailgun]
        for tab in ary:
            for labels in self.datas[tab]:
                self.datas[tab][labels]['value'] = globals(
                )[f'__ui_labelsData_{labels}'].get()

        # verify 'findOrders' is integer or not.
        try:
            int(self.datas[self.tabNameEmail]['findOrders']['value'])
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
                'bool': True if re.search(r'\W', self.datas[self.tabNameEmail]['tag']['value']) == None else False
            },
            {
                'title': 'findOrders',
                'text': '"Find orders" is not type of integer, make sure only input numbers without any character and symbols that try again.',
                'bool': findOrdersBool
            },
            {
                'title': 'chromePath',
                'text': f'Chrome path not found, please check "{self.tabNameSetting}" and try again.',
                'bool': self.WEB_HANDLER.pathCheckChrome(self.datas[self.tabNameSetting]['chromePath']['value'])
            },
            {
                'title': 'sender',
                'text': f'Sender can\'t not be empty, please check "{self.tabNameMailgun}" and try again.',
                'bool': True if self.datas[self.tabNameMailgun]['sender']['value'] != '' else False
            },
            {
                'title': 'senderEmail',
                'text': f'Sender\'s email have to include "@" and without any space. please check "{self.tabNameMailgun}" and try again.',
                'bool': '@' in self.datas[self.tabNameMailgun]['senderEmail']['value'] and ' ' not in self.datas[self.tabNameMailgun]['senderEmail']['value']
            },
            {
                'title': 'apiKey',
                'text': f'Apikey should start with "key-", please check "{self.tabNameMailgun}" and try again.',
                'bool': self.datas[self.tabNameMailgun]['apiKey']['value'].startswith('key-')
            },
            {
                'title': 'domain',
                'text': f'Domain can\'t not be empty, please check "{self.tabNameMailgun}" and try again.',
                'bool': True if self.datas[self.tabNameMailgun]['domain']['value'] != '' else False
            },
        ]

        # Verifies that each option Boolean and displays a Warning message if FALSE.
        for i in range(len(verifySettingList)):
            if (verifySettingList[i]['bool'] == False):
                self.displayUiMessageHandler(verifySettingList[i]['text'], 'Warning')
                break

        # if all options are True that save data to json.
        if (checkSettingAllTrue(verifySettingList)):
            self.JASON_HANDLER.writeJsonFile(self.datas)
            return True
    def saveSettingOptionAsFileBTN(self):
        saveSetting = self.saveSettingOptionAsFileHandler()
        if (saveSetting):
            self.displayUiMessageHandler('Setting options saved.')
            

    # download users data from "SHOPLINE"
    def downloadUserDataHandler(self):

        saveSettingOptionAsFile = self.saveSettingOptionAsFileHandler()

        if (saveSettingOptionAsFile):
            loadJsonData = self.JASON_HANDLER.loadJasonFile()
            mergeHandler = self.mergeHandler()

            # start
            self.displayUiMessageHandler(
                'starting process, please do not control you\'re computer before finish process.', 'Note')
            self.displayUiMessageHandler(
                'starting process, please do not control you\'re computer before finish process.', 'Note')

            # opean chrome
            self.displayUiMessageHandler('Starting : Open chrome processing.')

            self.WEB_HANDLER.createChrome(
                loadJsonData[self.tabNameSetting]['chromePath']['value'])

            driver = self.WEB_HANDLER.driver()
            self.displayUiMessageHandler('Done : Open chrome processing.')

            # get and download user data from shopline.
            self.displayUiMessageHandler(
                'Starting : Get all customer data processing.')
            mergeHandler.getAllCustomerData(driver)
            self.displayUiMessageHandler('Done : Get all customer data processing.')

            driver.close()
    def downloadUserDataBTN(self):
        self.downloadUserDataHandler()


    # save data as Excel handler
    def saveAsExcelHanlder(self):

        msg = 'saving user\'s data to excel.'
        self.displayUiMessageHandler(f'Starting : {msg}')

        mergeHandler = self.mergeHandler()
        self.EXECL_HANDLER.createNewExcelWithData(self, mergeHandler.exportXlsxData(), types=mergeHandler.tag)

        self.displayUiMessageHandler(f'Done : {msg}')
    def saveToExcelBTN(self):
        self.saveAsExcelHanlder()


    # return data.
    def mergeHandler(self):
        loadJsonData = self.JASON_HANDLER.loadJasonFile()
        result = MERGE_HANDLER(
            self,
            loadJsonData[self.tabNameSetting]['chromePath']['value'],
            loadJsonData[self.tabNameEmail]['condition']['value'],
            loadJsonData[self.tabNameEmail]['findOrders']['value'],
            loadJsonData[self.tabNameEmail]['tag']['value'],
            loadJsonData[self.tabNameEmail]['template']['value']
        )
        return result
    




