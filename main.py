#main python file - 395 team 8

import os, sys
import help_funcs
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from UI import UI, splash_screen
from PyQt5.QtWidgets import *
from database.database import *
import fill_data


def main():
    #check if database is empty - if empty, fill with default data
    db = help_funcs.check_path("database\database.db")  # database.db file path
    connection = create_connection(db)
    val = readProgramItem(connection, "%")
    if(len(val)<1):
        fill_data.createDefaultDatabase()
    close_connection(connection)

    #Set up GUI and run app
    app = QApplication([])
    app.setStyle('Fusion')
    window = UI.UI()
    window.hide()

    #Set up window centered
    w_rect = window.frameGeometry()
    center = QDesktopWidget().availableGeometry().center()
    w_rect.moveCenter(center)
    window.move(w_rect.topLeft())

    #Splash screen, then show main window
    #splash_screen.splash_screen(window)
    window.show()
    
    app.exec_()

if __name__ == "__main__":
    main()