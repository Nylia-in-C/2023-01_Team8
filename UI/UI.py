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
        self.table = QTableWidget()
        # Make table unedittable
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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


        calculate = QPushButton("Calculate Optimal Cohort Size")
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


    # Settings to create the TableView
    def create_tableview(self):

        try:
            # Connect to database to get headers
            database = sqlite3.connect("database/database.db")
            cursor = database.cursor()

            # Move to cohort table
            cursor.execute("SELECT * FROM COHORT")

            self.create_db_column_headers(cursor)

            value_fill = cursor.fetchall()
            self.load_db(value_fill)

            cursor.close()
            database.close()

        except:
            print("Could not read database")


    # The following section will be for action events
    # or functions that are called repeatedly
    # after the initial startup
    def create_db_column_headers(self, cursor_obj):
        table_columns.clear()
        all_columns = cursor_obj.description
        for column_name in all_columns:
            table_columns.append(column_name[0])

        self.table.setColumnCount(len(table_columns))
        self.table.setHorizontalHeaderLabels(table_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Load data into tableview
    def load_db(self, row_data):

        self.table.setRowCount(len(row_data))
        columns = self.table.columnCount()

        for each_row in range(len(row_data)):
            for each_column in range(columns):
                 self.table.setItem(each_row, each_column, QTableWidgetItem(str(row_data[each_row][each_column])))

    def clear_table(self):
        self.table.clear()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)


    def load_optimal_cohorts(self):

        self.clear_table()

        # This is a simulated event so far

        # Creates the randomized student number
        # and randomizes how many students are in programs
        program_count = random_students()
        opt_size = get_optimal_cohort_size(program_count, CLASSROOMS)
        self.cohort_size.setText(str(opt_size))

        cohort_dict = create_cohort_dict(program_count, opt_size)

        # Adding everything to tableview

        # Create Columns
        table_columns.clear()
        for programs in program_count.keys():
            table_columns.append(programs)

        self.table.setColumnCount(len(table_columns))
        self.table.setHorizontalHeaderLabels(table_columns)

        # Create Rows
        table_rows = ["Students in Program", "Amount of Cohorts", "Cohort sizes", ""]
        all_cohorts = []
        for program in cohort_dict.keys():
            for cohort_size in cohort_dict[program]:
                new_cohort = Cohort(program, TERM_ID, cohort_size)
                table_rows.append(new_cohort.name)
                all_cohorts.append(new_cohort)

        self.table.setRowCount(len(table_rows))
        self.table.setVerticalHeaderLabels(table_rows)

        # Enter students in program / amount of cohorts / cohort sizes
        for row in range(3):
            for program in range(len(table_columns)):
                match row:
                    case 0:
                        self.table.setItem(row, program, QTableWidgetItem(str(program_count[table_columns[program]])))
                    case 1:
                        self.table.setItem(row, program, QTableWidgetItem(str(len(cohort_dict[table_columns[program]]))))
                    case 2:
                        self.table.setItem(row, program, QTableWidgetItem(str(cohort_dict[table_columns[program]])))


        # Total Students
        self.table.setItem(3, 0, QTableWidgetItem("Total Students: " + str(sum(program_count.values()))))

        # Enters cohort sizes for each course
        co_size = 0
        for each_program in range(4, len(table_rows)):
            self.table.setItem(each_program, 0, QTableWidgetItem("Cohort size: " + str(all_cohorts[co_size].count)))
            co_size+=1

