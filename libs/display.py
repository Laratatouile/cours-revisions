import customtkinter as ctk
import libs.my_libs as my_libs
import datetime
import libs.add_course as add_course

class Display(ctk.CTkFrame):
    """ class used to display all the courses """

    def __init__(self, master:ctk.CTk) -> None:
        """" constructor of the Display class """
        my_libs.logs("disp_courses", "info", "loading the courses")
        super().__init__(
            master
        )

        self.first_time = True

        self.times =  [0, 1, 5, 10, 30, 90]
        self.days = [31, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336, 367]
        str_day = str(datetime.date.today())
        self.day = self.days[int(str_day[5:7])] + int(str_day[8:10])

        self.display_courses()

        self.pack(
            side = ctk.TOP,
            fill = ctk.BOTH,
            expand = True
        )

        # add the button to add courses
        self.add_course = add_course.AddCourse(self)
        my_libs.logs("disp_courses", "info", "all the courses are loaded and the function to add courses is ready")



    def display_courses(self) -> None:
        """ function that read the file and display all the courses to revise """
        my_libs.logs("disp_courses", "info", "loading all the courses")

        self.x = 10
        self.y = 10
        
        cours = my_libs.json_read("./cours.json")
        if cours == None: my_libs.logs("disp_courses", "info", "the courses can't be loaded")

        my_libs.logs("disp_courses", "info", "all the courses are loaded")
        my_libs.logs("disp_courses", "info", "searching for the courses to revise")

        if not self.first_time:
            for elmt in self.list_buttons.values():
                try:
                    elmt.place_forget()
                except:pass

        displayable = {}
        self.list_buttons = {}

        for name, elmt in cours.items():
            course_day = self.days[int(elmt["date"][5:7])] + int(elmt["date"][8:10])
            if self.day - course_day >= self.times[elmt["revise"]]:
                displayable[name] = elmt

        my_libs.logs("disp_courses", "info", "the courses to revise are loaded try displaying it")

        for name, elmt in displayable.items():
            if self.x + len(name * 7) + 30 > 1000:
                self.x = 10
                self.y += 40
            self.list_buttons[name] = (Button(self, self.x, self.y, name))
            self.x += len(name * 7) + 30

        self.first_time = False
        my_libs.logs("disp_courses", "info", "all the courses to revise are displayed")




class Button(ctk.CTkButton):
    """ a class for the button """

    def __init__(self, master:ctk.CTkFrame, x:int, y:int, course_name:str) -> None:
        """ the constructor of a button to display one course """

        width = len(course_name * 7) + 10

        super().__init__(
            master,
            command = self.delete,
            text = course_name,
            width = width
        )

        self.course_name = course_name
        self.master = master

        self.place(
            x = x,
            y = y
        )


    def delete(self) -> None:
        """ delete the button and change the course """
        my_libs.logs("button", "info", f"the {self.course_name} course is revised, well played")
        
        courses = my_libs.json_read("./cours.json")
        elmt = courses[self.course_name]

        if elmt["revise"] == len(self.master.times):
            del courses[self.course_name]
        else:
            elmt["revise"] += 1

        self.place_forget()

        my_libs.json_save(courses, "./cours.json")
        my_libs.logs("button", "info", "reloading all the buttons")
        self.master.display_courses()
        