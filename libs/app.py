import customtkinter as ctk
import datetime
import libs.my_libs as my_libs
import libs.display as display


class App(ctk.CTk):
    """ the main class of the app """

    def __init__(self):
        """ the constructor of the app class """
        my_libs.logs("Main", "info", "loading the app")
        super().__init__()
        self.title("cours à réviser")
        self.minsize(width=1000, height=750)
        self.geometry("1000x750")
        self.iconbitmap("./icone.ico")

        self.top_bar = TopBar(self)
        self.display = display.Display(self)
        self.add_course = self.display.add_course
        self.bind("<Configure>", self.on_config)

        my_libs.logs("Main", "info", "the app is loaded")
        self.mainloop()

    def on_config(self, event):
        if event.widget == self:
            self.width = event.width
            self.height = event.height




class TopBar(ctk.CTkFrame):
    """ the class for the top bar """

    def __init__(self, master:App):
        """ the constructor for the top bar """
        my_libs.logs("top bar", "info", "loading the top bar")
        NORMAL_FONT = ctk.CTkFont(
            size=30
        )
        self.master = master

        super().__init__(
            master,
            fg_color = "#626262",
            width = 1000,
            height = 50,
            corner_radius = 0,
        )

        ctk.CTkLabel(
            master = self,
            text_color = "#c9c6c6",
            text = "Cours à réviser",
            font=NORMAL_FONT
        ).place(
            x = 300,
            y = 5
        )

        self.pack(
            side = ctk.TOP,
            fill = ctk.X,
            expand = False
        )

        my_libs.logs("top bar", "info", "the top bar is ready")


