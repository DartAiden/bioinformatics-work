import cv2 as cv
import serial as ser
import numpy as np
import io
camname = 'COM1'
def pull(camname):
    try:
        cam = ser.Serial(camname)
        temp = ''
        im = bytearray()
        while b'\xD9' not in temp:
            size = cam.in_waiting
            temp = cam.read(size)
            im.extend(temp)
        return im

    except ser.SerialException:
        with open(r'cvis\imerror.png', "rb") as image:
            f = image.read()
            b = bytearray(f)
        return b
print(pull(camname))