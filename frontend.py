from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow

class FrontEnd(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file directly into `self`
        uic.loadUi("ui/frontend_10.ui", self)  # Replace with your .ui file path

