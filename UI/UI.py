# main python file - 395 team 8

import os
import sqlite3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from imports.create_cohorts import *

table_columns = []

class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create references for things that can change - filepaths, charts etc.\
        # Can add more as needed
        self.file_path = ""
        self.file_label = QLabel()


        '''
        Creating tables for each tab
        and giving proper settings (i.e. un-editable, resize to width etc)
        '''
        self.main_table = QTableWidget()
        self.bg_calc_table = QTableWidget()

        self.main_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bg_calc_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Make table un-editable
        self.main_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.bg_calc_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.cohort_size = QLabel()

        self.setWindowTitle("Scheduler")

        self.setGeometry(50, 50, 970, 600)

        central_widget = QWidget()  # Must have central widget set
        central_widget.setLayout(self.create_vlayout())

        self.setCentralWidget(central_widget)

        self.show()

    # Creates all items for central widget
    def create_vlayout(self):
        vbox = QVBoxLayout(self)
        top_hbox = self.create_tabs()
        bottom_hbox = self.create_botlayout()

        # Add layouts to overall area
        vbox.addWidget(top_hbox)
        vbox.addSpacing(100)
        vbox.addLayout(bottom_hbox)
        vbox.addSpacing(20)

        # Add spacing, currently there are "4" items (tophbox, bothbox, spacer 1, spacer 2)

        return vbox

    # Creates the top hbox where most information will be displayed
    def create_tabs(self):
        hbox = QHBoxLayout(self)

        # Create tabs
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()

        tabs.addTab(tab1, "Main")
        tabs.addTab(tab2, "Cohort Calculations")

        hbox.addWidget(self.bg_calc_table)

        tab2.setLayout(hbox)

        return tabs

    # Creates the bottom layout where most user interaction takes place
    def create_botlayout(self):

        vbox = QVBoxLayout(self)

        vbox.addLayout(self.create_file_choose())

        vbox.addSpacing(50)

        vbox.addLayout(self.create_cohort_size())

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
    def create_cohort_size(self):
        hbox_all = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox_info = QHBoxLayout()

        label = QLabel("Optimal Cohort Size:")
        label.setFont(QFont("Times", 10))
        label.setMaximumWidth(150)

        self.cohort_size.setFont(QFont("Times", 10))
        self.cohort_size.setMaximumWidth(100)


        calculate = QPushButton("Calculate Cohort Sizes")
        calculate.clicked.connect(self.load_optimal_cohorts)
        # Need to connect this button to a function

        hbox_info.addWidget(label)
        hbox_info.addWidget(self.cohort_size)

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


    # The following section will be for action events
    # or functions that are called repeatedly
    # after the initial startup
    def create_db_column_headers(self, cursor_obj):
        table_columns.clear()
        all_columns = cursor_obj.description
        for column_name in all_columns:
            table_columns.append(column_name[0])

        self.bg_calc_table.setColumnCount(len(table_columns))
        self.bg_calc_table.setHorizontalHeaderLabels(table_columns)
        self.bg_calc_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Load data into tableview
    # row_data is a list of tuples generated from
    # a cursor object calling fetchall()
    def load_db(self, row_data):

        self.bg_calc_table.setRowCount(len(row_data))
        columns = self.bg_calc_table.columnCount()

        for each_row in range(len(row_data)):
            for each_column in range(columns):
                 self.bg_calc_table.setItem(each_row, each_column, QTableWidgetItem(str(row_data[each_row][each_column])))

    def clear_table(self):
        self.bg_calc_table.clear()
        self.bg_calc_table.setColumnCount(0)
        self.bg_calc_table.setRowCount(0)


    def load_optimal_cohorts(self):

        self.clear_table()

        # This is a simulated event so far

        # Creates the randomized student number
        # and randomizes how many students are in programs
        program_count = random_students()
        self.cohort_size.setText("Work in Progress")

        cohort_dict = create_cohort_dict(program_count)

        # Adding everything to tableview

        # Create Columns
        table_columns.clear()
        for programs in program_count.keys():
            table_columns.append(programs)

        self.bg_calc_table.setColumnCount(len(table_columns))
        self.bg_calc_table.setHorizontalHeaderLabels(table_columns)

        # Create Rows
        table_rows = ["Students in Program", "Amount of Cohorts", "Cohort sizes", ""]

        self.bg_calc_table.setRowCount(len(table_rows))
        self.bg_calc_table.setVerticalHeaderLabels(table_rows)

        # Enter students in program / amount of cohorts / cohort sizes
        for row in range(3):
            for program in range(len(table_columns)):
                match row:
                    case 0:
                        self.bg_calc_table.setItem(row, program, QTableWidgetItem(str(program_count[table_columns[program]])))
                    case 1:
                        self.bg_calc_table.setItem(row, program, QTableWidgetItem(str(len(cohort_dict[table_columns[program]]))))
                    case 2:
                        self.bg_calc_table.setItem(row, program, QTableWidgetItem(str(cohort_dict[table_columns[program]])))


        # Total Students
        self.bg_calc_table.setItem(3, 0, QTableWidgetItem("Total Students: " + str(sum(program_count.values()))))


