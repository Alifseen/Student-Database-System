from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget
import sys
from PyQt6.QtGui import QAction


## Add a Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        ## Add Top Menu
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        sub_menu_add = QAction("Add Student", self)
        file_menu.addAction(sub_menu_add)

        sub_menu_about = QAction("About SMS", self)
        help_menu.addAction(sub_menu_about)

        ## Add Table for Data to Load into
        self.table = QTableWidget()
        self.table.setColumnCount(4)  ## Sets columns to 4
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "SUBJECT", "MOBILE"))

        self.setCentralWidget(self.table)  ## Makes the table widget the main widget




app = QApplication(sys.argv)
sms = MainWindow()
sms.show()
sys.exit(app.exec())