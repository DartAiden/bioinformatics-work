import cv2 as cv
from pygrabber.dshow_graph import FilterGraph
import time
import numpy as np
import matplotlib.pyplot as plt

def getcams():

    devices = FilterGraph().get_input_devices()

    cams = {}

    for device_index, device_name in enumerate(devices):
        cams[device_name] = device_index
    return cams


class saver():
    def __init__(self, filename, width, height, on, off, output):
        name = filename+'.avi'
        size = (width, height)
        fourcc = cv.VideoWriter_fourcc(*'MJPG')
        self.vid = cv.VideoWriter(name, fourcc, 15, size)
        self.lister = []
        self.on = on
        self.off = off
        self.output = output
    def anal(self, frame: np.ndarray):

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, frame = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)

        conts, _ = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        conts = sorted(conts, key =lambda it: cv.contourArea(it), reverse = True)
        m = cv.moments(conts[0])
        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])
        self.lister.append(np.array((cX, cY)))
        if cX > 320:
            w = 0
        self.vid.write(frame)
    def end(self):
        self.vid.release()
        arr = np.array(self.lister)
        plt.scatter(arr[:,0], arr[:,1])
        plt.xlim([0,640])
        plt.ylim([0,480])
        plt.show()

            
