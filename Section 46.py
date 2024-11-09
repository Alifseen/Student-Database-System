from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar
import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3


## Add a Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        ## default size of the window
        self.setMinimumSize(800,600)

        ## Add Top Menu
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu("&Edit")

        sub_menu_add = QAction(QIcon("Files/icons/add.png"), "Add Student", self)
        file_menu.addAction(sub_menu_add)
        sub_menu_add.triggered.connect(self.add_student)  ## This calls the function when clicked

        sub_menu_about = QAction("About SMS", self)
        help_menu.addAction(sub_menu_about)

        sub_menu_search = QAction(QIcon("Files/icons/search.png"), "Search", self)
        edit_menu.addAction(sub_menu_search)
        sub_menu_search.triggered.connect(self.search_student)  ## This calls the function when clicked

        ## Add Table for Data to Load into
        self.table = QTableWidget()
        self.table.setColumnCount(4)  ## Sets columns to 4
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "SUBJECT", "MOBILE"))

        self.table.verticalHeader().setVisible(False)  ## Removes the row number display

        self.setCentralWidget(self.table)  ## Makes the table widget the main widget

        ## Add Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(sub_menu_add)
        toolbar.addAction(sub_menu_search)


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

    def search_student(self):
        SearchStudentPopup().exec()


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
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter The Students Name")
        layout.addWidget(self.name_edit)

        ## Subject Field
        courses = ["Math","Astronomy","Physics","Biology"]
        self.subject_select = QComboBox()
        self.subject_select.addItems(courses)
        layout.addWidget(self.subject_select)

        ## Mobile Field
        self.mobile_edit = QLineEdit()
        self.mobile_edit.setPlaceholderText("Enter The Students Mobile")
        layout.addWidget(self.mobile_edit)

        ## Button Field
        button = QPushButton("Register")
        layout.addWidget(button)
        button.clicked.connect(self.register)

        self.setLayout(layout)

    def register(self):
        ## Get data from instance variables
        name = self.name_edit.text()
        subject = self.subject_select.itemText(self.subject_select.currentIndex())
        mobile = self.mobile_edit.text()

        ## Connect and Insert the values into SQL
        connection = sqlite3.connect("Files/database.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)", (name, subject, mobile))
        connection.commit()

        cursor.close()
        connection.close()

        sms.load_data()


## Search Student Popup
class SearchStudentPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Search")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        ## Search field
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Enter Name to Search")
        layout.addWidget(self.search_field)

        ## Button
        self.button = QPushButton("Search")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.search_student)

        self.setLayout(layout)

    def search_student(self):
        query = self.search_field.text()  ## Save query

        connection = sqlite3.connect("Files/database.db")
        cursor = connection.cursor()

        sql_result = cursor.execute("SELECT * FROM students WHERE name = ?", (query,))  ## Look for query in SQL

        search_result = list(sql_result)  ## Covnert SQL to list of tuples

        table_result = sms.table.findItems(query, Qt.MatchFlag.MatchFixedString)  ## search for list in table
        for result in table_result:
            sms.table.item(result.row(),1).setSelected(True)  ## for each matched item take the row and highlight/select the first column (name column))

        cursor.close()
        connection.close()



app = QApplication(sys.argv)
sms = MainWindow()
sms.load_data()  ## Loads SQL Data on the Table
sms.show()
sys.exit(app.exec())