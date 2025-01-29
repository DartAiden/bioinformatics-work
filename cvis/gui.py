from PyQt5 import QtMultimedia
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QComboBox, QLabel, QLineEdit
from PyQt5.QtCore import QSize, Qt, QEventLoop, QThread
import cv2 as cv
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraInfo
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
import cvanalysis
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        def oncamchange():    
            if self.camera:
                self.camera.stop()  
                self.camera.deleteLater()

            self.camera = QCamera(self.qcams[(self.cams.currentIndex())])

            self.camera.start()
            self.camera.setViewfinder(self.vfinder)


        layout = QGridLayout()

        layout.setContentsMargins(10,0,10,0)
        layout.setSpacing(10)
        self.setWindowTitle("Place Preference")
        self.setFixedSize(QSize(1200, 900))                        
        self.setStyleSheet("background : white;") 

                
        self.outputs = QComboBox()
        self.outputlabel = QLabel("Outputs:")
        layout.addWidget(self.outputlabel, 1,0)
        outputlist = ['COM1','COM2', 'COM3', 'COM4']
        self.outputs.count = len(outputlist)
        self.outputs.editable = False
        self.outputs.addItems(outputlist)
        layout.addWidget(self.outputs,3,0,1,10)
        layout.setRowStretch(2,0)
        self.qcams = QCameraInfo.availableCameras()
        self.camnames = []
        for i in ((self.qcams)):
            self.camnames.append(str(i.description()))

        self.cams = QComboBox()
        self.cams.count = len(self.cams)
        self.cams.editable = False
        self.cams.addItems(self.camnames)
        self.cams.currentIndexChanged.connect(oncamchange)
        self.camlabel = QLabel("Cams:")
        layout.addWidget(self.cams, 7, 0,1,10)
        layout.addWidget(self.camlabel, 5, 0,1,10)
        layout.setRowStretch(6,0)
        layout.setRowStretch(4,2)


        self.txtboxlabel = QLabel("File name: (Do not include extension)")
        self.txtbox = QLineEdit()
        layout.addWidget(self.txtboxlabel,9,0,1,10)
        layout.addWidget(self.txtbox,11,0,1,10)
        layout.setRowStretch(10,0)
        layout.setRowStretch(8,2)



        self.lsronlabel = QLabel("Laser on time:")
        self.lsronbox = QLineEdit()
        layout.addWidget(self.lsronlabel,13,0,1,1)
        layout.addWidget(self.lsronbox,13,1,1,1)
        layout.setColumnStretch(9,100)
        layout.setRowStretch(12,2)
        layout.setRowStretch(14,2)


        self.vfinder = QCameraViewfinder()
        layout.addWidget(self.vfinder, 18, 0, 15, 10)
        self.camera = QCamera((self.qcams[0]))
        self.camera.start()
        self.camera.setViewfinder(self.vfinder)


        layout.setRowStretch(13,2)
        self.lsrofflabel = QLabel("Laser off time:")
        self.lsroffbox = QLineEdit()
        layout.addWidget(self.lsrofflabel,15,0,1,1)
        layout.addWidget(self.lsroffbox,15,1,1,1)
        layout.setRowStretch(14,2)



        self.launch = QPushButton("Start")
        self.launch.setCheckable(True)
        self.launch.clicked.connect(self.launchCallback)
        layout.addWidget(self.launch,40,0,1,10)
        layout.setRowStretch(39,40)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def launchCallback(self):
        if self.intcheck(self.lsronbox.text()) and self.intcheck(self.lsroffbox.text()):
            cams = cvanalysis.getcams()
            self.launch.setEnabled(False)
            ind = cams[self.cams.currentText()]
            cvanalysis.anal(300, ind)


    def intcheck(self, num):
        if len(num) == 0:
            return False
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        for i in range(len(num)):
            if num[i] not in nums:
                return False
        return True
    def validname(self, name):
        forbidden = ["<", ">", '"', ":","/", "|", "?", "*"]
        if len(name) == 0:
            return False
        for i in range(len(name)):
            if name[i] in forbidden:
                return False
        return True


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
