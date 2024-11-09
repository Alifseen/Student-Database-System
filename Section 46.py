from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout
import sys
from PyQt6.QtGui import QAction
import sqlite3


## Add a Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        ## default size of the window
        self.setFixedHeight(600)
        self.setFixedWidth(600)

        ## Add Top Menu
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        sub_menu_add = QAction("Add Student", self)
        file_menu.addAction(sub_menu_add)
        sub_menu_add.triggered.connect(self.add_student)  ## This calls the function when clicked

        sub_menu_about = QAction("About SMS", self)
        help_menu.addAction(sub_menu_about)

        ## Add Table for Data to Load into
        self.table = QTableWidget()
        self.table.setColumnCount(4)  ## Sets columns to 4
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "SUBJECT", "MOBILE"))

        self.table.verticalHeader().setVisible(False)  ## Removes the row number display

        self.setCentralWidget(self.table)  ## Makes the table widget the main widget

    ## Load SQL Data into the Table
    def load_data(self):
        ## Load DB and get data
        connection = sqlite3.connect("Files/database.db")
        cursor = connection.cursor()
        data = cursor.execute("SELECT * FROM students")

        self.table.setRowCount(0)  ## This makes sure tha data is loaded in the table from row 1 column 1, not whereever the last entry was from.

        for row_no, row_data in enumerate(data):  ## loops over index and tuples from the SQL data
            self.table.insertRow(row_no)  ## Adds a row
            for col_no, cell_data in enumerate(row_data):  ## loops over the tuple
                self.table.setItem(row_no, col_no, QTableWidgetItem(str(cell_data)))  ## Adds the text into the cell

        connection.close()

    def add_student(self):
        AddStudenttPopup().exec()  ## this calls the class to open a pop up dialog box


## Create a pop up window for adding a student
class AddStudenttPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student Details")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        ## Instantiate the Layout
        layout = QVBoxLayout()

        ## Name field
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("Enter The Students Name")
        layout.addWidget(name_edit)

        ## Subject Field
        courses = ["Math","Astronomy","Physics","Biology"]
        subject = QComboBox()
        subject.addItems(courses)
        layout.addWidget(subject)

        ## Mobile Field
        mobile_edit = QLineEdit()
        mobile_edit.setPlaceholderText("Enter The Students Mobile")
        layout.addWidget(mobile_edit)

        ## Button Field
        button = QPushButton("Register")
        layout.addWidget(button)
        button.clicked.connect(self.register)

        self.setLayout(layout)

    def register(self):
        pass




app = QApplication(sys.argv)
sms = MainWindow()
sms.load_data()  ## Loads SQL Data on the Table
sms.show()
sys.exit(app.exec())