import customtkinter as ctk
import libs.my_lib_v2_1 as my_libs
import datetime
import libs.add_course as add_course



class Display(ctk.CTkFrame):
    """ class used to display all the courses """

    def __init__(self, masterr:ctk.CTk) -> None:
        """" constructor of the Display class """
        self.logs = my_libs.logs("disp courses")
        self.logs("loading the courses")
        super().__init__(
            masterr
        )

        self.list_texts = []

        self.first_time = True
        self.masterr = masterr

        self.times = my_libs.json_read("./courses/options.json")["working_planning"]
        # self.days = [31, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336, 367]
        # str_day = str(datetime.date.today())
        # self.day = self.days[int(str_day[5:7])] + int(str_day[8:10])

        self.display_courses()

        self.pack(
            side = ctk.TOP,
            fill = ctk.BOTH,
            expand = True
        )

        # add the button to add courses
        self.add_course = add_course.AddCourse(self)
        self.logs("all the courses are loaded and the function to add courses is ready")



    def display_courses(self) -> None:
        """ function that read the file and display all the courses to revise """
        self.logs("loading all the courses")
        
        cours = my_libs.json_read("./courses/cours.json")
        if cours == False:
            cours = {}

        self.logs("all the courses are loaded")
        self.logs("searching for the courses to revise")

        self.displayable = {}

        for crs_name, course in cours.items():
            self.displayable[crs_name] = {}
            for chap_id, chap in course.items():
                self.displayable[crs_name][chap_id] = []
                for id, elmt in enumerate(chap):

                    dt = (datetime.date.today() - datetime.date.fromisoformat(elmt["date"])).days
                    if dt >= self.times[elmt["worked"]]:
                        if self.displayable[crs_name][chap_id] == []:
                            self.displayable[crs_name][chap_id].append([elmt["page1"], elmt["page2"], [id]])
                        else:
                            if elmt["page1"] - self.displayable[crs_name][chap_id][-1][1] <= 2:
                                self.displayable[crs_name][chap_id][-1][1] = elmt["page2"]
                                self.displayable[crs_name][chap_id][-1][2].append(id)
                            else:
                                self.displayable[crs_name][chap_id].append([elmt["page1"], elmt["page2"], [id]])

                if len(self.displayable[crs_name][chap_id]) == 0:
                    del self.displayable[crs_name][chap_id]
            if len(self.displayable[crs_name]) == 0:
                del self.displayable[crs_name]

        self.logs("the courses to revise are loaded try displaying it")
        self.update_courses()




    def update_courses(self):
        """ update the courses """
        self.x = 10
        self.y = 10
        dec_x = 80
        

        if not self.first_time:
            for course in self.list_buttons.values():
                for chap in course.values():
                    for elmt in chap.values():
                        try:
                            elmt.place_forget()
                        except: pass

            for elmt in self.list_texts:
                elmt.place_forget()

        self.list_buttons = {}
        self.list_texts = []

        for crs_name, course in self.displayable.items():

            self.x = 10
            self.list_texts.append(ctk.CTkLabel(self, text=f"Matière : {crs_name.upper()} :"))
            self.list_texts[-1].place(x=self.x +70, y=self.y)
            self.y += 40
            self.list_buttons[crs_name] = {}

            for chap_id, chap in course.items():

                self.x = 10
                self.list_texts.append(ctk.CTkLabel(self, text=f"Chapitre {chap_id} :"))
                self.list_texts[-1].place(x=self.x, y=self.y)
                self.x += 70
                self.list_buttons[crs_name][chap_id] = {}

                for elmt in chap:

                    if self.x + dec_x + 20 >= self.masterr.width - 10:
                        self.x = 10
                        self.y += 40
                    
                    self.list_buttons[crs_name][chap_id][id] = Button(self, self.x, self.y, elmt, [crs_name, chap_id, elmt[2]])
                    self.x += dec_x + 200

                self.y += 40
            self.y += 20

        self.first_time = False
        self.logs("all the courses to revise are displayed")




class Button(ctk.CTkButton):
    """ a class for the button """

    def __init__(self, masterr:Display, x:int, y:int, pages:list, course_id:list) -> None:
        """ the constructor of a button to display one course """
        self.logs = my_libs.logs("Button")

        super().__init__(
            masterr,
            command = self.delete,
            text = f"pages {pages[0]} à {pages[1]}",
        )

        self.course_id = course_id
        self.masterr = masterr

        self.place(
            x = x,
            y = y
        )


    def delete(self) -> None:
        """ delete the button and change the course """
        self.logs("an other course is revised, well played")
        
        courses = my_libs.json_read("./courses/cours.json")

        for id in self.course_id[2]:
            elmt = courses[self.course_id[0]][self.course_id[1]][id]

            if elmt["worked"] == len(self.masterr.times):
                # supprime pas les bons parce que fusion des collés
                del courses[self.course_id[0]][self.course_id[1]][id]
                if courses[self.course_id[0]][self.course_id[1]] == []:
                    del courses[self.course_id[0]][self.course_id[1]]
                if courses[self.course_id[0]] == {}:
                    del courses[self.course_id[0]]
            else:
                elmt["worked"] += 1

        my_libs.json_save(courses, "./courses/cours.json")
        self.logs("reloading all the buttons")
        self.masterr.display_courses()
        