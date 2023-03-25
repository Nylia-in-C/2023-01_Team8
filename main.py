#main python file - 395 team 8

import os
from UI import UI
from PyQt5.QtWidgets import *

def main():

    #Set up GUI and run app
    app = QApplication([])
    app.setStyle('Fusion')
    window = UI.UI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()