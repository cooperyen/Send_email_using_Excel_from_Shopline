import tkinter
import tkinter.messagebox
import customtkinter
from web_handler.create_chrome import pathCheckChrome
from main import running,AutoEmailingAndDownlaoding
from web_handler.funcs import waitWithSec
import json
import os
import time
import re
from excel_handler.xlrdtest import createNewExcelWithData
from web_handler.create_chrome import createChrome
from web_handler.webdriver_setting import Driver, driverURL

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

JSON_FILE = 'setting.json'

class JASON_HANDLER():

    def writeJsonFile(data):
        with open(JSON_FILE, 'w') as json_file:
            json.dump(data, json_file)

        json_file.close()

    def loadJasonFile():
        with open(JSON_FILE, 'r') as json_file:
            return json.load(json_file)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window.
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1500}x{800}")
        self.minsize(1500, 800)

        # configure grid layout (4x4).
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.datas = {
            'chromePath': {
                'en': 'Chrome path',
                'ch': 'Chrome 路徑',
                'info' : 'C:/Program Files/Google/Chrome/Application/chrome.exe',
                'value':''
            },
            'condition': {
                'en': 'Condition',
                'ch': '匹配條件',
                'info':'',
                'value':''
            },
            'findOrders': {
                'en': 'Find orders',
                'ch': '匹配訂單數',
                'value':''
            },
            'tag': {
                'en': 'Tag Name',
                'ch': '標籤名稱',
                'value':''
            },
            'template': {
                'en': 'Template Name',
                'ch': '套版名稱',
                'value':''
            },
        }

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.sidebar_frames = customtkinter.CTkScrollableFrame(
            self, width=200, corner_radius=0, fg_color="transparent")
        self.sidebar_frames.grid(row=1, column=1, rowspan=5, sticky="nsew")
        self.sidebar_frames.grid_rowconfigure(20, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.saveBtnEvent)
        self.sidebar_button_1.configure(text='save')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)

        self.appearance_mode_optionemenu.grid(
            row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")

        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

    
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, height=250, state='disabled')
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # configure color tag.
        self.textbox.tag_config("Warning", foreground="#D05B5B")
        self.textbox.tag_config("Note", foreground="#B88347")
        self.textbox.tag_config("time", foreground="#8B8B8B")
        



        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=1, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False, values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(
            self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # self.settingOptionAreaContent()


   
    def settingOptionAreaContent(self):
        
        if (os.path.exists(JSON_FILE) == False):
            # self.writeJsonFile(self.datas)
            JASON_HANDLER.writeJsonFile(self.datas)
    
        saveJsonData = JASON_HANDLER.loadJasonFile()
  
        infoRowNum = 2
        mainRowNum = 1
        customtkinter.CTkLabel(
                self.sidebar_frames, text='Setting options', font=customtkinter.CTkFont(size=16, weight="bold")).grid(
                row=0, column=1,padx=20, pady=(20,5), sticky='w')
        
        for labels in self.datas :
            customtkinter.CTkLabel(
                self.sidebar_frames, text=f"{self.datas[labels]['en']}", anchor="w").grid(
                row=1 if mainRowNum == 1 else mainRowNum, column=1,padx=20, pady=(0,0), sticky='w')
            
            # information label
            customtkinter.CTkLabel(
                self.sidebar_frames, text=f"{self.datas[labels]['en']}", anchor="w").grid(
                row=infoRowNum, column=2,sticky='w')

            globals()[f'__ui_labelsData_{labels}'] = customtkinter.CTkEntry(self.sidebar_frames, width=400)

            if(labels != 'condition' ):
                globals()[f'__ui_labelsData_{labels}'].grid(row=1 if mainRowNum == 1 else mainRowNum , column=2, pady=(10, 0))
                globals()[f'__ui_labelsData_{labels}'].insert(0,saveJsonData[labels]['value'])

            if(labels == 'condition'):
                globals()[f'__ui_labelsData_{labels}'] = customtkinter.CTkOptionMenu(master=self.sidebar_frames,
                                     values=['>', '<','=','>=','<='])
                globals()[f'__ui_labelsData_{labels}'].set(saveJsonData[labels]['value'])
                globals()[f'__ui_labelsData_{labels}'].grid(row=3 , column=2, pady=(10, 0),sticky='w')


            infoRowNum = infoRowNum + 2
            mainRowNum = mainRowNum + 2
        
           
    def saveSettingOptionToFile(self):


        def checkSettingAllTrue(ary):
            array = []
            for i in range(len(ary)) :
                array.append(ary[i]['bool'])
            return all(array)

        def checkSettingOptionNotEmpty():
            array = []
            for labels in self.datas :
                array.append(self.datas[labels]['value'])
                
            return all(array)
        
        # append setting option value.
        for labels in self.datas :
            self.datas[labels]['value'] = globals()[f'__ui_labelsData_{labels}'].get()

        # verify 'findOrders' is integer or not. 
        try:
            int(self.datas['findOrders']['value'])
            findOrdersBool = True
        except:
            findOrdersBool = False
        
        # verify and Warning setting options.
        verifySettingList = [
            {
                'title':'settingOption',
                'text':'Setting options can\'t not be empty, please try again.',
                'bool':checkSettingOptionNotEmpty()
            },
            {
                'title':'chromePath',
                'text':'Chrome path not found, please check and try again.',
                'bool':pathCheckChrome(self.datas['chromePath']['value'])
            },
            {
                'title':'tag',
                'text':'Tag have symbols, please remove and try again.',
                'bool':True if re.search(r"\W",self.datas['tag']['value']) == None else False
            },
            {
                'title':'findOrders',
                'text':'"Find orders" is not type of integer, make sure only input numbers without any character and symbols that try again.',
                'bool':findOrdersBool
            },
        ]

        # Verifies that each option Boolean and displays a Warning message if FALSE.
        for i in range(len(verifySettingList)):
            if(verifySettingList[i]['bool'] == False):
                self.returnUiWarningMessage(verifySettingList[i]['bool'],verifySettingList[i]['text'])
                break

        # if all options are True that save data to json.
        if(checkSettingAllTrue(verifySettingList)):
            self.returnUiMessage('Setting options saved.')
            JASON_HANDLER.writeJsonFile(self.datas) 
            return True
            

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def returnUiMessage(self, value, tag=''):
        text = tag + ' : ' if tag != '' else ''
        self.textbox.configure(state='normal')
        self.textbox.insert("0.0", f'\n{text}{value}\n\n', tag)
        self.textbox.insert("0.0", f'{time.strftime("%m/%d %H:%M:%S", time.localtime())}', 'time')
        self.textbox.configure(state='disabled')
        self.textbox.update()
        print(value)

    def returnUiWarningMessage(self, data, str):
            if(data):
                return True
            else:
                self.returnUiMessage(str,'Warning')
                return False
            
    def saveBtnEvent(self):
        saveSettingOptionToFile = self.saveSettingOptionToFile()  

        if(saveSettingOptionToFile):
            saveJsonData = JASON_HANDLER.loadJasonFile()
            
            run = AutoEmailingAndDownlaoding(
                self, 
                saveJsonData['chromePath']['value'], 
                saveJsonData['condition']['value'], 
                saveJsonData['findOrders']['value'], 
                saveJsonData['tag']['value'],
                saveJsonData['template']['value']
                )

            self.returnUiMessage('starting process, please do not control you\'re computer before finish process.', 'Note')
            self.returnUiMessage('starting process, please do not control you\'re computer before finish process.', 'Note')
            self.returnUiMessage('Starting : Open chrome porcessing.')
            createChrome(saveJsonData['chromePath']['value'])
            driver = Driver().run()
            self.returnUiMessage('Done : Open chrome porcessing.')

            self.returnUiMessage('Starting : Get all customer data porcessing.')
            run.getAllCustomerData(driver)
            self.returnUiMessage('Done : Get all customer data porcessing.')

            driver.close()
            self.returnUiMessage('done, colse chrome porcessing.', 'Note')
            # # setting chrome
            # self.returnUiMessage('Starting : Open chrome porcessing')
            # waitWithSec()
            # run.sendingEmails(self)
            # createNewExcelWithData(self,run.excelData(), types=run.tag)
            # self.returnUiMessage('Done : Open chrome porcessing')

