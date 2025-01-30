from PyQt5 import QtMultimedia
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QComboBox, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import QSize, Qt, QEventLoop, QThread, QTimer
import cv2 as cv
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraInfo
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
import cvanalysis
import numpy as np
import os
import sys
import imfilter

from pygrabber.dshow_graph import FilterGraph
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        def oncamchange():    
            if self.cap:
                self.cap.release()

            self.cap = cv.VideoCapture(self.caminds[self.cams.currentText])


        devices = FilterGraph().get_input_devices()
        self.camnames = []
        self.caminds = {}
        for device_index, device_name in enumerate(devices):
            self.camnames.append(str(device_index))
            
            self.caminds[str(device_index)] = device_index
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



        layout.setRowStretch(13,2)
        self.lsrofflabel = QLabel("Laser off time:")
        self.lsroffbox = QLineEdit()
        layout.addWidget(self.lsrofflabel,15,0,1,1)
        layout.addWidget(self.lsroffbox,15,1,1,1)
        layout.setRowStretch(14,2)


        self.checked = False
        self.filterlabel = QCheckBox()
        self.filterlabel.setText("Filter")
        layout.addWidget(self.filterlabel, 15, 6, 1, 1)
        self.filterlabel.stateChanged.connect(self.checker)

        self.cap = cv.VideoCapture(self.caminds[self.camnames[0]])
        self.currentframe = QLabel()
        layout.addWidget(self.currentframe, 20, 2, 1, 14)
        self.defaults = {"brightness" : self.cap.get(cv.CAP_PROP_BRIGHTNESS),
                    "saturation" : self.cap.get(cv.CAP_PROP_SATURATION),
                    "contrast" : self.cap.get(cv.CAP_PROP_CONTRAST),
                    "exposure" : self.cap.get(cv.CAP_PROP_EXPOSURE),
                    "gain" : self.cap.get(cv.CAP_PROP_GAIN),
                    "wb" : self.cap.get(cv.CAP_PROP_WB_TEMPERATURE)} 

        self.timer = QTimer()
        self.timer.timeout.connect(self.readframe)
        self.timer.start(100)

        self.launch = QPushButton("Start")
        self.launch.setCheckable(True)
        self.launch.clicked.connect(self.launchCallback)
        layout.addWidget(self.launch,40,0,1,10)
        layout.setRowStretch(39,40)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    def checker(self):
        self.checked = self.filterlabel.checkState()

    def readframe(self):
        ret,frame = self.cap.read()
        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            if self.checked:
                self.cap.set(cv.CAP_PROP_BRIGHTNESS, 0.0)
                self.cap.set(cv.CAP_PROP_CONTRAST, 104.0)
                self.cap.set(cv.CAP_PROP_SATURATION, 0.0)
                self.cap.set(cv.CAP_PROP_SATURATION, 5950.0)

                ret, frame = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)

                
            else:
                self.cap.set(cv.CAP_PROP_BRIGHTNESS, self.defaults["brightness"])
                self.cap.set(cv.CAP_PROP_CONTRAST, self.defaults["contrast"])
                self.cap.set(cv.CAP_PROP_SATURATION, self.defaults["saturation"])
                self.cap.set(cv.CAP_PROP_WB_TEMPERATURE, self.defaults["wb"])


            h, w, ch = frame.shape
            bline = ch * w
            start = np.array((int(w/2),h))
            end = np.array((int(w/2),0))
            cv.line(frame, start, end , (255,0,0), 2)
            qimage = QImage(frame, w, h, bline, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.currentframe.setPixmap(pixmap)

    def launchCallback(self):
        if self.intcheck(self.lsronbox.text()) and self.intcheck(self.lsroffbox.text()) and self.validname(self.txtbox.text()):
            self.lsronbox.setEnabled(False)
            self.lsroffbox.setEnabled(False)
            self.lsronbox.setEnabled(False)
            self.filterlabel.setChecked(True)
            self.filterlabel.setEnabled(False)
            self.txtbox.setEnabled(False)
            cams = cvanalysis.getcams()
            self.launch.setEnabled(False)
            cvanalysis.anal(300, self.cap)

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

    def closeEvent(self, *args):
        self.cap.set(cv.CAP_PROP_BRIGHTNESS, self.defaults["brightness"])
        self.cap.set(cv.CAP_PROP_CONTRAST, self.defaults["contrast"])
        self.cap.set(cv.CAP_PROP_SATURATION, self.defaults["saturation"])

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
