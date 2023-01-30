# main python file - 395 team 8


import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3


table_columns = []
classrooms = ["11-533", "11-534", "11-560", "11-562",
              "11-564", "11-458", "11-430", "11-320"
              "11-532 (Lab)"]

class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create references for things that can change - filepaths, charts etc.\
        # Can add more as needed
        self.file_path = ""
        self.file_label = QLabel()
        self.table = QTableWidget()
        # Make table unedittable
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.efficiency_input = QLineEdit()

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
        bottom_hbox = self.create_botlayout()

        # Add layouts to overall area
        vbox.addLayout(top_hbox)
        vbox.addSpacing(100)
        vbox.addLayout(bottom_hbox)
        vbox.addSpacing(20)

        # Add spacing, currently there are "4" items (tophbox, bothbox, spacer 1, spacer 2)

        return vbox

    # Creates the top hbox where most information will be displayed
    def create_topHlayout(self):
        hbox = QHBoxLayout(self)
        self.create_tableview()
        hbox.addWidget(self.table)
        # Add stuff into this HBox as needed
        # This will most likely be the display of most information
        return hbox

    # Creates the bottom layout where most user interaction takes place
    def create_botlayout(self):

        vbox = QVBoxLayout(self)

        vbox.addLayout(self.create_file_choose())

        vbox.addSpacing(50)

        vbox.addLayout(self.create_class_efficiency())

        return vbox

    # create the file choose layout / widgets
    def create_file_choose(self):

        hbox_file_choose = QHBoxLayout(self)
        choose_input_button = QPushButton("Choose File", self)
        choose_input_button.setMaximumWidth(100)
        choose_input_button.clicked.connect(self.choose_file)

        self.file_label.setText("No File Chosen")
        self.file_label.setFont(QFont("Arial", 14))

        hbox_file_choose.addWidget(choose_input_button)
        hbox_file_choose.addWidget(self.file_label)
        return hbox_file_choose

    # Makes layout for the class efficiency section
    def create_class_efficiency(self):
        hbox_all = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox_info = QHBoxLayout()

        label = QLabel("Proposed Cohort Size:")
        label.setFont(QFont("Times", 10))
        label.setMaximumWidth(150)

        self.efficiency_input= QLineEdit()
        self.efficiency_input.setPlaceholderText("Eg. 5")

        calculate = QPushButton("Calculate Efficiency")
        # Need to connect this button to a function

        hbox_info.addWidget(label)
        hbox_info.addWidget(self.efficiency_input)

        vbox.addLayout(hbox_info)
        vbox.addWidget(calculate)

        hbox_all.addLayout(vbox)

        # Remove this spacing if adding more stuff
        hbox_all.insertSpacing(1, self.width())

        return hbox_all




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


    # Settings to create the TableView
    def create_tableview(self):

        try:
            # Connect to database to get headers
            database = sqlite3.connect("database/database.db")
            cursor = database.cursor()

            # Move to cohort table
            cursor.execute("SELECT * FROM COHORT")

            self.create_column_headers(cursor)

            value_fill = cursor.fetchall()
            self.load_data(value_fill)

            cursor.close()
            database.close()

        except:
            print("Could not read database")


    # The following section will be for action events
    # or functions that are called repeatedly
    # after the initial startup
    def create_column_headers(self, cursor_obj):
        table_columns.clear()
        all_columns = cursor_obj.description
        for column_name in all_columns:
            table_columns.append(column_name[0])

        self.table.setColumnCount(len(table_columns))
        self.table.setHorizontalHeaderLabels(table_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Load data into tableview
    def load_data(self, row_data):

        self.table.setRowCount(len(row_data))
        columns = self.table.columnCount()

        for each_row in range(len(row_data)):
            for each_column in range(columns):
                 self.table.setItem(each_row, each_column, QTableWidgetItem(str(row_data[each_row][each_column])))

    def clear_table(self):
        self.table.clear()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)


# total cohort size:
# total number of students:
# Cohorts per program: