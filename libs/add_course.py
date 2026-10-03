import customtkinter as ctk
import time
import datetime
import libs.my_lib_v2_1 as my_libs



class AddCourseWindow(ctk.CTkToplevel):
    """ generate a new window to add a course """

    def __init__(self, masterr:AddCourse) -> None:
        """ constructor of the class """
        self.logs = my_libs.logs("courses")
        self.logs("oppening the window to add a course")

        super().__init__(
            masterr,
        )

        self.minsize(200, 270)
        self.iconbitmap("./icone.ico")
        self.masterr = masterr

        self.geometry("200x270")
        self.title("ajouter un cour")

        self.courses_options = my_libs.json_read("./courses/options.json")
        if self.courses_options == False: self.logs("the courses types can't be loaded", 1)

        ctk.CTkLabel(
            master = self,
            text="Nom du cour :"
        ).place(
            x = 20,
            y = 10
        )

        self.course_var = ctk.StringVar(value=self.courses_options["courses_types"][0])
        optionmenu = ctk.CTkOptionMenu(
            self,
            values=self.courses_options["courses_types"],
            variable=self.course_var
        )
        optionmenu.place(
            x = 20,
            y = 40
        )


        ctk.CTkLabel(
            master = self,
            text="Numéro du chapitre :"
        ).place(
            x = 20,
            y = 80
        )

        self.chap = ctk.StringVar(value="")
        entry = ctk.CTkEntry(
            master = self,
            textvariable = self.chap
        )
        entry.place(
            x = 20,
            y = 110
        )


        ctk.CTkLabel(
            master = self,
            text="Numéro des pages :"
        ).place(
            x = 20,
            y = 150
        )
        
        self.page1 = ctk.StringVar(value="")
        ctk.CTkEntry(
            width = 40,
            master = self,
            textvariable = self.page1
        ).place(
            x = 20,
            y = 180
        )

        ctk.CTkLabel(
            master = self,
            text="à"
        ).place(
            x = 75,
            y = 180
        )

        self.page2 = ctk.StringVar(value="")
        ctk.CTkEntry(
            width = 40,
            master = self,
            textvariable = self.page2
        ).place(
            x = 100,
            y = 180
        )
        

        ctk.CTkButton(
            self,
            text = "Ajouter",
            command = self.verif_add
        ).place(
            x = 20,
            y = 230
        )

        self.focus_set()
        self.logs("the window to add a course is oppened")
        return


        
    def verif_add(self, *args) -> None:
        """ verification if the numbers waited are really numbers """
        try:
            a = int(self.chap.get())
            p1 = int(self.page1.get())
            p2 = int(self.page2.get())

            if p1 > p2: return
        except: return

        self.add()
        return



    def add(self) -> None:
        """ Add the course to the database """
        self.logs("adding the course")

        courses = my_libs.json_read("./courses/courses.json")
        if courses == False: courses = {}

        course = self.course_var.get()
        chap = self.chap.get()
        page1 = int(self.page1.get())
        page2 = int(self.page2.get())

        contain = {
            "date": str(datetime.date.today()),
            "page1": page1,
            "page2": page2,
            "worked": 0
        }

        if course in courses.keys():
            if chap in courses[course]:
                courses[course][chap].append(contain)
            else:
                courses[course][chap] = [contain]
        else:
            courses[course] = {}
            courses[course][chap] = [contain]

        my_libs.json_save(courses, "./courses/courses.json")
        self.destroy()
        self.masterr.masterr.display_courses()
        self.logs("the course is added and the window is closed")








class AddCourse(ctk.CTkButton):
    """ the button to add a course """

    def __init__(self, masterr:ctk.CTkFrame) -> None:
        """ the constructor of the button to add a course """
        self.logs = my_libs.logs("courses")
        self.logs("adding the button to add courses")

        self.masterr = masterr

        super().__init__(
            master = masterr.master,
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

        self.logs("the button to add courses is added")



    def add_course(self) -> None:
        """ add a course to the list of courses """
        self.logs("add a course")
        AddCourseWindow(self)