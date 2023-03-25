# main python file - 395 team 8

#Imports
import os
import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
import random
import database.database
from database.database import *
import imports.fillClassrooms

import imports.schedulers.initialize_data
import imports.schedulers.core_scheduler
import imports.classes.classrooms
import datetime


BG_COLOURS = QtGui.QColor.colorNames()

SEM = {"Fall":1, "Winter":2, "Spring / Summer":3}

LEFT_MAX_WIDTH = 450
global CORE_SCHEDULE
global PROG_SCHEDULE
global PROG_LABELS
WEEK = 1
CORE_PREV = ""
CORE_POST = ""
PROG_PREV = ""
PROG_POST = ""
COLOUR_INDEX = -1
global COURSE_COLOUR


# Removes colours that make the text hard to read / separate from the background
def remove_colours():
    global BG_COLOURS
    excludedcolours = ["aliceblue", "mediumturquoise", "midnightblue", 
                    "lavenderblush", "blue", "mediumblue", "blanchedalmond", 
                    "indigo", "seashell", "navy", "black", "brown", "beige",
                    "azure", "deeppink", "fuchsia", "hotpink", "magenta",
                    "red", "pink", "mediumvioletred"]

    for colour in excludedcolours:
        BG_COLOURS.remove(colour)

    _colours = BG_COLOURS.copy()
    for colour in range(len(_colours)):
        if "dark" in _colours[colour] or "white" in _colours[colour] or "gray" in _colours[colour] or "grey" in _colours[colour]:
            BG_COLOURS.remove(_colours[colour])

class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        remove_colours()

        self.setWindowTitle("Scheduler")
        self.setFixedSize(1240, 850)

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
        self.pick_semester = QComboBox()
        self.pick_semester.addItems(list(SEM.keys()))

        # Options
        self.class_id = QLineEdit()
        self.class_lab = QButtonGroup()
        self.class_capacity = QSpinBox()
        self.classroom_list = QComboBox()

        self.courses = QComboBox()
        self.courses_edit_new = QButtonGroup()
        self.course_id = QLineEdit()
        self.course_term_hours = QSpinBox()
        self.course_term = QSpinBox()
        self.course_duration = QSpinBox()
        self.course_core = QCheckBox()
        self.course_online = QCheckBox()
        self.course_lab = QCheckBox()

        self.course_pre_req_selector = QComboBox()
        self.course_pre_reqs = []
        self.course_pre_reqs_label = QLabel()


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

    # Quick function to make horizontal separators
    def create_vertical_line(self):
        v_line = QFrame()
        v_line.setFrameShape(QFrame.VLine)
        v_line.setLineWidth(1)
        return v_line

    # Creates the top hbox where most information will be displayed
    def create_tabs(self):

        # Create tabs
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        tabs.addTab(tab1, "Schedule")
        tabs.addTab(tab2, "Options")
        tabs.addTab(tab3, "Instructions")

        self.create_schedule_base()

        tab1.setLayout(self.make_main_tab())
        tab2.setLayout(self.make_options_tab())

        # Read me Doc
        read_me = QTextEdit()
        file_content = open("README.md").read()
        read_me.setMarkdown(file_content)
        layout = QHBoxLayout()
        layout.addWidget(read_me)
        tab3.setLayout(layout)

        return tabs

    def make_main_tab(self):
        main_table_box = QVBoxLayout(self)
        week_choose = QHBoxLayout(self)

        #Left/Right Navigation Arrows
        arrowfont = QFont()
        arrowfont.setBold(True)
        arrowfont.setPointSize(20)
        left = QPushButton("←")
        left.setFont(arrowfont)
        right = QPushButton("→")
        right.setFont(arrowfont)

        right.clicked.connect(self.forward_week)
        left.clicked.connect(self.back_week)

        week_choose.addWidget(left)
        week_choose.addWidget(self.week_label)
        week_choose.addWidget(right)

        main_table_box.addLayout(week_choose)
        main_table_box.addWidget(self.main_table)

        return main_table_box

    def make_options_tab(self):
        vbox_overall = QVBoxLayout()

        vbox_overall.addLayout(self.update_classroom_section())
        vbox_overall.addWidget(self.create_horizontal_line())
        vbox_overall.addWidget(self.create_horizontal_line())
        vbox_overall.addLayout(self.update_course_section())


        return vbox_overall

    def update_classroom_section(self):
        room_add_layout = QHBoxLayout()
        room_add_layout.setSpacing(15)

        room_delete_layout = QHBoxLayout()
        room_delete_layout.setSpacing(15)

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)

        subfont = QFont()
        subfont.setBold(True)
        subfont.setItalic(True)
        subfont.setPointSize(14)

        # Classroom section
        vbox_class = QVBoxLayout()
        vbox_class.setContentsMargins(20,0,0,0)
        class_section_text = QLabel("Room Options")
        class_section_text.setFont(font)

        #Header
        vbox_class.addWidget(class_section_text)
        vbox_class.addWidget(self.create_horizontal_line())

        #Adding a Room Subheader
        class_add_text = QLabel("Add New Room")
        class_add_text.setFont(subfont)
        vbox_class.addWidget(class_add_text)

        # Class ID section
        self.class_id.setPlaceholderText("Classroom Name")
        class_id_box = QHBoxLayout()
        class_id_box.addWidget(QLabel("Room ID"))
        #self.class_id.setMaximumWidth(100)
        class_id_box.addWidget(self.class_id)

        # Class Capacity Section
        class_capacity_box = QHBoxLayout()
        class_capacity_box.addWidget(QLabel("Room Capacity"))
        self.class_capacity.setValue(10)
        self.class_capacity.setMinimum(10)
        self.class_capacity.setMaximum(50)
        self.class_capacity.setMaximumWidth(100)
        class_capacity_box.addWidget(self.class_capacity)

        # Class Lab/Lecture section
        class_lab_bool = QHBoxLayout()
        b1 = QRadioButton("Lab")
        b1.setChecked(True)
        b2 = QRadioButton("Lecture")
        self.class_lab.addButton(b1)
        self.class_lab.addButton(b2)

        class_lab_bool.addWidget(QLabel("Room Type"))
        class_lab_bool.addWidget(b1)
        class_lab_bool.addWidget(b2)

        # Create add button
        class_btn = QPushButton("Add")
        class_btn.setMaximumWidth(100)
        class_btn.clicked.connect(self.add_edit_classroom)

        # Put adding functions into the layout
        room_add_layout.addLayout(class_id_box)
        room_add_layout.addWidget(self.create_vertical_line())
        room_add_layout.addLayout(class_capacity_box)
        room_add_layout.addWidget(self.create_vertical_line())
        room_add_layout.addLayout(class_lab_bool)
        room_add_layout.addWidget(class_btn)
        room_add_layout.addWidget(self.create_vertical_line())
        
        #Deleting a Room

        #Delete Room Header
        class_delete_text = QLabel("Delete Room")
        class_delete_text.setFont(subfont)

        # Create remove button
        remove_btn = QPushButton("Remove")
        remove_btn.setMaximumWidth(150)
        remove_btn.clicked.connect(self.remove_classroom)

        remove_section = QHBoxLayout()
        remove_section.addWidget(self.classroom_list)
        remove_section.addWidget(remove_btn)

        # Put deleting functions into layout
        room_delete_layout.addLayout(remove_section)
        room_delete_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum))

        #Add sublayouts to big vbox_class object
        vbox_class.addLayout(room_add_layout)
        vbox_class.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Minimum))

        vbox_class.addWidget(class_delete_text)

        vbox_class.addLayout(room_delete_layout)
        vbox_class.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Minimum))
        
        return vbox_class

    def update_course_section(self):
        vbox_course = QVBoxLayout()
        vbox_course.setContentsMargins(20,0,0,0)

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)

        course_section_text = QLabel("Course Options")
        course_section_text.setFont(font)
        
        vbox_course.addWidget(course_section_text)
        vbox_course.addWidget(self.create_horizontal_line())


        db = r".\database\database.db"  # database.db file path
        connection = create_connection(db)
        db_courses = readCourseItem(connection, "%")
        close_connection(connection)

        course_name_list = []

        for each_course in range(len(db_courses)):
            course_name_list.append(db_courses[each_course][0])

        self.courses.addItems(course_name_list)
        self.courses.setMaximumWidth(200)
        self.course_pre_req_selector.addItems(course_name_list)

        # Creating inputs
        hbox = QHBoxLayout()

        new_or_edit = QVBoxLayout()
        b1 = QRadioButton("New Course")
        b1.setChecked(True)
        b2 = QRadioButton("Edit Course")
        self.courses_edit_new.addButton(b1)
        self.courses_edit_new.addButton(b2)

        new_or_edit.addWidget(QLabel("Edit?"))
        new_or_edit.addWidget(b1)
        new_or_edit.addWidget(b2)
        #-----------------------------

        course_id_sec = QVBoxLayout()
        course_id_sec.addWidget(QLabel("Course Name"))
        self.courses_edit_new.buttonClicked.connect(self.show_hide_course)
        self.course_id.setMaximumWidth(100)
        course_id_sec.addWidget(self.courses)
        course_id_sec.addWidget(self.course_id)
        self.courses.hide()

        # ---------------------------

        vbox_spin_boxes = QVBoxLayout()
        hbox_hours = QHBoxLayout()
        hbox_hours.addWidget(QLabel("Course Hours: "))
        hbox_hours.addWidget(self.course_term_hours)

        hbox_term = QHBoxLayout()
        hbox_term.addWidget(QLabel("Term: "))
        hbox_term.addWidget(self.course_term)

        hbox_duration = QHBoxLayout()
        hbox_duration.addWidget(QLabel("Duration: "))
        hbox_duration.addWidget(self.course_duration)

        vbox_spin_boxes.addLayout(hbox_hours)
        vbox_spin_boxes.addLayout(hbox_term)
        vbox_spin_boxes.addLayout(hbox_duration)

        #--------------------------

        vbox_online_lab = QVBoxLayout()

        core_hbox = QHBoxLayout()
        core_hbox.addWidget(QLabel("Core Course: "))
        core_hbox.addWidget(self.course_core)

        online_hbox = QHBoxLayout()
        online_hbox.addWidget(QLabel("Online?: "))
        online_hbox.addWidget(self.course_online)

        hbox_lab = QHBoxLayout()
        hbox_lab.addWidget(QLabel("Has a lab?: "))
        hbox_lab.addWidget(self.course_lab)

        vbox_online_lab.addLayout(core_hbox)
        vbox_online_lab.addLayout(online_hbox)
        vbox_online_lab.addLayout(hbox_lab)
        #--------------------------

        course_btn = QPushButton("Save Course")
        course_btn.clicked.connect(self.save_course)

        # --------------------------

        hbox_pre_reqs = QHBoxLayout()
        vbox_pre_reqs = QVBoxLayout()

        hbox_pre_reqs.addWidget(QLabel("Chosen Pre-Reqs"))
        add_pre_req = QPushButton("Add Pre-Req")
        add_pre_req.clicked.connect(self.add_pre_req)
        rem_pre_req = QPushButton("Clear Pre-Reqs")
        rem_pre_req.clicked.connect(self.clear_pre_reqs)

        hbox_pre_reqs.addWidget(self.course_pre_reqs_label)
        vbox_pre_reqs.addLayout(hbox_pre_reqs)
        vbox_pre_reqs.addWidget(self.course_pre_req_selector)
        vbox_pre_reqs.addWidget(add_pre_req)
        vbox_pre_reqs.addWidget(rem_pre_req)

        #-----------------------------

        hbox.setSpacing(15)

        hbox.addLayout(new_or_edit)
        hbox.addWidget(self.create_vertical_line())
        hbox.addLayout(course_id_sec)
        hbox.addWidget(self.create_vertical_line())
        hbox.addLayout(vbox_spin_boxes)
        hbox.addWidget(self.create_vertical_line())
        hbox.addLayout(vbox_online_lab)
        hbox.addWidget(self.create_vertical_line())
        hbox.addLayout(vbox_pre_reqs)
        hbox.addWidget(self.create_vertical_line())
        hbox.addWidget(course_btn)

        #hbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum))

        vbox_course.addLayout(hbox)

        return vbox_course

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

        create_sched = QPushButton("Create Schedule")
        font.setPointSize(16)
        create_sched.setFont(font)
        create_sched.clicked.connect(self.create_schedule)

        input_title = QLabel("Students per Term")
        input_title.setMaximumWidth(LEFT_MAX_WIDTH)
        font.setPointSize(12)
        input_title.setFont(font)

        # Read Current items in teh Database
        self.update_class_combos()


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
        vbox.addWidget(self.pick_semester)
        vbox.addWidget(create_sched)
        vbox.addWidget(self.select_room)

        width_limit.setLayout(vbox)

        return width_limit

    # create the file choose layout / widgets
    def create_file_choose(self):

        vbox = QVBoxLayout()

        #Title
        title = QLabel("Enrollment Import by Program")
        title.setMaximumWidth(LEFT_MAX_WIDTH)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        title.setFont(font)

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

        vbox.addWidget(title)
        vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
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
        global PROG_LABELS
        vbox_labels = QVBoxLayout()

        vbox_labels.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)) #for alignment

        PROG_LABELS = ["PCOM", "BCOM", "PM", "BA", "GLM", "FS", "DXD", "BKC"]

        for label in PROG_LABELS:
            vbox_labels.addWidget(QLabel(label))

        return vbox_labels


    def create_term1_inputs(self):

        '''
        self.term_1_inputs holds all the fields here
        '''
        vbox = QVBoxLayout()

        for n in range(len(PROG_LABELS)):
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

        for n in range(len(PROG_LABELS)):
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

        for n in range(len(PROG_LABELS)):
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

    def update_class_combos(self):
        self.classroom_list.clear()
        self.select_room.clear()

        db = r".\database\database.db"  # database.db file path
        connection = create_connection(db)
        db_classes = readClassroomItem(connection, "%")
        close_connection(connection)

        for each_class in range(len(db_classes)):

            if db_classes[each_class][2] == 1:
                self.select_room.addItem(db_classes[each_class][0] + f" Capacity: [{db_classes[each_class][1]}] (LAB)")
                self.classroom_list.addItem(db_classes[each_class][0] + f" Capacity: [{db_classes[each_class][1]}] (LAB)")
            else:
                self.select_room.addItem(db_classes[each_class][0] + f" Capacity: [{db_classes[each_class][1]}]")
                self.classroom_list.addItem(db_classes[each_class][0] + f" Capacity: [{db_classes[each_class][1]}]")

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
                placeholder.setBackground(QtGui.QColor('#c4ddde'))
                self.main_table.setItem(row, column, placeholder)
                self.main_table.removeCellWidget(row, column)

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
        list_val = []

        for each_field in range(input_fields):
            list_val.append(layout.itemAt(each_field).widget().value())

        return list_val


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

        global COLOUR_INDEX

        course = ""

        day_list = pd_dataframe.tolist()
        font = QFont()
        font.setPointSize(11)

        for cell in range(self.main_table.rowCount()):

            if day_list[cell] == "":
                continue

            elif day_list[cell] != "" and course == day_list[cell]:
                self.main_table.item(cell,weekday).setBackground(QtGui.QColor(COURSE_COLOUR[course]))

                side_fill = QLabel()
                side_fill.setStyleSheet("border: solid black;"
                                        "border-width : 0px 2px 0px 2px;")

                if cell + 1 <= 18 and day_list[cell + 1] == "":
                    side_fill.setStyleSheet("border: solid black;"
                                            "border-width : 0px 2px 2px 2px;")
                self.main_table.setCellWidget(cell, weekday, side_fill)
            else:
                course = day_list[cell]
                label_fill = QLabel(day_list[cell])
                label_fill.setFont(font)
                label_fill.setAlignment(Qt.AlignCenter)
                label_fill.setStyleSheet("border: solid black;"
                                         "border-width : 2px 2px 0px 2px;")

                if cell + 1 <= 18 and day_list[cell + 1] != course:
                    label_fill.setStyleSheet("border: solid black;"
                                            "border-width : 0px 2px 2px 2px;")

                if course not in COURSE_COLOUR.keys():
                    COLOUR_INDEX += 1
                    if COLOUR_INDEX == len(BG_COLOURS):
                        COLOUR_INDEX = 0
                    COURSE_COLOUR[course] = BG_COLOURS[COLOUR_INDEX]
                self.main_table.setCellWidget(cell, weekday, label_fill)
                self.main_table.item(cell, weekday).setBackground(QtGui.QColor(COURSE_COLOUR[course]))


    def add_ghost_rooms(self):
        imports.fillClassrooms.fillClassrooms(SEM[self.pick_semester.currentText()])
        print(SEM[self.pick_semester.currentText()])

        db = r".\database\database.db"  # database.db file path
        connection = create_connection(db)
        if (len(readClassroomItem(connection, "ghost%")) != 0):
            QMessageBox.information(self, "Ghost Rooms", "Be advised Ghost Rooms are required.")

        close_connection(connection)

    '''
    Action Event functions
    '''

    def back_week(self):
        global CORE_SCHEDULE
        global WEEK
        global CORE_PREV
        global CORE_POST
        global PROG_PREV
        global PROG_POST

        # Only 13 weeks in a semester
        if WEEK == 1:
            return
        WEEK -= 1

        room_requested = self.select_room.currentText().split(" ")[0]
        if (len(self.select_room.currentText().split(" ")) > 1 and 
            self.select_room.currentText().split(" ")[1] == "(LAB)"):
            room_requested = room_requested + " (LAB)"

        try:
            # Find the next day that the schedule changes.
            # When accessing from dataframe, odd is monday, even, wednesday

            day = (WEEK * 2)  # day will be the wednesday / thursday of the previous week

            while not (isinstance(CORE_SCHEDULE["day " + str(day)], pd.DataFrame) or isinstance(PROG_SCHEDULE["day " + str(day)], pd.DataFrame)):

                # If R != 0, then go to the previous week
                if day % 2 != 0:
                    WEEK -= 1
                    day = (WEEK * 2)

                day -= 1

            self.week_label.setText("Week " + str(WEEK))
            self.reset_table()
            CORE_PREV = "day " + str(day)
            PROG_PREV = "day " + str(day)

            if day % 2 != 0 and isinstance(CORE_SCHEDULE[CORE_PREV], pd.DataFrame):
                # If the change day is monday and core is changing
                # wednesday stays the same, monday changes
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 0)
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 2)

            elif day % 2 == 0 and isinstance(CORE_SCHEDULE[CORE_PREV], pd.DataFrame) and isinstance(CORE_SCHEDULE["day " + str(day - 1)], pd.DataFrame):
                # Change on wednesday and monday core
                CORE_POST = CORE_PREV
                CORE_PREV = "day " + str(day - 1)
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 0)
                self.show_schedule(CORE_SCHEDULE[CORE_POST][room_requested], 2)
            elif day % 2 == 0 and isinstance(CORE_SCHEDULE["day " + str(day)], pd.DataFrame):
                # Change on wednesday, no change on monday
                CORE_POST = CORE_PREV

                # Find the next previous change
                _day = day - 1
                _week = WEEK
                while not isinstance(CORE_SCHEDULE["day " + str(_day)], pd.DataFrame):
                    if _day % 2 != 0:
                        _week -= 1
                        _day = (_week * 2)

                    _day -= 1

                CORE_PREV = "day " + str(_day)

                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 0)
                self.show_schedule(CORE_SCHEDULE[CORE_POST][room_requested], 2)
                CORE_PREV = CORE_POST

            else:
                # Change only in program (tue / thur)
                # Must find previous change
                _day = day - 1
                _week = WEEK
                while not isinstance(CORE_SCHEDULE["day " + str(_day)], pd.DataFrame):
                    if _day % 2 != 0:
                        _week -= 1
                        _day = (_week * 2)

                    _day -= 1
                CORE_PREV = "day " + str(_day)
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 0)
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 2)

            CORE_POST = CORE_PREV

            if day % 2 != 0 and isinstance(PROG_SCHEDULE[PROG_PREV], pd.DataFrame):
                # If the change day is tuesday and prog is changing
                # thursday stays the same, tuesday changes
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 1)
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 3)

            elif day % 2 == 0 and isinstance(PROG_SCHEDULE[PROG_PREV], pd.DataFrame) and isinstance(PROG_SCHEDULE["day " + str(day - 1)], pd.DataFrame):
                # Change on thursday and tuesday prog
                PROG_POST = PROG_PREV
                PROG_PREV = "day " + str(day - 1)
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 1)
                self.show_schedule(PROG_SCHEDULE[PROG_POST][room_requested], 3)
            elif day % 2 == 0 and isinstance(PROG_SCHEDULE[PROG_PREV], pd.DataFrame):
                # Change on thursday, no change on tuesday
                PROG_POST = PROG_PREV
                # Find the next previous change
                _day = day - 1
                _week = WEEK
                while not isinstance(PROG_SCHEDULE["day " + str(_day)], pd.DataFrame):
                    if _day % 2 != 0:
                        _week -= 1
                        _day = (_week * 2)

                    _day -= 1

                PROG_PREV = "day " + str(_day)

                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 1)
                self.show_schedule(PROG_SCHEDULE[PROG_POST][room_requested], 3)
                PROG_PREV = PROG_POST

            else:
                # Change only in course (mon / wed)
                # Must find previous change
                _day = day - 1
                _week = WEEK
                while not isinstance(PROG_SCHEDULE["day " + str(_day)], pd.DataFrame):
                    if _day % 2 != 0:
                        _week -= 1
                        _day = (_week * 2)

                    _day -= 1
                PROG_PREV = "day " + str(_day)
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 1)
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 3)

            PROG_POST = PROG_PREV

        except:
            print("error")
    def forward_week(self):
        global CORE_SCHEDULE
        global WEEK
        global CORE_PREV
        global CORE_POST
        global PROG_PREV
        global PROG_POST


        # Only 13 weeks in a semester
        if WEEK == 13:
            return
        WEEK += 1

        room_requested = self.select_room.currentText().split(" ")[0]
        if (len(self.select_room.currentText().split(" ")) > 1 and 
            self.select_room.currentText().split(" ")[1] == "(LAB)"):
            room_requested = room_requested + " (LAB)"

        try:
            # Find the next day that the schedule changes.
            # When accessing from dataframe, odd is monday / tuesday, even, wednesday / thursday

            day = (WEEK*2) - 1    # day will be the monday / tuesday of the next week

            while not (isinstance(CORE_SCHEDULE["day " + str(day)], pd.DataFrame) or isinstance(PROG_SCHEDULE["day " + str(day)], pd.DataFrame) ):

                # If we get to the last day of the semester (day 26) and theres no dataframe,
                # There is no more changes for the semester

                # If R = 0, then go to the next week
                if day % 2 == 0:
                    WEEK += 1
                    day = (WEEK*2) - 2

                day += 1

            self.reset_table()

            self.week_label.setText("Week " + str(WEEK))

            CORE_POST = "day " + str(day)
            PROG_POST = "day " + str(day)

            if day % 2 == 0 and isinstance(CORE_SCHEDULE[CORE_POST], pd.DataFrame):
                # If the change day is wednesday and theres a change in core
                # Monday stays the same, wednesday changes
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 0)
                self.show_schedule(CORE_SCHEDULE[CORE_POST][room_requested], 2)

            elif day % 2 != 0 and isinstance(CORE_SCHEDULE["day " + str(day + 1)], pd.DataFrame):
                # Change on monday and wednesday
                CORE_PREV = CORE_POST
                CORE_POST = "day " + str(day + 1)
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 0)
                self.show_schedule(CORE_SCHEDULE[CORE_POST][room_requested], 2)
            elif day % 2 != 0 and isinstance(CORE_SCHEDULE[CORE_POST], pd.DataFrame):
                # Change happens on a monday
                self.show_schedule(CORE_SCHEDULE[CORE_POST][room_requested], 0)
                self.show_schedule(CORE_SCHEDULE[CORE_POST][room_requested], 2)
            else:
                # Change only in program (tue / thur)
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 0)
                self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 2)
                CORE_POST = CORE_PREV


            CORE_PREV = CORE_POST

            if day % 2 == 0 and isinstance(PROG_SCHEDULE[PROG_POST], pd.DataFrame):
                # If the change day is thursday and theres a change in program
                # Tue stays the same, thur changes
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 1)
                self.show_schedule(PROG_SCHEDULE[PROG_POST][room_requested], 3)

            elif day % 2 != 0 and isinstance(PROG_SCHEDULE["day " + str(day + 1)], pd.DataFrame):
                # Change on tuesday and thursday
                PROG_PREV = PROG_POST
                PROG_POST = "day " + str(day + 1)
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 1)
                self.show_schedule(PROG_SCHEDULE[PROG_POST][room_requested], 3)
            elif day % 2 != 0 and isinstance(PROG_SCHEDULE[PROG_POST], pd.DataFrame):
                # Change happens on a tuesday
                self.show_schedule(PROG_SCHEDULE[PROG_POST][room_requested], 1)
                self.show_schedule(PROG_SCHEDULE[PROG_POST][room_requested], 3)
            else:
                # Change only in core (mon / wed)
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 1)
                self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 3)
                PROG_POST = PROG_PREV

            PROG_PREV = PROG_POST
        except:
            print("error")



    def create_schedule(self):
        # Will eventually replace create_schedule, as it will pull form the db
        room_requested = self.select_room.currentText().split(" ")[0]
        self.week_label.setText("Week 1")
        global WEEK
        WEEK = 1

        # Pass in student numbers to db
        # Then calculate ghost rooms
        # Then parse the schedule.
        self.pass_stu_num_db()
        self.add_ghost_rooms()
        self.update_class_combos()


        random.shuffle(BG_COLOURS)
        self.reset_table()

        # Retrieve lecture items for the week

        # week1 = self.get_lecture_items()

        # Create a list for each day, (26 slots) for each list to correspond for each time
        # for each_day in range(len(week1)):
        #     schedule_list = [""] * 26
        #
        #     for each_lecture in range(len(week1[each_day])):
        #         #TODO match start time of lecture to its spot in the schedule_list
        #         # Separate the cohorts within it
        #         # put them in list
        #         # Pass to show schedule function
        #         return



    def create_schedule_old(self):
        room_requested = self.select_room.currentText().split(" ")[0]
        self.week_label.setText("Week 1")
        global WEEK
        WEEK = 1


        # TODO Uncomment this if you want random colours every time you remake schedule
        random.shuffle(BG_COLOURS)

        if (len(self.select_room.currentText().split(" ")) > 1 and 
            self.select_room.currentText().split(" ")[1] == "(LAB)"):
            room_requested = room_requested + " (LAB)"

        # Clear any values from the table
        # Fresh Start

        self.reset_table()

        # Call upon the schedule creation functions, hopefully will
        # be able to just read from the database eventually.

        global CORE_SCHEDULE, PROG_SCHEDULE
        CORE_SCHEDULE  = imports.schedulers.core_scheduler.get_sched(2)
        # scheduling program-specific courses isnt implemented yet, so just use core schedules twice for UI testing -Andrew
        PROG_SCHEDULE  = CORE_SCHEDULE


        global CORE_PREV, PROG_PREV
        CORE_PREV = "day 1"
        PROG_PREV = "day 1"

        # Note: Schedule is form of - schedule[day #][room]
        # Be advised that if [day #] is an even number
        # That is monday, odd numbers are wednesday

        # 03/17/2022 Update: 
        # all 26 core course schedules are included in `CORE_SCHEDULE`, so we can get rid of all the `isinstance` checks

        # This dictionary will hold the course name (key)
        # and the colour (value) for easier distinction between same courses, and different ones
        global COURSE_COLOUR, COLOUR_INDEX
        COURSE_COLOUR = {}
        COLOUR_INDEX = -1

        self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 0)
        self.show_schedule(PROG_SCHEDULE[PROG_PREV][room_requested], 1)
        if isinstance(CORE_SCHEDULE["day 2"], pd.DataFrame):
            self.show_schedule(CORE_SCHEDULE["day 2"][room_requested], 2)
        else:
            self.show_schedule(CORE_SCHEDULE[CORE_PREV][room_requested], 2)

        if isinstance(PROG_SCHEDULE["day 2"], pd.DataFrame):
            self.show_schedule(PROG_SCHEDULE["day 2"][room_requested], 3)
        else:
            self.show_schedule(PROG_SCHEDULE[CORE_PREV][room_requested], 3)






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

                #----------------------------------------
                # Template excel. Term, Program, Students
                if sheet["A1"].value == "Term": 
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

                #----------------------------------------
                # Client requested excel. Student ID, Student Name, Program, Term
                elif sheet["A1"].value == "Student ID":
                    i = 2

                    program_counts = {"PCOM1": 0, "PCOM2": 0, "PCOM3": 0,
                                      "BCOM1": 0, "BCOM2": 0, "BCOM3": 0,
                                      "PM1":   0, "PM2":   0, "PM3":   0,
                                      "BA1":   0, "BA2":   0, "BA3":   0,
                                      "GLM1":  0, "GLM2":  0, "GLM3":  0,
                                      "FS1":   0, "FS2":   0, "FS3":   0,
                                      "DXD1":  0, "DXD2":  0, "DXD3":  0,
                                      "BKC1":  0, "BKC2":  0, "BKC3":  0}

                    while sheet[f"A{i}"].value:

                        program  = sheet[f"C{i}"].value
                        term = str(sheet[f"D{i}"].value)
                        
                        program_counts[program + term] += 1

                        i += 1

                    keys = list(program_counts.keys())
                    for i in range(self.term_1_inputs.count()):
                        self.term_1_inputs.itemAt(i).widget().setValue(program_counts[keys[3*i + 0]])

                    for i in range(self.term_2_inputs.count()):
                        self.term_2_inputs.itemAt(i).widget().setValue(program_counts[keys[3*i + 1]])

                    for i in range(self.term_3_inputs.count()):
                        self.term_3_inputs.itemAt(i).widget().setValue(program_counts[keys[3*i + 2]])
                    """
                    program = ''
                    term = 0
                    count = 0
                    while not sheet[f"A{i}"].value == "":
                        if program == '' and term == 0:
                            program = sheet[f"C{i}"].value
                            term    = int(sheet[f"D{i}"].value)

                        elif not (program == sheet[f"C{i}"] and term == sheet[f"D{i}"]):
                            # Add value to textbox
                            x = 'donothing'

                            program = sheet[f"C{i}"].value
                            term    = int(sheet[f"D{i}"].value)
                            count = 1
                        
                        else: count += 1
                    """

                
                else: print("Bad template!")

            except:
                print("Error reading values")  # add error message here eventually

        except:
            print("Error Opening File")# Maybe put an actual error message here eventually about opening files


    def pass_stu_num_db(self):

        term_1 = self.retrieve_term_inputs(self.term_1_inputs)
        term_2 = self.retrieve_term_inputs(self.term_2_inputs)
        term_3 = self.retrieve_term_inputs(self.term_3_inputs)

        programs = ["PCOM", "BCOM", "PM", "BA", "GLM", "FS", "DXD", "BKC"]

        try:
            db = r".\database\database.db"  # database.db file path
            connection = create_connection(db)

            # Takes the currently input numbers, and adds them to the DB.
            for each_input in range(8):

                addStudentItem(connection, programs[each_input], 1, term_1[each_input])
                addStudentItem(connection, programs[each_input], 2, term_2[each_input])
                addStudentItem(connection, programs[each_input], 3, term_3[each_input])

            close_connection(connection)

        except:
            print("Could not read database")
            close_connection(connection)

        return

    def get_lecture_items(self):
        #TODO see if easy to change to search by week / class

        db = r".\database\database.db"  # database.db file path
        connection = create_connection(db)
        lectures_each_day = []

        for each_day in range(4):
            lectures_each_day.append(database.database.readLectureItem(connection))

        close_connection(connection)

        return lectures_each_day

    def add_edit_classroom(self):
        db = r".\database\database.db"  # database.db file path
        connection = create_connection(db)

        try:

            # Adds a classroom if it does not exist in database currently.
            # If it does, treat is as an edit (i.e. remove it from db, then add it fresh)

            classroom_id = self.class_id.text().strip()
            wanted_class = readClassroomItem(connection, classroom_id)
            lab = self.class_lab.checkedButton().text()

            if classroom_id.isspace() or classroom_id == "":
                close_connection(connection)
                return

            val = 0

            if (lab == "Lab"):
                val = 1
            if(len(wanted_class) == 1):
                deleteClassroomItem(connection, self.class_id.text().strip())

            new_room = Classroom(self.class_id.text().strip(), self.class_capacity.value(), val)
            addClassroomItem(connection, new_room)

            # Must close connection to update db before updating comboboxes
            close_connection(connection)

            # Update the combobox
            self.update_class_combos()


        except:
            print("error adding classroom")
            close_connection(connection)

    def remove_classroom(self):
        db = r".\database\database.db"  # database.db file path
        connection = create_connection(db)

        try:

            # Remove the classroom from the DB
            classroom = self.classroom_list.currentText()

            deleteClassroomItem(connection, classroom.replace("(LAB)", "").strip())

            close_connection(connection)

            # Update the combobox
            self.update_class_combos()


        except:
            print("error adding classroom")
            close_connection(connection)

    def save_course(self):
        db = r".\database\database.db"  # database.db file path
        connection = create_connection(db)

        try:

            if self.courses_edit_new.checkedButton().text() == "New Course":
                course_id = self.course_id.text().strip()
            else:
                course_id = self.courses.currentText().strip()

            if course_id.isspace() or course_id == "":
                close_connection(connection)
                return

            wanted_course = readCourseItem(connection, course_id)

            if(len(wanted_course) == 1):
                deleteCourseItem(connection, course_id)

            term_hours = self.course_term_hours.value()
            term = self.course_term.value()
            duration = self.course_duration.value()
            core = self.course_core.isChecked()
            online = self.course_online.isChecked()
            lab = self.course_lab.isChecked()
            pre_reqs = self.course_pre_reqs

            new_course = Course(course_id, 1, term_hours, term, duration, core, online,lab, pre_reqs)
            addCourseItem(connection, new_course)

            close_connection(connection)
            # Update the combobox
            self.update_course_combos()

        except:
            print("error adding course")

    def update_course_combos(self):
        db = r".\database\database.db"  # database.db file path
        connection = create_connection(db)
        db_courses = readCourseItem(connection, "%")
        close_connection(connection)

        course_name_list = []

        for each_course in range(len(db_courses)):
            course_name_list.append(db_courses[each_course][0])

        self.courses.clear()
        self.courses.addItems(course_name_list)
        self.course_pre_req_selector.clear()
        self.course_pre_req_selector.addItems(course_name_list)

    def show_hide_course(self):

        if self.courses_edit_new.checkedButton().text() == "New Course":
            self.course_id.show()
            self.courses.hide()
        else:
            self.course_id.hide()
            self.courses.show()


    def add_pre_req(self):
        self.course_pre_reqs.append(self.course_pre_req_selector.currentText())
        self.course_pre_reqs_label.setText(", ".join(self.course_pre_reqs))

    def clear_pre_reqs(self):
        self.course_pre_reqs.clear()
        self.course_pre_reqs_label.clear()