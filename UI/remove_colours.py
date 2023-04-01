#Imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def remove_colours(BG_COLOURS):
    excludedcolours = ["aliceblue", "mediumturquoise", "midnightblue", 
                    "lavenderblush", "blue", "mediumblue", "blanchedalmond", 
                    "indigo", "seashell", "navy", "black", "brown", "beige",
                    "azure", "deeppink", "fuchsia", "hotpink", "magenta",
                    "red", "pink", "mediumvioletred", "blueviolet", "darkviolet",
                    "mediumpurple", "purple"]

    for colour in excludedcolours:
        BG_COLOURS.remove(colour)

    _colours = BG_COLOURS.copy()
    for colour in range(len(_colours)):
        if "dark" in _colours[colour] or "white" in _colours[colour] or "gray" in _colours[colour] or "grey" in _colours[colour]:
            BG_COLOURS.remove(_colours[colour])

    return(BG_COLOURS)