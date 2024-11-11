from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox, QGridLayout, QLabel
import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3


class SQLConnection:
    def __init__(self, database_file="Files/database.db"):
        self.database_file = database_file

    def connect(self):
        connect = sqlite3.connect(self.database_file)
        return connect


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
        sub_menu_about.triggered.connect(self.about)  ## This calls the function when clicked

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

        ## Add Status Bar at the bottom that only shows buttons when cell is selected
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.table.cellClicked.connect(self.show_buttons)  ## Show buttons when cell is clicked


    ## Load SQL Data into the Table
    def load_data(self):
        ## Load DB and get data
        connection = SQLConnection.connect()
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

    def edit_cell(self):
        EditCellPopup().exec()

    def delete_cell(self):
        DeleteCellPopup().exec()

    def show_buttons(self):
        ## Create an edit button
        edit_button = QPushButton("Edit Cell")
        edit_button.clicked.connect(self.edit_cell)

        ## Create a delete button
        delete_button = QPushButton("Delete Cell")
        delete_button.clicked.connect(self.delete_cell)

        ## If buttons exists, remove them so there are no duplicates
        button_status = self.findChildren(QPushButton)  ## Checks if QpushButton is already in the method
        if button_status:
            for button in button_status:
                self.status_bar.removeWidget(button)

        ## Add Buttons
        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    ## Display "About" window
    def about(self):
        AboutPopup().exec()


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
        connection = SQLConnection.connect()
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

        connection = SQLConnection.connect()
        cursor = connection.cursor()

        sql_result = cursor.execute("SELECT * FROM students WHERE name = ?", (query,))  ## Look for query in SQL

        search_result = list(sql_result)  ## Covnert SQL to list of tuples

        table_result = sms.table.findItems(query, Qt.MatchFlag.MatchFixedString)  ## search for list in table
        for result in table_result:
            sms.table.item(result.row(),1).setSelected(True)  ## for each matched item take the row and highlight/select the first column (name column))

        cursor.close()
        connection.close()


## Dialog box that edits cell
class EditCellPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Details")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        ## Get the Name from the field and place it
        self.row = sms.table.currentRow()
        name = sms.table.item(self.row, 1).text()

        self.name_edit = QLineEdit(name)
        self.name_edit.setPlaceholderText("Enter The Students Name")
        layout.addWidget(self.name_edit)

        ## Get the Subject from the box and place it
        subject = sms.table.item(self.row, 2).text()

        courses = ["Math","Astronomy","Physics","Biology"]
        self.subject_select = QComboBox()
        self.subject_select.addItems(courses)
        self.subject_select.setCurrentText(subject)
        layout.addWidget(self.subject_select)

        ## Get the Mobile from the box and place it
        mobile = sms.table.item(self.row, 3).text()

        self.mobile_edit = QLineEdit(mobile)
        self.mobile_edit.setPlaceholderText("Enter The Students Mobile")
        layout.addWidget(self.mobile_edit)

        button = QPushButton("Register")
        layout.addWidget(button)
        button.clicked.connect(self.update)

        self.setLayout(layout)

    def update(self):
        ## Get the values
        updated_name = self.name_edit.text()
        updated_subject = self.subject_select.itemText(self.subject_select.currentIndex())
        updated_mobile = self.mobile_edit.text()
        student_id = sms.table.item(self.row,0).text()

        ## Connect with and edit SQL DB
        connection = SQLConnection.connect()
        cursor = connection.cursor()

        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?", (updated_name, updated_subject, updated_mobile, student_id))

        ## Close and Finalize
        connection.commit()
        cursor.close()
        connection.close()
        sms.load_data()

        self.close()


## Dialog box that deletes cell
class DeleteCellPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Details")


        ## Create a confirmation prompt
        layout = QGridLayout()

        sure = QLabel("Are you sure you want to Delete the Data?")
        no = QPushButton("No")
        yes = QPushButton("Yes")

        layout.addWidget(sure, 0,0,1,2)
        layout.addWidget(yes, 1,0)
        layout.addWidget(no, 1,1)

        ## Delete if user clicked yes
        yes.clicked.connect(self.delete)

        self.setLayout(layout)

    def delete(self):
        row = sms.table.currentRow()
        student_id = sms.table.item(row, 0).text()

        connection = SQLConnection.connect()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM students WHERE id = ?", (student_id, ))

        connection.commit()
        cursor.close()
        connection.close()
        sms.load_data()

        ## Close the confirmation prompt
        self.close()

        ## Show a message box once deleted
        self.confirmation_msg()

    ## Show a message box
    def confirmation_msg(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Success")
        msg_box.setText("Deleted Successfully")
        msg_box.exec()


## Message Box that shows info about the program
class AboutPopup(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About SMS (Student Management System)")

        content = """\
        This Program Lets you enter, edit, store and delete student information such as names, subjects and phone numbers.
        Feel free to modify or re-use it as you see fit. 
        """

        self.setText(content)


app = QApplication(sys.argv)
sms = MainWindow()
sms.load_data()  ## Loads SQL Data on the Table
sms.show()
sys.exit(app.exec())