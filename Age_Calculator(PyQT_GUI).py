from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton  ## Import all the classes we will use
import sys  ## Important for loading and exiting the program
from datetime import datetime  ## Important for getting current year

class AgeCalculator(QWidget):  ## A class that inherits QWidget class
    def __init__(self):  ## We edit the init so this code loads as soon as the class is instantiated
        super().__init__()  ## We add the functionality of init method of the parent class as well, so instead of overwriting the init, we add to it.

        ## Setup the content
        self.setWindowTitle("Age Calculator")  ## Title
        grid = QGridLayout()  ## Instantiated grid layout class
        name = QLabel("Name: ")  ## Instantiated name label
        dob = QLabel("Date of Birth (MM/DD/YYYY): ")  ## Instantiated date of birth label
        self.name_edit = QLineEdit()  ## Instantiated edit box for name. Converted to instance variables to be used by other methods in this class
        self.dob_edit = QLineEdit()  ## Instantiated edit box for age. Converted to instance variables to be used by other methods in this class
        button = QPushButton("Caclucate Age")
        self.output = QLabel("")  ## Instantiated Output label to show the result. Converted to instance variables to be used by other methods in this class

        ## Setup Grid Window.
        grid.addWidget(name, 0,0)  ## first row, first column
        grid.addWidget(dob, 1,0)  ## second row, first column
        grid.addWidget(self.name_edit, 0,1)  ## first row, second column
        grid.addWidget(self.dob_edit, 1,1)  ## second row, second column
        grid.addWidget(button, 2,0,1,2)  ## third row, first column spanned to one row two columns
        grid.addWidget(self.output, 3,0,1,2)  ## fourth row, first column spanned to one row two columns

        ## Functionality
        button.clicked.connect(self.calculation)  ## Process calculation when button is pressed

        self.setLayout(grid)  ## Set the layout as designed above on the window

    ## Perform calculation
    def calculation(self):
        current_year = datetime.now().year  ## Get current year
        date_of_birth = self.dob_edit.text()  ## get the text entered in dob_edit box
        year_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y").date().year  ## convert dob text to date and get year from it
        age = current_year - year_of_birth
        self.output.setText(f"{self.name_edit.text()} is {age} years old.")  ## Edit output layout text to display the result.


## The actual instantiation and program
app = QApplication(sys.argv)  ## Instantiate the window
age_caclulator = AgeCalculator()  ## Instantiate the widgets
age_caclulator.show()  ## show the windows with widgets
sys.exit(app.exec())  ## Close the window
