# main python file - 395 team 8

import os

import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
import database.database
from database.database import *

import imports.schedulers.core_scheduler
import datetime


BG_COLOURS = QtGui.QColor.colorNames()

LEFT_MAX_WIDTH = 450
LEC_ROOMS = []
LAB_ROOMS = []
global SCHEDULE
WEEK = 1
PREV_KEY = ""
POST_KEY = ""
global COURSE_COLOUR


# Removes colours that make the text hard to read / separate from the background
def remove_colours():
    global BG_COLOURS
    BG_COLOURS.remove("aliceblue")
    BG_COLOURS.remove("bisque")
    BG_COLOURS.remove("mediumturquoise")
    BG_COLOURS.remove("midnightblue")
    BG_COLOURS.remove("linen")
    BG_COLOURS.remove("oldlace")
    BG_COLOURS.remove("papayawhip")
    BG_COLOURS.remove("lavenderblush")
    BG_COLOURS.remove("ivory")
    BG_COLOURS.remove("blue")
    BG_COLOURS.remove("mediumblue")
    BG_COLOURS.remove("blanchedalmond")
    BG_COLOURS.remove("indigo")
    BG_COLOURS.remove("cornsilk")
    BG_COLOURS.remove("lightyellow")
    BG_COLOURS.remove("seashell")
    BG_COLOURS.remove("navy")
    BG_COLOURS.remove("black")
    BG_COLOURS.remove("brown")
    BG_COLOURS.remove("beige")
    BG_COLOURS.remove("azure")
    _colours = BG_COLOURS.copy()
    for colour in range(len(_colours)):
        if "dark" in _colours[colour] or "white" in _colours[colour] or "gray" in _colours[colour] or "grey" in _colours[colour]:
            BG_COLOURS.remove(_colours[colour])
class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        remove_colours()

        self.setWindowTitle("Scheduler")
        self.setGeometry(0,0,1240,700)

        # Create references for things that can change - filepaths, charts etc.\
        # Can add more as needed
        self.file_path = ""
        self.file_label = QLabel()
        self.legion_size = QLabel()
        self.select_room = QComboBox()
        self.week_label = QLabel()
        font = QFont()
        font.setPointSize(16)
        self.week_label.setFont(font)
        self.week_label.setAlignment(Qt.AlignCenter)


        '''
        Creating tables for each tab
        and giving proper settings (i.e. un-editable, resize to width etc)
        '''
        self.main_table = QTableWidget()

        self.main_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Make table un-editable / un-targettable
        self.main_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.main_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.main_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

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

        # Create tabs
        tabs = QTabWidget()
        tab1 = QWidget()

        tabs.addTab(tab1, "Schedule")

        self.create_schedule_base()

        week_choose = QHBoxLayout(self)

        left = QPushButton("<--")
        right = QPushButton("-->")
        right.clicked.connect(self.forward_week)
        left.clicked.connect(self.back_week)

        week_choose.addWidget(left)
        week_choose.addWidget(self.week_label)
        week_choose.addWidget(right)

        main_table_box.addLayout(week_choose)
        main_table_box.addWidget(self.main_table)

        tab1.setLayout(main_table_box)

        return tabs

    # Make the basic layout of the schedule table

    def create_schedule_base(self):

        days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        times = []

        # Creation of all times from 8:00 AM to 5:00 PM to use as row headers

        first_time = datetime.datetime(year=2000, month=1, day=1, hour=8, minute=00)
        time_dif = datetime.timedelta(minutes=30)

        times.append(first_time.strftime("%I:%M %p"))
        new_time = first_time + time_dif
        for half_hour in range(18):
            times.append(new_time.strftime("%I:%M %p"))
            new_time = new_time + time_dif

        self.main_table.setColumnCount(4)
        self.main_table.setHorizontalHeaderLabels(days)

        self.main_table.setRowCount(len(times))
        self.main_table.setVerticalHeaderLabels(times)

        self.main_table.setShowGrid(False)

        # Fill with empty items to change background colours later
        self.reset_table()


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

        create_sched = QPushButton("Create Schedule")
        create_sched.clicked.connect(self.create_schedule)

        #TODO Currently reading from the schedulers dummy values. Need to change to read from database, shouldnt be too much.

        for rooms in range(len(imports.schedulers.core_scheduler.lecture_rooms)):
            LEC_ROOMS.append(imports.schedulers.core_scheduler.lecture_rooms[rooms].ID + " Capacity: " + str(imports.schedulers.core_scheduler.lecture_rooms[rooms].capacity))
        for rooms in range(len(imports.schedulers.core_scheduler.lab_rooms)):
            LAB_ROOMS.append(imports.schedulers.core_scheduler.lab_rooms[rooms].ID + " (LAB) " + "Capacity: " + str(imports.schedulers.core_scheduler.lab_rooms[rooms].capacity))

        self.select_room.addItems(LEC_ROOMS)
        self.select_room.addItems(LAB_ROOMS)

        vbox.addWidget(title)
        vbox.addWidget(self.create_horizontal_line())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addWidget(input_title)
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(self.legion_inputs())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addWidget(self.create_horizontal_line())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(self.create_file_choose())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addWidget(self.create_horizontal_line())
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addWidget(create_sched)
        vbox.addWidget(self.select_room)

        width_limit.setLayout(vbox)

        return width_limit

    # create the file choose layout / widgets
    def create_file_choose(self):

        vbox = QVBoxLayout()

        hbox_file_choose = QHBoxLayout(self)
        choose_input_button = QPushButton("Choose File", self)
        choose_input_button.setMaximumWidth(100)
        choose_input_button.clicked.connect(self.choose_file)

        self.file_label.setText("No File Chosen")
        self.file_label.setMaximumWidth(LEFT_MAX_WIDTH)

        hbox_file_choose.addWidget(choose_input_button)
        hbox_file_choose.addWidget(self.file_label)

        load_data = QPushButton("Load Data")
        load_data.clicked.connect(self.load_student_numbers)

        create_template_button = QPushButton("Create Template")
        create_template_button.clicked.connect(self.create_template)

        vbox.addLayout(hbox_file_choose)
        vbox.addWidget(load_data)
        vbox.addWidget(create_template_button)

        return vbox



    # Makes layout for the term input section
    def legion_inputs(self):
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
        vbox_labels.addWidget(QLabel("PCOM"))
        vbox_labels.addWidget(QLabel("BCOM"))
        vbox_labels.addWidget(QLabel("PM"))
        vbox_labels.addWidget(QLabel("BA"))
        vbox_labels.addWidget(QLabel("GLM"))
        vbox_labels.addWidget(QLabel("FS"))
        vbox_labels.addWidget(QLabel("DXD"))
        vbox_labels.addWidget(QLabel("BKC"))
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

    '''
    Helper Functions

    # The following section will be for action events
    # or functions that are called repeatedly
    # after the initial startup
    '''

    def reset_table(self):
        # Use this to populate table with values to allow
        # Background colouring

        rows = self.main_table.rowCount()
        columns = self.main_table.columnCount()

        for row in range(rows):
            for column in range(columns):
                placeholder = QTableWidgetItem()
                placeholder.setTextAlignment(Qt.AlignCenter)
                #placeholder.setBackground(QtGui.QColor("lightGray"))
                placeholder.setBackground(QtGui.QColor('#fff2e6'))
                self.main_table.setItem(row, column, placeholder)

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


    # This function will store the input values
    # into the database, after calling the create legions
    # functions
    #TODO: Not used atm, must be implemented
    def store_legions(self):
        db = r".\database\database.db"  # database.db file path
        conn = create_connection(db)

        programs = ["PCOM", "BCOM" , "PM",  "BA",  "GLM",  "FS" , "DXD",  "BKC"]

        #TODO Need to get the legions made to parse the numbers to add to db
        # Anything with a '/' is what needs to be obtained

        # for each_field in range(8):
        #
        #     self.term_1_inputs.itemAt(each_field).widget().value()
        #     # Calculate legions here
        #     for each_legion in range(/legions):
        #         database.database.addLegionItem(conn, programs[each_field], 1, /legion_num )
        #
        #     self.term_2_inputs.itemAt(each_field).widget().value()
        #     for each_legion in range( / legions):
        #         database.database.addLegionItem(conn, programs[each_field], 2, /legion_num)
        #
        #     self.term_3_inputs.itemAt(each_field).widget().value()
        #     for each_legion in range( / legions):
        #         database.database.addLegionItem(conn, programs[each_field], 3, /legion_num)

        close_connection(conn)



    # weekday is 0 or 2, depending on if its monday or wednesday respectively
    # eventually 1 and 3 for tuesday, thursday
    def show_schedule(self, pd_dataframe, weekday):

        course = ""

        colour_index = -1

        day_list = pd_dataframe.tolist()

        for cell in range(self.main_table.rowCount()):

            if day_list[cell] == "":
                continue
            elif day_list[cell] != "" and course == day_list[cell]:
                self.main_table.item(cell,weekday).setBackground(QtGui.QColor(COURSE_COLOUR[course]))
            else:
                course = day_list[cell]
                if course not in COURSE_COLOUR.keys():
                    colour_index += 1
                    COURSE_COLOUR[course] = BG_COLOURS[colour_index]
                self.main_table.item(cell, weekday).setText(day_list[cell])
                self.main_table.item(cell, weekday).setBackground(QtGui.QColor(COURSE_COLOUR[course]))


    '''
    Action Event functions
    '''

    def back_week(self):
        global SCHEDULE
        global WEEK
        global PREV_KEY
        global POST_KEY
        global COURSE_COLOUR
        COURSE_COLOUR = {}

        # Only 13 weeks in a semester
        if WEEK == 1:
            return
        WEEK -= 1

        room_requested = self.select_room.currentText().split(" ")[0]
        if (self.select_room.currentText().split(" ")[1] == "(LAB)"):
            room_requested = room_requested + " (LAB)"

        self.reset_table()

        try:
            # Find the next day that the schedule changes.
            # When accessing from dataframe, odd is monday, even, wednesday

            day = (WEEK * 2)  # day will be the wednesday of the previous week
            while not isinstance(SCHEDULE["day " + str(day)], pd.DataFrame):

                # If R != 0, then go to the previous week
                if day % 2 != 0:
                    WEEK -= 1
                    day = (WEEK * 2)

                day -= 1

            self.week_label.setText("Week " + str(WEEK))

            PREV_KEY = "day " + str(day)
            if day % 2 != 0:
                # If the change day is monday
                # wednesday stays the same, monday changes
                self.show_schedule(SCHEDULE[PREV_KEY][room_requested], 0)
                self.show_schedule(SCHEDULE[PREV_KEY][room_requested], 2)

            elif day % 2 == 0 and isinstance(SCHEDULE["day " + str(day - 1)], pd.DataFrame):
                # Change on wednesday and monday
                POST_KEY = PREV_KEY
                PREV_KEY = "day " + str(day - 1)
                self.show_schedule(SCHEDULE[PREV_KEY][room_requested], 0)
                self.show_schedule(SCHEDULE[POST_KEY][room_requested], 2)
            else:
                # Change happens on a Wednesday
                POST_KEY = PREV_KEY

                # Find the next previous change
                _day = day - 1
                _week = WEEK
                while not isinstance(SCHEDULE["day " + str(_day)], pd.DataFrame):
                    if _day % 2 != 0:
                        _week -= 1
                        _day = (_week * 2)

                    _day -= 1

                PREV_KEY = "day " + str(_day)
                self.show_schedule(SCHEDULE[PREV_KEY][room_requested], 0)
                self.show_schedule(SCHEDULE[POST_KEY][room_requested], 2)
                PREV_KEY = POST_KEY

            POST_KEY = PREV_KEY
        except:
            print("error")
    def forward_week(self):
        global SCHEDULE
        global WEEK
        global PREV_KEY
        global POST_KEY
        global COURSE_COLOUR
        COURSE_COLOUR = {}


        # Only 13 weeks in a semester
        if WEEK == 13:
            return
        WEEK += 1

        room_requested = self.select_room.currentText().split(" ")[0]
        if (self.select_room.currentText().split(" ")[1] == "(LAB)"):
            room_requested = room_requested + " (LAB)"

        self.reset_table()

        try:
            # Find the next day that the schedule changes.
            # When accessing from dataframe, odd is monday, even, wednesday

            day = (WEEK*2) - 1    # day will be the monday of the next week
            while not isinstance(SCHEDULE["day " + str(day)], pd.DataFrame):

                # If R = 0, then go to the next week
                if day % 2 == 0:
                    WEEK += 1
                    day = (WEEK*2) - 2

                day += 1

            self.week_label.setText("Week " + str(WEEK))

            POST_KEY = "day " + str(day)
            if day % 2 == 0:
                # If the change day is wednesday
                # Monday stays the same, wednesday changes
                self.show_schedule(SCHEDULE[PREV_KEY][room_requested], 0)
                self.show_schedule(SCHEDULE[POST_KEY][room_requested], 2)

            elif day % 2 != 0 and isinstance(SCHEDULE["day " + str(day + 1)], pd.DataFrame):
                # Change on monday and wednesday
                PREV_KEY = POST_KEY
                POST_KEY = "day " + str(day + 1)
                self.show_schedule(SCHEDULE[PREV_KEY][room_requested], 0)
                self.show_schedule(SCHEDULE[POST_KEY][room_requested], 2)
            else:
                # Change happens on a monday
                self.show_schedule(SCHEDULE[POST_KEY][room_requested], 0)
                self.show_schedule(SCHEDULE[POST_KEY][room_requested], 2)

            PREV_KEY = POST_KEY
        except:
            print("error")



    def create_schedule(self):
        room_requested = self.select_room.currentText().split(" ")[0]
        self.week_label.setText("Week 1")
        global WEEK
        WEEK = 1

        if (self.select_room.currentText().split(" ")[1] == "(LAB)"):
            room_requested = room_requested + " (LAB)"

        # Clear any values from the table
        # Fresh Start

        self.reset_table()

        # Call upon the schedule creation functions, hopefully will
        # be able to just read from the database eventually.

        lectures = [course for course in imports.schedulers.core_scheduler.term_courses[1] if course not in imports.schedulers.core_scheduler.lab_courses]
        labs = [course for course in imports.schedulers.core_scheduler.term_courses[1] if course in imports.schedulers.core_scheduler.lab_courses]

        lec_hours, lab_hours = imports.schedulers.core_scheduler.get_course_hours(lectures, labs)
        global SCHEDULE
        SCHEDULE = imports.schedulers.core_scheduler.create_term_schedule(lec_hours, lectures, imports.schedulers.core_scheduler.lecture_rooms, lab_hours, labs, imports.schedulers.core_scheduler.lab_rooms)

        global PREV_KEY
        PREV_KEY = "day 1"

        # Note: Schedule is form of - schedule[day #][room]
        # Be advised that if [day #] is an even number
        # That is monday, odd numbers are wednesday

        # Note: If schedule at a specific day is empty, that means it hasn't changed from the last
        # day. Only days with dataframe objects indicate a change.

        # This dictionary will hold the course name (key)
        # and the colour (value) for easier distinction between same courses, and different ones
        global COURSE_COLOUR
        COURSE_COLOUR = {}

        self.show_schedule(SCHEDULE[PREV_KEY][room_requested], 0)
        if isinstance(SCHEDULE["day 2"], pd.DataFrame):
            self.show_schedule(SCHEDULE["day 2"][room_requested], 2)
        else:
            self.show_schedule(SCHEDULE[PREV_KEY][room_requested], 2)






    # Action event for creating template file
    def create_template(self):

        template = Workbook()

        sheet = template.active
        sheet.title = "Student Numbers"

        fields = ["Term", "Program", "Students"]

        sheet.append(fields)

        programs = ["PCOM", "BCOM", "PM", "BA", "GLM", "FS", "DXD", "BKC"]

        for term in range (1, 4):
            for program in range(len(programs)):
                sheet.append([term, programs[program], 0])

        template.save("Student_Number_Inputs_Template.xlsx")
        template.close()


    # Action event for the choose file button
    def choose_file(self):

        chosen_file = QFileDialog.getOpenFileName(
            self,
            "Choose a file",
            os.getcwd(),
            "Excel Workbook files (*.xlsx)"  # Filters to specified file types
        )
        if chosen_file[0] == "":
            self.file_label.setText("No File Chosen")
            self.file_path = ""
        else:
            self.file_path = chosen_file[0]
            tokens = chosen_file[0].split("/")
            self.file_label.setText(tokens[-1])

    # Action event to load student input numbers
    def load_student_numbers(self):

        try:
            stu_numbers = load_workbook(filename=self.file_path)

            try:
                sheet = stu_numbers.active
                term_1 = sheet["C2":"C9"]
                term_2 = sheet["C10":"C17"]
                term_3 = sheet["C18":"C25"]

                for each_field in range(self.term_1_inputs.count()):
                    self.term_1_inputs.itemAt(each_field).widget().setValue(term_1[each_field][0].value)

                for each_field in range(self.term_2_inputs.count()):
                    self.term_2_inputs.itemAt(each_field).widget().setValue(term_2[each_field][0].value)

                for each_field in range(self.term_3_inputs.count()):
                    self.term_3_inputs.itemAt(each_field).widget().setValue(term_3[each_field][0].value)

                stu_numbers.close()

            except:
                print("Error reading values")  # add error message here eventually

        except:
            print("Error Opening File")# Maybe put an actual error message here eventually about opening files
