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


#Most Buttons
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


#Function to make button
def push_button(Style, label, task):
    button = QPushButton(label)
    button.setFont(Style.font)
    button.setStyleSheet(Style.style)
    button.clicked.connect(task)

    return button
