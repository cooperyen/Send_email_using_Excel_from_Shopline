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
        self.geometry(f"{1100}x{580}")
        self.minsize(1100, 580)

        # configure grid layout (4x4).
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.datas = {
            'downloadPath': {
                'en': 'Browser download path',
                'ch': '瀏覽器下載路徑',
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
            self.sidebar_frame, command=self.sidebar_button_event)
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
        self.textbox = customtkinter.CTkTextbox(self, width=250,state='disabled')
        self.textbox.grid(row=0, column=1, padx=(
            20, 0), pady=(20, 20), sticky="nsew")
        
        # configure color tag.
        self.textbox.tag_config("wearing", foreground="#D05B5B")
        self.textbox.tag_config("time", foreground="#8B8B8B")
        



        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(
            self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.settingOptionAreaContent()


   
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
        
    def returnValues(saveJsonData, item):
        result = saveJsonData[item]['value'] if 'value' in saveJsonData[item] else 'x'
        print(result)
        return result

    def sidebar_button_event(self):



        # for labels in self.datas :
        #     if(globals()[f'__ui_labelsData_{labels}'].get() == '') :
        #         exit()

        #     self.datas[labels]['value'] = globals()[f'__ui_labelsData_{labels}'].get()
        
        # run = AutoEmailingAndDownlaoding(self, 'C:/Program Files/Google/Chrome/Application/chrome.exe', '=', 0, '0407test', 'test')

        # # setting chrome
        # self.returnStatus('Starting : Open chrome porcessing')
        # waitWithSec()
        # run.sendingEmails()
        # self.returnStatus('Done : Open chrome porcessing')

        def loooping(data, str):
            if(data):
                return True
            else:
                self.returnStatus(str,'wearing')
                return False
             
        for labels in self.datas :
            self.datas[labels]['value'] = globals()[f'__ui_labelsData_{labels}'].get()

        settingOptionBool = loooping(self.checkSettingOptionNotEmpty(),'Setting options can\'t not be empty, please try again.')

        downloadPathBool = loooping(pathCheckChrome(self.datas['downloadPath']['value']),'Chrome path not found, please check and try again.')

        tagBool = loooping( True if re.search(r"\W",self.datas['tag']['value']) == None else False, 'Tag have symbols, please remove and try again.')



        if(settingOptionBool and downloadPathBool and tagBool):

            try:
                int(self.datas['findOrders']['value'])
                findOrdersBool = True
            except:
                findOrdersBool = loooping(False,'"Find orders" is not type of integer, please enter number and try again.')

   
        if settingOptionBool and findOrdersBool and downloadPathBool:
            self.returnStatus('Setting options saved.')
            JASON_HANDLER.writeJsonFile(self.datas)

        # findOrdersBool = loooping(int(self.datas['findOrders']['value']),'Setting options can\'t not be empty, please try again.')

 
   
        # if(self.checkSettingOptionNotEmpty()):
        #     print('1213')
        # else:
        #     self.returnStatus('Setting options can\'t not be empty, please try again.')
        # JASON_HANDLER.writeJsonFile(self.datas)

    def checkSettingOptionNotEmpty(self):
        array = []
        for labels in self.datas :
            array.append(self.datas[labels]['value'])
            
        return all(array)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


    def returnStatus(self, value, tag=''):

        self.textbox.configure(state='normal')
        self.textbox.insert("0.0", f'\n{value}\n\n', tag)
        self.textbox.insert("0.0", f'{time.strftime("%m/%d %H:%M:%S", time.localtime())}', 'time')
        self.textbox.configure(state='disabled')
        self.textbox.update()
        
        print(value)
