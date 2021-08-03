from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *

from threading import Thread

class KeyboardListener(QWidget):

    bindings = {}

    def __init__(self):
        return

    def event(self, event):
            if event.type() == QEvent.KeyPress:
                print("KEY PRESSED: {}\nTYPE: {}".format(event.key(), type(event.key()))) 
                return True

            return super().event(event)