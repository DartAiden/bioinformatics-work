import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QComboBox, QLabel
from PySide6.QtCore import QSize, Qt, QEventLoop, QThread, Signal
from PySide6 import QtSerialPort, QtTest
from PySide6.QtSerialPort import QSerialPortInfo
import cam
from PIL import Image,ImageOps
import io

from PySide6.QtGui import QPixmap, QImage

import cam
class MainWindow(QMainWindow):
    
    class Cam(QThread):
        image_signal = Signal(QPixmap)
        def __init__(self, camer, parent):
            super().__init__(parent)
            self.camer = camer
            self.parent = parent

            self.image = cam.pull(self.camer)
        def run(self):
            while True:
                self.image = cam.pull(self.camer)
                self.pixer = Image.open(io.BytesIO(self.image))
                self.pixer = ImageOps.invert(self.pixer)
                self.pixer.save("saver.jpg")
                qimage = QImage(self.pixer.tobytes(), self.pixer.width, self.pixer.height, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                #self.image_signal.emit(pixmap)
                QtTest.QTest.qWait(100)


    def __init__(self):
        def updateThread(self,camer):
            self.camthread.camer = camer

        
        super().__init__()
        layout = QGridLayout()

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(20)
        self.setWindowTitle("Place Preference")
        self.setFixedSize(QSize(1200, 900))
        try:
            #self.feed = QtSerialPort.QSerialPort(self.cams.currentText(), baudRate = 9600, readyRead = True)
                        
            self.cams = QComboBox()
            camlist = QSerialPortInfo().availablePorts()
            camlist = ['COM1','COM2']
            self.cams.count = len(camlist)
            self.cams.editable = False
            self.cams.addItems(camlist)
            layout.addWidget(self.cams, 0, 0)
            
            self.camthread = self.Cam(self.cams.currentText(),self)
            self.camthread.start()
            self.cams.currentTextChanged.connect(self.updateThread)
        except:

         #   self.label = QLabel()
          #  self.label.setText("No available ports!")
           # layout.addWidget(self.label, 0, 0)
           print("Err")
        self.currentcam = "COM1"
        self.launch = QPushButton("Launch")
        self.launch.setCheckable(True)
        self.launch.clicked.connect(self.launchCallback)
        layout.addWidget(self.launch, 4, 0)

        self.loop = QEventLoop()
        self.image = Image.open(r'cvis\imerror.png', 'r') 
        self.image = ImageOps.invert(self.image)

        barr = self.image.tobytes("xbm", "rgb")
        pixmap = QPixmap(barr)
        self.imlabel = QLabel(self)
        self.imlabel.setPixmap(pixmap)
        layout.addWidget(self.imlabel,2,0)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def updateThread(self, pixmap):
        self.imlabel.setPixmap(pixmap)


    def launchCallback(self):
        print(self.cams.currentText())
        self.launch.setEnabled(False)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
