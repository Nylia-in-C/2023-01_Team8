# main python file - 395 team 8


import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3


table_columns = []

class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create references for things that can change - filepaths, charts etc.\
        # Can add more as needed
        self.file_path = ""
        self.file_label = QLabel()
        self.table = QTableWidget()

        self.setWindowTitle("Scheduler")

        self.setGeometry(50, 50, 970, 600)

        central_widget = QWidget()  # Must have central widget set
        central_widget.setLayout(self.create_vlayout())

        self.setCentralWidget(central_widget)

        self.show()

    # Creates all items for central widget
    def create_vlayout(self):
        vbox = QVBoxLayout(self)
        top_hbox = self.create_topHlayout()
        bottom_hbox = self.create_botHlayout()

        # Add layouts to overall area
        vbox.addLayout(top_hbox)
        vbox.addLayout(bottom_hbox)

        # Add spacing, currently there are "4" items (tophbox, bothbox, spacer 1, spacer 2)
        vbox.insertSpacing(1, 100)
        vbox.insertSpacing(3, 70)
        return vbox

    # Creates the top hbox where most information will be displayed
    def create_topHlayout(self):
        hbox = QHBoxLayout(self)
        self.create_tableview()
        hbox.addWidget(self.table)
        # Add stuff into this HBox as needed
        # This will most likely be the display of most information
        return hbox

    # Settings to create the TableView
    def create_tableview(self):

        try:
            # Connect to database to get headers
            database = sqlite3.connect("database/database.db")
            cursor = database.cursor()

            # Move to cohort table
            cursor.execute("SELECT * FROM COHORT")

            all_columns = cursor.description

            for column_name in all_columns:
                table_columns.append(column_name[0])

            self.table.setColumnCount(len(table_columns))
            self.table.setHorizontalHeaderLabels(table_columns)

            cursor.close()
            database.close()

        except:
            print("Could not read database")



    # Creates the bottom hbox where most user interaction takes place
    def create_botHlayout(self):
        hbox = QHBoxLayout(self)

        self.create_file_label()

        hbox.addWidget(self.create_buttons())
        hbox.addWidget(self.file_label)
        # Add stuff into this HBox as needed
        # Maybe make it inside a vbox later?
        return hbox

    # Currently only creates choose input button, can add more when / if needed
    def create_buttons(self):
        choose_input_button = QPushButton("Choose File", self)
        choose_input_button.setMaximumWidth(100)
        choose_input_button.clicked.connect(self.choose_file)
        return choose_input_button

    # The settings for the file chosen label
    def create_file_label(self):

        self.file_label.setText("No File Chosen")
        self.file_label.setFont(QFont("Arial", 14))

    # Action event for the choose file button
    def choose_file(self):

        chosen_file = QFileDialog.getOpenFileName(
            self,
            "Choose a file",
            os.getcwd(),
            "",  # Filters to be added later to show only excel type files
            ""
        )
        if chosen_file[0] == "":
            self.file_label.setText("No File Chosen")
            self.file_path = ""
        else:
            self.file_path = chosen_file[0]
            self.file_label.setText(chosen_file[0])



# total cohort size:
# total number of students:
# Cohorts per program: