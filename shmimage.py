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

        self.bppMath = re.compile('(bpp=\(int\))(\d*)')
        self.widthMatch = re.compile('(width=\(int\))(\d*)')
        self.heightMatch = re.compile('(height=\(int\))(\d*)')

    
    def callback(self, image, datatype):
        width = int(self.widthMatch.search(datatype).group(2))
        height = int(self.heightMatch.search(datatype).group(2))
        sizeStr = str(width * height)

        tple = struct.unpack(sizeStr + "H", image)
        array = np.array(tple, dtype=np.uint16)
        array.shape = (height, width)
        self.image = array

    
    def connect(self, shmpath=""):
        self.shmreader = shm.Reader(path=shmpath, callback=ShmImage.callback, user_data=self)
