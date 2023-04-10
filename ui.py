import tkinter
import tkinter.messagebox
import customtkinter
from main import running,AutoEmailingAndDownlaoding
from web_handler.funcs import waitWithSec

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

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

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.sidebar_frames = customtkinter.CTkFrame(
            self, width=200, corner_radius=0, fg_color="transparent")
        self.sidebar_frames.grid(row=1, column=1, rowspan=5, sticky="nsew")
        self.sidebar_frames.grid_rowconfigure(5, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.configure(text='new_text')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_4 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

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
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        # self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        # self.entry.grid(row=3, column=1, columnspan=2, padx=(
        #     20, 0), pady=(20, 20), sticky="nsew")

        # self.main_button_1 = customtkinter.CTkButton(
        #     master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        # self.main_button_1.grid(row=3, column=3, padx=(
        #     20, 20), pady=(20, 20), sticky="nsew")


        

        # self.appearance_mode_labels = customtkinter.CTkLabel(
        #     self.sidebar_frames, text="Appearance Mode:", anchor="w")
        # self.appearance_mode_labels.grid(
        #     row=1, column=1,padx=20, pady=(10, 20))

        # self.label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # self.dataVlaue = customtkinter.CTkEntry(self.sidebar_frames, width=250)
        # self.dataVlaue.grid(row=1, column=2, pady=(10, 20))
        # self.dataVlaue = customtkinter.CTkEntry(self.sidebar_frames, width=250).grid(row=1, column=2, pady=(10, 20))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(
            20, 0), pady=(20, 0), sticky="nsew")


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(
            20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(
            0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(
            self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)


        self.labelsTitles()

    def labelsTitles(self):
        num = 1
        for labels in self.datas :
            customtkinter.CTkLabel(
                self.sidebar_frames, text=f"{self.datas[labels]['en']}", anchor="w").grid(
                row=num, column=1,padx=20, pady=(10, 20),sticky='w')
            
            globals()[f'uiLabel_{labels}'] = customtkinter.CTkEntry(self.sidebar_frames, width=250)
            globals()[f'uiLabel_{labels}'].grid(row=num, column=2, pady=(10, 20))
            print(f'uiLabel_{labels}')
            num = num + 1
        


    def returnValues(saveJsonData, item):
        result = saveJsonData[item]['value'] if 'value' in saveJsonData[item] else 'x'
        print(result)
        return result

    def sidebar_button_event(self):
        # run = AutoEmailingAndDownlaoding(self, 'C:/Program Files/Google/Chrome/Application/chrome.exe', '=', 0, '0407test', 'test')

        # # setting chrome
        # self.returnStatus('Starting : Open chrome porcessing')
        # waitWithSec()
        # run.sendingEmails()
        # self.returnStatus('Done : Open chrome porcessing')
        print(globals()['uiLabel_downloadPath'].get())



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


    def returnStatus(self, value):
        self.textbox.insert("0.0", f'{value}\n\n')
        self.textbox.update()
        print(value)
