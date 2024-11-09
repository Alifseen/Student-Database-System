from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox
import sys

class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()
        distance = QLabel("Distance: ")
        time = QLabel("Time: (Hours)")
        self.distance_edit = QLineEdit()
        self.time_edit = QLineEdit()
        button = QPushButton("Calculate")
        self.output = QLabel("")
        self.type = QComboBox()
        self.type.addItem("Metric (KM)")
        self.type.addItem("Imperial (M)")

        grid.addWidget(distance, 0,0)
        grid.addWidget(self.distance_edit, 0,1)
        grid.addWidget(self.type, 0,2)
        grid.addWidget(time, 1,0)
        grid.addWidget(self.time_edit, 1,1)
        grid.addWidget(button, 2,1)
        grid.addWidget(self.output, 3,0,1,3)

        button.clicked.connect(self.calculate)

        self.setLayout(grid)

    def calculate(self):
        d = float(self.distance_edit.text())
        t = float(self.time_edit.text())
        metric = self.type.currentIndex()
        s = d / t
        if metric == 1:
            sp = round(s * 0.621371, 2)
            m = "Mph"
        else:
            sp = round(s, 2)
            m = "Kmph"
        self.output.setText(f"Average Speed: {sp} {m}")


app = QApplication(sys.argv)
speed_caclulator = SpeedCalculator()
speed_caclulator.show()
sys.exit(app.exec())
