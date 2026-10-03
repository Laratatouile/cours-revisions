import customtkinter as ctk
import libs.my_lib_v2_1 as my_libs


class ChangePlanning(ctk.CTkToplevel):
    """ change the revision planning """

    def __init__(self, master:ctk.CTkFrame) -> None:
        """ constructor of the class """
        self.logs = my_libs.logs("courses type")
        self.logs("oppening the window to set the planning revision")

        super().__init__(
            master,
        )
        self.minsize(250, 200)
        self.iconbitmap("./icone.ico")

        self.master = master

        self.geometry("200x150")
        self.title("modifier le planning de révisions")

        courses = my_libs.json_read("./courses/options.json")
        if courses == False: courses = []

        list_work = ",".join([str(elmt) for elmt in courses["working_planning"]])

        self.text = ctk.StringVar(self, value=list_work)


        ctk.CTkLabel(
            master = self,
            text="jours de révisions des cours :"
        ).place(
            x = 20,
            y = 20
        )

        ctk.CTkLabel(
            master = self,
            text="(séparer les jours par des vigules)"
        ).place(
            x = 20,
            y = 40
        )

        entry = ctk.CTkEntry(
            master = self,
            textvariable = self.text
        )
        entry.place(
            x = 20,
            y = 80
        )
        entry.bind("<Return>", self.ok)
        entry.focus_set()

        ctk.CTkButton(
            self,
            text = "Ajouter",
            command=self.ok
        ).place(
            x = 20,
            y = 130
        )

        self.logs("the window to of working planning is oppened")



    def ok(self, *args) -> None:
        """ Save the revision planning """
        self.logs("saving the revisions")

        courses = my_libs.json_read("./courses/options.json")
        if courses == False: courses = []

        try:
            list_work = self.text.get().split(",")
            list_work = [int(elmt) for elmt in list_work]
        except: return
        
        courses["working_planning"] = list_work
        
        my_libs.json_save(courses, "./courses/options.json")
        self.destroy()
        self.logs("the planning is saved and the window is closed")

