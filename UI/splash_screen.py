import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def splash_screen(self):
        # Start up splash screen
        # adapted from: https://stackoverflow.com/questions/58661539/create-splash-screen-in-pyqt5
        
        if getattr(sys, 'frozen', True):
            logo = 'macewan_logo.png'
        else:
            logo = '..\\macewan_logo.png'

        splash_pic = QPixmap(logo)
        splash_msg = QSplashScreen(splash_pic, Qt.WindowStaysOnTopHint)
        splash_msg.setFixedSize(965, 568)

        #Fade in, fade out
        opaque = 0.00
        step = 0.02
        splash_msg.setWindowOpacity(opaque)
        splash_msg.show()
        while opaque < 1:
            splash_msg.setWindowOpacity(opaque)
            time.sleep(step)
            opaque+=step
        time.sleep(2)
        while opaque > 0:
            splash_msg.setWindowOpacity(opaque)
            time.sleep(2*step)
            opaque-=2*step
        splash_msg.close()