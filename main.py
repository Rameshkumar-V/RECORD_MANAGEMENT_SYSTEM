from PyQt5.QtWidgets import QApplication
from backend import BackEnd
import sys
class Main(BackEnd):
    """
    Main class for Frontend and Backend
    """
    def __init__(self):
        BackEnd.__init__(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()  # Instantiate the FrontEnd class
    window.show()  # Display the window
    sys.exit(app.exec_())
