import customtkinter


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # configure window.
        self.displayWidth = self.winfo_screenwidth()  # Width of the screen
        self.displayHeight = self.winfo_screenheight()  # Height of the screen
        self.width = 1400
        self.height = 800
        self.x = (self.displayWidth/2) - (self.width/2)
        self.y = (self.displayHeight/2) - (self.height/2)
        self.title("All for one")
        self.geometry('%dx%d+%d+%d' %
                      (self.width, self.height, self.x, self.y))
        self.minsize(self.width, self.height)
        self.appTitle = 'ALL FOR ONE.'

        self.button = customtkinter.CTkButton(master=self,
                                              width=120,
                                              height=32,
                                              border_width=0,
                                              corner_radius=8,
                                              text="CTkButton",
                                              command=self.button_events)
        self.button.place(relx=0.5, rely=0.5, anchor='center')
        self.toplevel_window = None

    def button_events(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = ToplevelWindow(self)
        else:
            self.toplevel_window.focus()  # if window exists focus it


app = App()
app.mainloop()
