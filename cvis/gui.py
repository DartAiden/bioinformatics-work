import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QComboBox
from PySide6.QtCore import QSize, Qt
import cam
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(20)
        self.setWindowTitle("Place Preference")
        self.setFixedSize(QSize(1200, 900))

        self.cams = QComboBox()
        self.cams.count = 4
        self.cams.editable = False
        self.cams.currentData = ['CAM1', 'CAM2', 'CAM3', 'CAM4']
        layout.addWidget(self.cams, 0, 0)


        self.launch = QPushButton("Launch")
        self.launch.setCheckable(True)
        self.setCentralWidget(self.launch)
        self.launch.clicked.connect(self.launchCallback)
        layout.addWidget(self.launch, 4, 0)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)



    def launchCallback(self):
        print("test")
        self.launch.setEnabled(False)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()