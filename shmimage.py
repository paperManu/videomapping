import pyshmdata as shm
import numpy as np
import cv2 as cv
import struct
import re
from time import sleep, ctime

class ShmImage():
    def __init__(self):
        self.shmreader = None
        self.shmtype = None
        self.image = None
        self.callback = None

        self.bppMath = re.compile('(bpp=\(int\))(\d*)')
        self.widthMatch = re.compile('(width=\(int\))(\d*)')
        self.heightMatch = re.compile('(height=\(int\))(\d*)')

    
    def callback(self, image, datatype):
        width = int(self.widthMatch.search(datatype).group(2))
        height = int(self.heightMatch.search(datatype).group(2))
        sizeStr = str(width * height)

        array = np.frombuffer(image, np.uint16, width * height)
        array.shape = (height, width)
        self.image = array
        self.shmtype = datatype

        if self.callback is not None:
            self.callback(self.image)

    
    def connect(self, shmpath="", callback=None):
        self.callback = callback
        self.shmreader = shm.Reader(path=shmpath, callback=ShmImage.callback, user_data=self)


    def getType(self):
        return self.shmtype


    def getImage(self):
        return self.image


class DetectSurface():
    def __init__(self):
        self.image = None
        self.detector = None
        self.points = None

        self.thresholdValue = 127

        self.detectorParams = cv.SimpleBlobDetector_Params()
        self.detectorParams.filterByColor = False
        self.detectorParams.filterByConvexity = False
        self.detectorParams.filterByInertia = False


    def setImage(self, img):
        if self.detector is None:
            self.detector = cv.SimpleBlobDetector(self.detectorParams)

        self.image = img.astype(np.uint8)
        self.image = cv.threshold(self.image, self.thresholdValue, 255, cv.THRESH_BINARY)[1]
        self.points = self.detector.detect(self.image)


    def getPoints(self):
        return self.points


    def getMatrix(self):
        pass


def test():
    shm = ShmImage()
    shm.connect("/tmp/switcher_nodeserver_posturesrc6_ir")

    detector = DetectSurface()

    return shm, detector
