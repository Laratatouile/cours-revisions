import customtkinter as ctk
import time
import datetime
import libs.my_libs as my_libs



class AddCourseWindow(ctk.CTkToplevel):
    """ generate a new window to add a course """

    def __init__(self, master:ctk.CTkFrame) -> None:
        """ constructor of the class """
        my_libs.logs("courses", "info", "oppening the window to add a course")

        super().__init__(
            master,
        )

        self.master = master

        self.geometry("200x150")
        self.title("ajouter un cour")

        self.text = ctk.StringVar(self)


        ctk.CTkLabel(
            master = self,
            text="Nom du cour :"
        ).place(
            x = 20,
            y = 20
        )

        entry = ctk.CTkEntry(
            master = self,
            textvariable = self.text
        )
        entry.place(
            x = 20,
            y = 50
        )
        entry.bind("<Return>", self.add)
        entry.focus_set()

        ctk.CTkButton(
            self,
            width = 30,
            height = 10,
            text = "Ajouter",
            command=self.add
        ).place(
            x = 20,
            y = 90
        )

        self.grab_set()
        my_libs.logs("courses", "info", "the window to add a course is oppened")

        


    def add(self, *args) -> None:
        """ Add the course to the database """
        my_libs.logs("courses", "info", "adding the course")

        courses = my_libs.json_read("./cours.json")
        courses[self.text.get()] = {
            "date": str(datetime.date.today()),
            "revise" : 0
        }
        
        print(courses)
        my_libs.json_save(courses, "./cours.json")
        self.destroy()
        self.master.master.display_courses()
        my_libs.logs("courses", "info", "the course is added and the window is closed")





class AddCourse(ctk.CTkButton):
    """ the button to add a course """

    def __init__(self, master:ctk.CTkToplevel) -> None:
        """ the constructor of the button to add a course """
        my_libs.logs("courses", "info", "adding the button to add courses")

        self.master = master

        super().__init__(
            master = master,
            border_color = "",
            text = "+",
            font = ctk.CTkFont(
                size = 30
            ),
            width = 30,
            height = 30,
            corner_radius=30,
            command = self.add_course
        )

        self.place(
            relx = 0.9,
            rely = 0.9
        )

        my_libs.logs("courses", "info", "the button to add courses is added")

    def add_course(self) -> None:
        """ add a course to the list of courses """
        my_libs.logs("courses", "info", "add a course")
        AddCourseWindow(self)