import os
import sys

def check_path(file):
    
    #Check if running in .exe
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    elif __file__:
        app_path = os.path.dirname(__file__)
    file_path = os.path.join(app_path, file)
    #print(file_path)

    return file_path