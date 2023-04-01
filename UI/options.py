#Imports
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from database.database import *
from UI import widgets as w


def make_tab(self):
    vbox_overall = QVBoxLayout()

    vbox_overall.addLayout(self.update_classroom_section())
    vbox_overall.addWidget(w.create_horizontal_line())
    vbox_overall.addWidget(w.create_horizontal_line())

    vbox_overall.addLayout(self.update_course_section())
    vbox_overall.addWidget(w.create_horizontal_line())
    vbox_overall.addWidget(w.create_horizontal_line())

    #Reset database button
    reset_label = w.label(w.snow_header1, "Reset Database")

    reset_button = w.push_button(w.glass, "Reset to Default Settings", self.reset_db)
    reset_button.setFixedWidth(200)

    hbox = QVBoxLayout()
    hbox.setContentsMargins(20,40,0,50)
    hbox.addWidget(reset_label)
    hbox.addWidget(reset_button)

    vbox_overall.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum))
    vbox_overall.addLayout(hbox)
    vbox_overall.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum))

    return vbox_overall


def reset_db(self):

    global CREATE_SCHEDULE_CLICKED, CORE_SCHEDULE, CORE_SCHEDULE_COHORTS, PROG_SCHEDULE_COHORTS, PROG_SCHEDULE
    answer = QMessageBox(QMessageBox.Warning, "Reset Database",
                                    "Are you sure you want to reset the database?\n\nAll data will be lost!",
                                    buttons=QMessageBox.Yes | QMessageBox.No)
    answer.setDefaultButton(QMessageBox.No)
    answer.setStyleSheet("color: black")
    clicked = answer.exec()

    if clicked == QMessageBox.Yes:
        try:
            os.remove("./database/database.db")
            fill_data.createDefaultDatabase()
            self.update_class_combos()
            self.update_course_combos()
            self.cohort_tab_combo.clear()
            self.reset_table()
            self.reset_table_cohort()
            CORE_SCHEDULE_COHORTS.clear()
            PROG_SCHEDULE_COHORTS.clear()
            CORE_SCHEDULE.clear()
            PROG_SCHEDULE.clear()
            CREATE_SCHEDULE_CLICKED = 0

        except:
            return
    else:
        return
