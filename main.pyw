import customtkinter as ctk
import libs.my_lib_v2_1 as my_libs
import libs.display as display
import libs.add_course_type as add_courses_type
import libs.working_box as working_box


class App(ctk.CTk):
    """ the main class of the app """

    def __init__(self):
        """ the constructor of the app class """
        self.logs = my_libs.logs("Main")
        self.logs("starting the app")
        super().__init__()

        self.height = 1000
        self.width = 750

        self.title("cours à réviser")
        self.minsize(width=600, height=600)
        self.geometry("1000x750")
        self.iconbitmap("./icone.ico")

        self.option_bar = OptionBar(self)
        self.top_bar = TopBar(self)
        self.display = display.Display(self)
        self.add_course = self.display.add_course
        self.bind("<Configure>", self.on_config)

        self.logs("the app is loaded")
        self.mainloop()

    def on_config(self, event):
        if event.widget == self:
            scaling = self._get_window_scaling()
            self.width = event.width / scaling
            self.height = event.height / scaling
            self.display.update_courses()




class OptionBar(ctk.CTkFrame):
    """ the option bar at the very top """

    def __init__(self, master:App):
        """ the constructor of the option bar """
        self.logs = my_libs.logs("option bar")
        self.logs("initislise the option bar")

        super().__init__(
            master,
            height = 50
        )

        self.courses_button = ctk.CTkButton(
            self,
            corner_radius=0,
            text = "cours",
            command = self.add_course_type
        )
        self.courses_button.pack(
            side = ctk.LEFT
        )

        self.working = ctk.CTkButton(
            self,
            corner_radius=0,
            text = "working planning",
            command = self.working_box
        )
        self.working.pack(
            side = ctk.LEFT
        )


        self.pack(
            side = ctk.TOP,
            fill = ctk.X,
            expand = False
        )

    def add_course_type(self) -> None:
        """ open the box to add a course type """
        add_courses_type.AddCourseType(self.master)

    def working_box(self) -> None:
        """ open the working box """
        working_box.ChangePlanning(self.master)





class TopBar(ctk.CTkFrame):
    """ the class for the top bar """

    def __init__(self, master:App):
        """ the constructor for the top bar """
        self.logs = my_libs.logs("top bar")
        self.logs("loading the top bar")
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

        self.logs("the top bar is ready")




App()