#Imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from database.database import *

#Button Styles
class Style:

    def __init__(self):
        self.font = QFont()
        self.specs = ""

#Most buttons
glass = Style()
glass.specs = (     "background-color: #5e869c; " +
                    "color: #fefdea; " +
                    "border-color: #fefdea; ")


#Navigation arrows and other major buttons
coal = Style()
coal.specs =  (     "background-color: #4f4f4f; " +
                    "color: #fefdea; " +
                    "border-width: 3px; "+
                    "border-radius: 5px; "+
                    "border-color: #fefdea")
coal.font.setBold(True)
coal.font.setPointSize(20)


#Backgrounds
brick = Style()
brick.specs = (    "background-color: #3b0918; " +
                    "color: #fefdea; ") 



paper = Style()
paper.specs = (  "background-color: #fefdea; " +
                    "color: #4f4f4f; " +
                    "border-color: #fefdea; ")

#Label Styles

#Most Labels
#Regular text
snow_reg = Style()
snow_reg.specs = ("color: #fefdea")
snow_reg.font.setPointSize(10)
snow_reg.font.setBold(False)
snow_reg.font.setItalic(False)

#Headers
snow_header1 = Style()
snow_header1.specs = ("color: #fefdea")
snow_header1.font.setPointSize(16)
snow_header1.font.setBold(True)
snow_header1.font.setItalic(False)

#Subheaders
snow_header2 = Style()
snow_header2.specs = ("color: #fefdea")
snow_header2.font.setPointSize(14)
snow_header2.font.setBold(True)
snow_header2.font.setItalic(True)


#Widget functions
def push_button(Style, label, task):
    button = QPushButton(label)
    button.setFont(Style.font)
    button.setStyleSheet(Style.specs)
    button.clicked.connect(task)

    return button

def label(Style, text, size = 10):
    label = QLabel(text)
    label.setStyleSheet(Style.specs)
    Style.font.setPointSize(size)
    label.setFont(Style.font)

    return label

def drop_down(Style, task = None):
    dropdown = QComboBox()
    dropdown.setStyleSheet(Style.specs)
    if task != None:
        dropdown.activated.connect(task)

    return dropdown

def spin_box(Style, min = 0, max = 1000):
    spinbox = QSpinBox()
    spinbox.setStyleSheet(Style.specs)
    spinbox.setMinimum(min)
    spinbox.setValue(min)
    spinbox.setMaximum(max)

    return spinbox

def splash(Style):
    splash = QSplashScreen()
    splash.setFixedSize(400,200)
    splash.setStyleSheet(Style.specs)
    splash.setFont(snow_header1.font)

    return splash

def create_horizontal_line():
    h_line = QFrame()
    h_line.setFrameShape(QFrame.HLine)
    h_line.setFrameShadow(QFrame.Plain)
    h_line.setStyleSheet("color: #fefdea")
    h_line.setLineWidth(3)

    return h_line

def create_vertical_line():
    v_line = QFrame()
    v_line.setFrameShape(QFrame.VLine)
    v_line.setLineWidth(2)
    v_line.setFrameShadow(QFrame.Plain)
    v_line.setStyleSheet("color: #fefdea")

    return v_line