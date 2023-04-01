#Imports
import os
import sys
import time
import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from database.database import *
import imports.fillClassrooms

import imports.schedulers.core_scheduler
import imports.schedulers.program_scheduler
import imports.classes.classrooms
import datetime
import copy

#Button Styles
class Style:

    def __init__(self):
        self.font = QFont()
        self.style = ""


#Button Styles

#Most buttons
glass = Style()
glass.style = (     "background-color: #5e869c; " +
                    "color: #fefdea; " +
                    "border-color: #fefdea; ")


#Navigation arrows and other major buttons
coal = Style()
coal.style =  (     "background-color: #4f4f4f; " +
                    "color: #fefdea; " +
                    "border-width: 3px; "+
                    "border-radius: 5px; "+
                    "border-color: #fefdea")
coal.font.setBold(True)
coal.font.setPointSize(20)

#Label Styles

#Most Labels
#Regular text
snow_reg = Style()
snow_reg.style = ("color: #fefdea")
snow_reg.font.setPointSize(10)
snow_reg.font.setBold(False)
snow_reg.font.setItalic(False)

#Headers
snow_header1 = Style()
snow_header1.style = ("color: #fefdea")
snow_header1.font.setPointSize(16)
snow_header1.font.setBold(True)
snow_header1.font.setItalic(False)

#Subheaders
snow_header2 = Style()
snow_header2.style = ("color: #fefdea")
snow_header2.font.setPointSize(14)
snow_header2.font.setBold(True)
snow_header2.font.setItalic(True)


#Widget functions
def push_button(Style, label, task):
    button = QPushButton(label)
    button.setFont(Style.font)
    button.setStyleSheet(Style.style)
    button.clicked.connect(task)

    return button

def label(Style, text, size = 10):
    label = QLabel(text)
    label.setStyleSheet(Style.style)
    Style.font.setPointSize(size)
    label.setFont(Style.font)

    return label

def drop_down(Style, task = None):
    dropdown = QComboBox()
    dropdown.setStyleSheet(Style.style)
    dropdown.activated.connect(task)

    return dropdown