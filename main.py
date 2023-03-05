#main python file - 395 team 8

from UI import UI
from database.database import *
from PyQt5.QtWidgets import *
def main():
    database = r".\database\database.db"  #database.db file path 
    connection = create_connection(database)
    app = QApplication([])
    window = UI.UI()
    window.show()
    app.exec_()

    close_connection(connection)
if __name__ == "__main__":
    main()