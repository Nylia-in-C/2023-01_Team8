#main python file - 395 team 8

from UI import UI
from PyQt5.QtWidgets import *
def main():

    app = QApplication([])
    window = UI.UI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()