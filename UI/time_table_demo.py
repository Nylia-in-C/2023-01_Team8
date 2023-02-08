# This file demonstrates how the final classroom time tables should appear.

# To cut down on bloat, this class loads its basic features from the `timeTableTemplate.ui` file.
# The `fill_table` method currently adds color-coded dummy data to the time table.
# The final implementation will ideally be easier to read/follow.

# Rather than hard-coding the data inside a single method, we'll need to pass a dictionary 
# of Classroom objects. When a different classroom is selected from one of the side buttons, 
# that Classroom's booked times should be passed as arguments to a helper function that creates
# the necessary Label objects and places them at the correct coordinates in the window.
# To make this less of a PITA, use the coordinates in the `fill_table` method as reference

# TODO:
# Set the window to a fixed size
# Disable resizing of table columns/rows/cells
# Extend height of table to make room for FS courses (these run from 4:30 - 8:30)
# Move style sheet stuff into a css file 

import sys
import os
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Main(QWidget):
    def __init__(self):
        super().__init__()
        
        curr_path = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(curr_path, "timeTableTemplate.ui")
        uic.loadUi(template_path, self)
        
        self.fill_table()
        self.show()
        
    def fill_table(self):
        # add PCOM 0151 lecture times
        self.label = QLabel(self)
        self.label.setText("PCOM 0151")
        self.label.setGeometry(QRect(385, 141, 125, 112))
        self.label.setStyleSheet("background-color: rgb(85, 0, 127);\n"
"color: rgb(255, 255, 255);")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        
        self.label_2 = QLabel(self)
        self.label_2.setText("PCOM 0151")
        self.label_2.setGeometry(QRect(635, 141, 125, 112))
        self.label_2.setStyleSheet("background-color: rgb(85, 0, 127);\n"
"color: rgb(255, 255, 255);")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        
        # set PCOM 0105 lecture times
        self.label_3 = QLabel(self)
        self.label_3.setText("PCOM 0105")
        self.label_3.setGeometry(QRect(260, 67, 125, 223))
        self.label_3.setStyleSheet("\n"
"background-color: rgb(0, 170, 255);\n"
"color: rgb(255, 255, 255);")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QLabel(self)
        self.label_4.setText("PCOM 0105")
        self.label_4.setGeometry(QRect(385, 326, 125, 149))
        self.label_4.setStyleSheet("\n"
"background-color: rgb(255, 121, 26);\n"
"color: rgb(255, 255, 255);")
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        
        # set PCOM 0203 lecture times
        self.label_5 = QLabel(self)
        self.label_5.setText("PCOM 0203")
        self.label_5.setGeometry(QRect(635, 326, 125, 149))
        self.label_5.setStyleSheet("\n"
"background-color: rgb(255, 121, 26);\n"
"color: rgb(255, 255, 255);")
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        
        self.label_7 = QLabel(self)
        self.label_7.setText("PCOM 0203")
        self.label_7.setGeometry(QRect(260, 475, 125, 74))
        self.label_7.setStyleSheet("background-color: rgb(14, 170, 66);\n"
"color: rgb(255, 255, 255);")
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        
        # set PCOM 0204 lecture times
        self.label_8 = QLabel(self)
        self.label_8.setText("PCOM 0204")
        self.label_8.setGeometry(QRect(510, 475, 125, 74))
        self.label_8.setStyleSheet("background-color: rgb(14, 170, 66);\n"
"color: rgb(255, 255, 255);")
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        
        self.label_9 = QLabel(self)
        self.label_9.setText("PCOM 0204")
        self.label_9.setGeometry(QRect(260, 290, 125, 112))
        self.label_9.setStyleSheet("\n"
"background-color: rgb(144, 98, 24);\n"
"color: rgb(255, 255, 255);")
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        
        # set PCOM 0206 lecture times
        self.label_10 = QLabel(self)
        self.label_10.setText("PCOM 0206")
        self.label_10.setGeometry(QRect(510, 290, 125, 112))
        self.label_10.setStyleSheet("\n"
"background-color: rgb(144, 98, 24);\n"
"color: rgb(255, 255, 255);")
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    app.exec_()