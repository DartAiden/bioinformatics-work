from PyQt5 import QtMultimedia, QtTest
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QComboBox, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import QSize, Qt, QEventLoop, QThread, QTimer
import cv2 as cv
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
import cvanalysis
import numpy as np
import time
from pygrabber.dshow_graph import FilterGraph
'''
This is a program that creates a GUI to determine which place a mouse preferences, analyzes the position, and then plots it.
The backbone is the QT for Python environment. It pulls a frame and then displays it in the GUI. When launch is started, it passes the frames it pulls to an OpenCV series of functions.
These functions then determine the centroid of the largest contour. It saves the frames and the position of the centroid to an AVI file and a MatPlotLib scatterplot.
It continuously monitors the frames that are passed to see if the Arduino should be activated.
Reach out to Aiden Dartley, or adartley123@gmail.com, if you have any questions/concerns about this code.
'''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        def oncamchange():    
            if self.cap:
                self.cap.release() 
            try:
                self.cap = cv.VideoCapture(self.caminds[self.cams.currentText]) #changes the camera that is being used to capture
            except:
                pass
        def onfilter():
            if self.filterlabel.checkState():  
                self.cap.set(cv.CAP_PROP_BRIGHTNESS, 0.0) #Settings to imitate the original MATLAB
                self.cap.set(cv.CAP_PROP_CONTRAST, 104.0)
                self.cap.set(cv.CAP_PROP_SATURATION, 50)
                self.cap.set(cv.CAP_PROP_WB_TEMPERATURE, 5950.0) 
                self.cap.set(cv.CAP_PROP_GAIN, 1) 
            else:
                self.cap.set(cv.CAP_PROP_BRIGHTNESS, self.defaults["brightness"])
                self.cap.set(cv.CAP_PROP_CONTRAST, self.defaults["contrast"])
                self.cap.set(cv.CAP_PROP_SATURATION, self.defaults["saturation"])
                self.cap.set(cv.CAP_PROP_WB_TEMPERATURE, self.defaults["wb"])
                self.cap.set(cv.CAP_PROP_GAIN, self.defaults["gain"])

        self.timeend = 10 #how long the recording lasts for
        self.refresh = 20 #how often to pull the frame
        devices = FilterGraph().get_input_devices()
        self.camnames = [] #strings of the camnames
        self.caminds = {} #indices of the sams
        for device_index, device_name in enumerate(devices):
            if cv.VideoCapture(device_index).isOpened():
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
        outputlist = ['COM1','COM2', 'COM3', 'COM4'] #outputs for the computer in the lab, will change thsi maybe
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
        self.vid = 0


        layout.setRowStretch(13,2)
        self.lsrofflabel = QLabel("Laser off time:")
        self.lsroffbox = QLineEdit()
        layout.addWidget(self.lsrofflabel,15,0,1,1)
        layout.addWidget(self.lsroffbox,15,1,1,1)
        layout.setRowStretch(14,2)


        self.checked = False
        self.filterlabel = QCheckBox()
        self.filterlabel.setText("Filter")
        self.filterlabel.stateChanged.connect(onfilter)
        self.filterlabel.setChecked(False)
        layout.addWidget(self.filterlabel, 15, 6, 1, 1)
        try:
            self.cap = cv.VideoCapture(self.caminds[self.camnames[0]])

        except:
            pass
        self.currentframe = QLabel()
        layout.addWidget(self.currentframe, 20, 2, 1, 14)
        self.defaults = {"brightness" : self.cap.get(cv.CAP_PROP_BRIGHTNESS), #These save the default values of certain camera settings on OpenCV.
                    "saturation" : self.cap.get(cv.CAP_PROP_SATURATION), #OpenCV modifies the cameara settings, so this is necessary
                    "contrast" : self.cap.get(cv.CAP_PROP_CONTRAST),
                    "exposure" : self.cap.get(cv.CAP_PROP_EXPOSURE),
                    "gain" : self.cap.get(cv.CAP_PROP_GAIN),
                    "wb" : self.cap.get(cv.CAP_PROP_WB_TEMPERATURE)} 
        try:
            self.cap.set(cv.CAP_PROP_BRIGHTNESS, self.defaults["brightness"])
            self.cap.set(cv.CAP_PROP_CONTRAST, self.defaults["contrast"])
            self.cap.set(cv.CAP_PROP_SATURATION, self.defaults["saturation"])
            self.cap.set(cv.CAP_PROP_CONTRAST, self.defaults["wb"])
            self.cap.set(cv.CAP_PROP_GAIN, self.defaults["gain"])
        except:
            pass
        print(self.defaults)
        self.timer = QTimer()
        self.timer.timeout.connect(self.readframe) #pulls the frame every self.refresh mses
        self.timer.start(self.refresh)

        self.launch = QPushButton("Start")
        self.launch.setCheckable(True) 
        self.launch.clicked.connect(self.launchCallback)
        layout.addWidget(self.launch,40,0,1,10)
        layout.setRowStretch(39,40)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    def readframe(self):
        ret, frame = self.cap.read()
        if ret:
            if self.vid != 0:
                self.vid.write(frame)
            if self.filterlabel.checkState():

                ret,self.inter = self.cap.read()

                self.inter = cv.cvtColor(self.inter, cv.COLOR_BGR2RGB)
                self.inter = cv.cvtColor(self.inter, cv.COLOR_BGR2GRAY)  #converts it to grayscale
                ret, self.inter = cv.threshold(self.inter, 127, 255, cv.THRESH_BINARY) #and then the binary black and white
                self.frame = cv.cvtColor(self.inter, cv.COLOR_GRAY2RGB) #and then back to color


                
            else:
                ret,self.inter = self.cap.read()
                self.frame = cv.cvtColor(self.inter,cv.COLOR_BGR2RGB)


            h, w, ch = self.frame.shape
            bline = ch * w

            start = np.array((int(w/2),h))
            end = np.array((int(w/2),0))
            cv.line(self.frame, start, end , (255,0,0), 2) #adds a midline
            qimage = QImage(self.frame, w, h, bline, QImage.Format_RGB888) #converts the capture to a QImage
        
            pixmap = QPixmap.fromImage(qimage) #And then a QPixmap
            self.currentframe.setPixmap(pixmap) #and then sets it

    def launchCallback(self):
        if self.intcheck(self.lsronbox.text()) and self.intcheck(self.lsroffbox.text()) and self.validname(self.txtbox.text()):
            self.lsronbox.setEnabled(False)
            self.lsroffbox.setEnabled(False)
            self.lsronbox.setEnabled(False)
            self.filterlabel.setChecked(True)
            self.filterlabel.setEnabled(False)
            self.txtbox.setEnabled(False)
            self.outputs.setEnabled(False)
            cams = cvanalysis.getcams()
            self.launch.setEnabled(False)
            print(self.txtbox.text())
            self.name = str(self.txtbox.text()) + ".mp4"
            end = time.time() + self.timeend
            runner = cvanalysis.saver(self.name, 640, 320, self.lsronbox.text(), self.lsroffbox.text(), self.outputs.currentText())
            
            fourcc = cv.VideoWriter_fourcc(*'mp4v')
            frame_width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
            self.vid = cv.VideoWriter(self.name, fourcc, 15.0, (frame_width,frame_height))


            while time.time() < end:
                runner.anal(self.frame)
                QtTest.QTest.qWait(self.refresh)
            self.vid.release()

            runner.end()
            self.lsronbox.setEnabled(True)
            self.lsroffbox.setEnabled(True)
            self.lsronbox.setEnabled(True)
            self.filterlabel.setEnabled(True)
            self.txtbox.setEnabled(True)
            self.outputs.setEnabled(True)
            self.launch.setEnabled(True)
            self.vid = 0
    def intcheck(self, num): #ensures the text is an int
        num = num.strip()
        if len(num) == 0:
            return False
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        for i in range(len(num)):
            if num[i] not in nums:
                return False
        return True
    def validname(self, name):
        forbidden = ["<", ">", '"', ":","/", "|", "?", "*"] #ensures the text is a valid file name
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
        self.cap.set(cv.CAP_PROP_CONTRAST, self.defaults["wb"])
        self.cap.set(cv.CAP_PROP_GAIN, self.defaults["gain"])


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
