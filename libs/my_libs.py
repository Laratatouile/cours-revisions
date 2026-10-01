#!/usr/bin/env python

##################################
# file writed by maxime geoffroy #
##################################

from datetime import datetime
from json import load, dump

# simplified and more readable console print
class logs:
    def __init__(self, loader:str, gravity:str, text:str, error_code:int=1) -> None:
        len_space = ""
        if len(loader) + len(gravity) < 18:
            space = 18 - (len(loader) + len(gravity))
            for _ in range(space):
                len_space += " "
        
        if gravity.upper() == "FATAL" :
            len_space += "  "
            self._ErrorExit(error_code, text, len_space, loader)
        else :
            self._log(loader, gravity.upper(), len_space, text)

    def _log(self, loader:str, gravity:str, len_space:str, text:str) -> None:
        print("["+str(datetime.now())[11:-7]+"] [ "+loader+" / "+gravity+" ]"+len_space+" : "+text)


    def _ErrorExit(self, error_code:str, error_text:str, len_space:str, loader:str) -> None:
        exit(str("[ "+str(datetime.now())[11:-7]+" ] [ "+loader+" / FATAL ]"+len_space+" : error code : "+str(error_code)+" : "+error_text))


# simplified and console displayed saves in json files
def json_read(file:str) -> any:
    try:
        with open(file, "r") as opened_file:
            data = load(opened_file)
        logs("JsonReader", "INFO", "the file has been readed")
    except Exception as e:
        logs("JsonReader", "FATAL", "the file can't be readed : "+str(e), 2)
    return data

def json_save(data:any, file:str) -> None:
    try:
        with open(file, "w") as opened_file:
            dump(data, opened_file)
        logs("JsonReader", "INFO", "the file has been saved")
    except Exception as e:
        logs("JsonReader", "FATAL", "the file can't be saved : "+str(e), 2)
    
