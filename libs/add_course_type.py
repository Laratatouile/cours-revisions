import customtkinter as ctk
import libs.my_lib_v2_1 as my_libs


class AddCourseType(ctk.CTkToplevel):
    """ add a type of course """

    def __init__(self, master:ctk.CTkFrame) -> None:
        """ constructor of the class """
        self.logs = my_libs.logs("courses type")
        self.logs("oppening the window to add a course type")

        super().__init__(
            master,
        )
        self.minsize(200, 150)
        self.iconbitmap("./icone.ico")

        self.master = master

        self.geometry("200x150")
        self.title("ajouter un type de cour")

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
            text = "Ajouter",
            command=self.add
        ).place(
            x = 20,
            y = 90
        )

        self.logs("the window to add a course type is oppened")



    def add(self, *args) -> None:
        """ Add the course to the database """
        self.logs("adding the course")

        courses = my_libs.json_read("./courses/options.json")["courses_type"]
        if courses == False: courses = []
        
        courses.append(self.text.get())
        
        my_libs.json_save(courses, "./courses/options.json")
        self.destroy()
        self.logs("the course is added and the window is closed")

