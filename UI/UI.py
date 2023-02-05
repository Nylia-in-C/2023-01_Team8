# main python file - 395 team 8

import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from imports.create_cohorts import *

table_columns = []
LEFT_MAX_WIDTH = 450

class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scheduler")
        self.setGeometry(0,0,1240,700)

        # Create references for things that can change - filepaths, charts etc.\
        # Can add more as needed
        self.file_path = ""
        self.file_label = QLabel()
        self.cohort_size = QLabel()


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

        '''
        Layouts containing the term inputs
        for easier iteration when reading inputs
        '''
        self.term_1_inputs = QVBoxLayout()
        self.term_2_inputs = QVBoxLayout()
        self.term_3_inputs = QVBoxLayout()

        central_widget = QWidget()  # Must have central widget set
        central_widget.setLayout(self.create_hlayout())

        self.setCentralWidget(central_widget)

        self.show()

    # Creates all items for central widget
    def create_hlayout(self):
        hbox = QHBoxLayout(self)
        right_box = self.create_tabs()
        left_vbox = self.create_leftlayout()

        # Add layouts to overall area
        hbox.addWidget(left_vbox)
        hbox.addWidget(right_box)

        hbox.setAlignment(left_vbox, Qt.AlignTop)

        return hbox

    # Quick function to make horizontal separators
    def create_horizontal_line(self):
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setLineWidth(1)
        return h_line


    # Creates the top hbox where most information will be displayed
    def create_tabs(self):
        main_table_box = QVBoxLayout(self)
        cohort_calc_box = QVBoxLayout(self)

        # Create tabs
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()


        tabs.addTab(tab1, "Main")
        tabs.addTab(tab2, "Cohort Calculations")

        main_table_box.addWidget(self.main_table)
        cohort_calc_box.addWidget(self.bg_calc_table)

        tab1.setLayout(main_table_box)
        tab2.setLayout(cohort_calc_box)

        return tabs

    # Creates the bottom layout where most user interaction takes place
    def create_leftlayout(self):

        width_limit = QWidget()
        width_limit.setMaximumWidth(LEFT_MAX_WIDTH)

        vbox = QVBoxLayout(self)
        vbox.setSizeConstraint(QLayout.SetFixedSize) # Prevents left side from resizing

        title = QLabel("Scheduler")
        title.setMaximumWidth(LEFT_MAX_WIDTH)
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        title.setFont(font)

        input_title = QLabel("Students per Term")
        input_title.setMaximumWidth(LEFT_MAX_WIDTH)
        font.setPointSize(12)
        input_title.setFont(font)

        vbox.addWidget(title)
        vbox.addWidget(self.create_horizontal_line())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addWidget(input_title)
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(self.cohort_inputs())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addWidget(self.create_horizontal_line())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(self.create_file_choose())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addWidget(self.create_horizontal_line())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(self.calc_cohort())

        width_limit.setLayout(vbox)

        return width_limit

    # create the file choose layout / widgets
    def create_file_choose(self):

        hbox_file_choose = QHBoxLayout(self)
        choose_input_button = QPushButton("Choose File", self)
        choose_input_button.setMaximumWidth(100)
        choose_input_button.clicked.connect(self.choose_file)

        self.file_label.setText("No File Chosen")
        self.file_label.setMaximumWidth(LEFT_MAX_WIDTH)

        hbox_file_choose.addWidget(choose_input_button)
        hbox_file_choose.addWidget(self.file_label)
        return hbox_file_choose



    # Makes layout for the term input section
    def cohort_inputs(self):
        vbox_all = QVBoxLayout()

        hbox_inputs = QHBoxLayout()

        hbox_inputs.addLayout(self.program_labels())
        hbox_inputs.addLayout(self.create_term1_inputs())
        hbox_inputs.addLayout(self.create_term2_inputs())
        hbox_inputs.addLayout(self.create_term3_inputs())

        vbox_all.addLayout(hbox_inputs)

        return vbox_all


    def stu_num_input(self):
        input_box = QSpinBox()
        input_box.setMaximum(1000)
        input_box.setMinimumWidth(50)
        return input_box

    def program_labels(self):
        vbox_labels = QVBoxLayout()

        vbox_labels.addWidget(QLabel())
        vbox_labels.addWidget(QLabel("PCOM Students"))
        vbox_labels.addWidget(QLabel("BCOM Students"))
        vbox_labels.addWidget(QLabel("PM Students"))
        vbox_labels.addWidget(QLabel("BA Students"))
        vbox_labels.addWidget(QLabel("GLM Students"))
        vbox_labels.addWidget(QLabel("FS Students"))
        vbox_labels.addWidget(QLabel("DXD Students"))
        vbox_labels.addWidget(QLabel("BKC Students"))
        return vbox_labels
    def create_term1_inputs(self):


        '''
        self.term_1_inputs holds all the fields here
        '''
        vbox = QVBoxLayout()

        self.term_1_inputs.addWidget(self.stu_num_input())
        self.term_1_inputs.addWidget(self.stu_num_input())
        self.term_1_inputs.addWidget(self.stu_num_input())
        self.term_1_inputs.addWidget(self.stu_num_input())
        self.term_1_inputs.addWidget(self.stu_num_input())
        self.term_1_inputs.addWidget(self.stu_num_input())
        self.term_1_inputs.addWidget(self.stu_num_input())
        self.term_1_inputs.addWidget(self.stu_num_input())

        self.term_1_inputs.setAlignment(Qt.AlignLeft)

        vbox.addWidget(QLabel("Term 1"))
        vbox.addLayout(self.term_1_inputs)

        return vbox
    
    def create_term2_inputs(self):


        '''
        self.term_2_inputs holds all the fields here
        '''
        vbox = QVBoxLayout()

        self.term_2_inputs.addWidget(self.stu_num_input())
        self.term_2_inputs.addWidget(self.stu_num_input())
        self.term_2_inputs.addWidget(self.stu_num_input())
        self.term_2_inputs.addWidget(self.stu_num_input())
        self.term_2_inputs.addWidget(self.stu_num_input())
        self.term_2_inputs.addWidget(self.stu_num_input())
        self.term_2_inputs.addWidget(self.stu_num_input())
        self.term_2_inputs.addWidget(self.stu_num_input())

        self.term_2_inputs.setAlignment(Qt.AlignLeft)

        vbox.addWidget(QLabel("Term 2"))
        vbox.addLayout(self.term_2_inputs)

        return vbox

    def create_term3_inputs(self):


        '''
        self.term_2_inputs holds all the fields here
        '''
        vbox = QVBoxLayout()

        self.term_3_inputs.addWidget(self.stu_num_input())
        self.term_3_inputs.addWidget(self.stu_num_input())
        self.term_3_inputs.addWidget(self.stu_num_input())
        self.term_3_inputs.addWidget(self.stu_num_input())
        self.term_3_inputs.addWidget(self.stu_num_input())
        self.term_3_inputs.addWidget(self.stu_num_input())
        self.term_3_inputs.addWidget(self.stu_num_input())
        self.term_3_inputs.addWidget(self.stu_num_input())

        self.term_3_inputs.setAlignment(Qt.AlignLeft)

        vbox.addWidget(QLabel("Term 3"))
        vbox.addLayout(self.term_3_inputs)

        return vbox

    def calc_cohort(self):
        hbox_info = QHBoxLayout()

        label = QLabel("Optimal Cohort Size:")
        label.setFont(QFont("Times", 10))
        label.setMaximumWidth(150)

        self.cohort_size.setFont(QFont("Times", 10))
        self.cohort_size.setMaximumWidth(100)


        calculate = QPushButton("Calculate Cohort Sizes")
        calculate.clicked.connect(self.load_optimal_cohorts)

        hbox_info.addWidget(calculate)
        hbox_info.addWidget(label)
        hbox_info.addWidget(self.cohort_size)

        return hbox_info

    '''
    Helper Functions

    # The following section will be for action events
    # or functions that are called repeatedly
    # after the initial startup
    '''
    def retrieve_term_inputs(self, layout):

        '''
        Used to read values from the term input fields.
        Will return a list of the inputs
        Always in the order of:
        PCOM
        BCOM
        PM
        BA
        GLM
        FS
        DXD
        BKC
        '''
        input_fields = layout.count()

        for each_field in range(input_fields):
            print(layout.itemAt(each_field).widget().value())

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


    '''
    Table Clearing functions
    '''
    def clear_bg_table(self):
        self.bg_calc_table.clear()
        self.bg_calc_table.setColumnCount(0)
        self.bg_calc_table.setRowCount(0)

    def clear_main_table(self):
        self.main_table.clear()
        self.main_table.setColumnCount(0)
        self.main_table.setRowCount(0)


    '''
    Action Event functions
    '''

    def load_optimal_cohorts(self):

        self.clear_bg_table()

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