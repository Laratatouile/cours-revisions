#!/usr/bin/env python

##################################
# file writed by maxime geoffroy #
##################################

from datetime import datetime
from json import load, dump


class logs:
    """ simplified and more readable console print """

    def __init__(self, loader:str) -> None:
        """ initialise instance for the specified loader """
        self.loader = loader
    
    def __call__(self, text:str, error_code:int=None) -> None:
        """
            print the informations in the console.
            if error_code = None everything is good
            if error_code = 0 it's a warning
            else the code exit
        """
        spacing = 18 - len(self.loader)

        if error_code:
            spacing = " " * (18 - len(self.loader) - (3 if error_code == 0 else 1))
            print(f"[{str(datetime.now())[11:-7]}] [ {self.loader} / {("WARNING" if error_code == 0 else "FATAL")} ]{spacing}: {text}")

            if error_code > 0: exit()

        else:
            spacing = " " *(18 - len(self.loader))
            print(f"[{str(datetime.now())[11:-7]}] [ {self.loader} / INFO ]{spacing}: {text}")
 



# simplified and console displayed saves in json files
_json_reader_logs = logs("JsonReader")
_json_writer_logs = logs("JsonWriter")

def json_read(file:str) -> any:
    """ if the file can't be loaded return False """
    try:
        with open(file, "r") as opened_file:
            data = load(opened_file)
        _json_reader_logs("the file has been readed")
    except Exception as e:
        _json_reader_logs("the file can't be readed : "+str(e), 0)
        return False
    return data

def json_save(data:any, file:str) -> bool:
    """ return if the file has been saved or not """
    try:
        with open(file, "w") as opened_file:
            dump(data, opened_file)
        _json_writer_logs("the file has been saved")
        return True
    except Exception as e:
        _json_writer_logs("the file can't be saved : "+str(e), 0)
    
