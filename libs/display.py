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
        
        cours = my_libs.json_read("./courses/courses.json")
        if cours == False:
            cours = {}
            return

        self.logs("all the courses are loaded")
        self.logs("searching for the courses to revise")


        if not self.first_time:
            for course in self.list_buttons.values():
                for chap in course.values():
                    for elmt in chap.values():
                        try:
                            elmt.place_forget()
                        except: pass
        
            for elmt in self.list_texts:
                elmt.place_forget()
        
        self.displayable = {}
        self.list_buttons = {}
        self.list_texts = []

        self.x = 10
        self.y = 10
        dec_x = 80



        for crs_name, course in cours.items():
            self.displayable[crs_name] = {}
            self.list_buttons[crs_name] = {}

            for chap_id, chap in course.items():
                self.displayable[crs_name][chap_id] = []
                self.list_buttons[crs_name][chap_id] = {}

                for elmt_id, elmt in enumerate(chap):

                    dt = (datetime.date.today() - datetime.date.fromisoformat(elmt["date"])).days
                    if dt >= self.times[elmt["worked"]]:

                        if self.displayable[crs_name][chap_id] == []:
                            self.displayable[crs_name][chap_id].append([elmt["page1"], elmt["page2"], [elmt_id]])
                        
                        else:
                            if elmt["page1"] - self.displayable[crs_name][chap_id][-1][1] <= 2:
                                self.displayable[crs_name][chap_id][-1][1] = elmt["page2"]
                                self.displayable[crs_name][chap_id][-1][2].append(elmt_id)
                            else:
                                self.displayable[crs_name][chap_id].append([elmt["page1"], elmt["page2"], [elmt_id]])

                # create the buttons
                for nb_btn, elmt in enumerate(self.displayable[crs_name][chap_id]):
                    self.list_buttons[crs_name][chap_id][nb_btn] = Button(
                        self,
                        0, 0,
                        [elmt[0], elmt[1]],
                        [crs_name, chap_id, elmt[2]]
                    )


                if len(self.displayable[crs_name][chap_id]) == 0:
                    del self.displayable[crs_name][chap_id]
    
            if len(self.displayable[crs_name]) == 0:
                del self.displayable[crs_name]

        self.first_time = False
    
        self.logs("all the courses to revise are initialised")




    def update_courses(self):
        """ update the courses """
        self.x = 10
        self.y = 10
        dec_x = 80
    
        for elmt in self.list_texts:
            elmt.place_forget()

        self.list_texts = []

        for crs_name, course in self.displayable.items():

            self.x = 10
            self.list_texts.append(ctk.CTkLabel(self, text=f"Matière : {crs_name.upper()} :"))
            self.list_texts[-1].place(x=self.x +70, y=self.y)
            self.y += 40

            for chap_id, chap in course.items():

                self.x = 10
                self.list_texts.append(ctk.CTkLabel(self, text=f"Chapitre {chap_id} :"))
                self.list_texts[-1].place(x=self.x, y=self.y)
                self.x += 70

                for elmt_id, elmt in enumerate(chap):

                    # reset the position
                    if self.x + dec_x + 30 >= self.masterr.width:
                        self.x = 10
                        self.y += 50

                    self.list_buttons[crs_name][chap_id][elmt_id].place_configure(x=self.x*self.masterr.scaling, y=self.y*self.masterr.scaling)
                    self.x += dec_x + 70

                self.y += 50
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
        
        courses = my_libs.json_read("./courses/courses.json")

        for elmt_id in reversed(self.course_id[2]):
            if courses[self.course_id[0]][self.course_id[1]][elmt_id]["worked"] >= len(self.masterr.times) -1:
                # the real suppression
                del courses[self.course_id[0]][self.course_id[1]][elmt_id]

                # delete the part if the part is empty
                if courses[self.course_id[0]][self.course_id[1]] == []:
                    del courses[self.course_id[0]][self.course_id[1]]
                if courses[self.course_id[0]] == {}:
                    del courses[self.course_id[0]]
            else:
                courses[self.course_id[0]][self.course_id[1]][elmt_id]["worked"] += 1

        self.place_forget()
        my_libs.json_save(courses, "./courses/courses.json")
        self.logs("reloading all the buttons")
        self.masterr.display_courses()
        self.masterr.update_courses()
        