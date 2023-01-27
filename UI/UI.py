#main python file - 395 team 8

import os
from PyQt5.QtWidgets import *


class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        # Create variables for filepaths, combobox choices etc.
        self.file_path = ""
        self.rename_type = 1
        self.start_number = 1

        self.setWindowTitle("Scheduler")

        self.setGeometry(800, 800, 800, 800)

        central_widget = QWidget()  # Must have central widget set
        central_widget.setLayout(self.create_vlayout())

        self.setCentralWidget(central_widget)

        self.show()


    def create_vlayout(self):   # Creates the interactions in central widget
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.create_buttons())
        vbox.addWidget(self.create_input())
        return vbox

    def create_buttons(self):
        btn = QPushButton("Create Schedule", self)
        return btn


    def create_input(self):

        # Maybe make this a file explorer browser?
        # Instead of taking a filepath
        directory_field = QLineEdit(self)
        directory_field.setPlaceholderText("Enter filepath")
        directory_field.setClearButtonEnabled(True)
        return directory_field