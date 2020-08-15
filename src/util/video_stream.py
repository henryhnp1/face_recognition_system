import cv2
from imutils.video import VideoStream
import sys
from PyQt5.QtCore import QThread, Qt, pyqtSignal, QObject, pyqtSlot, QRunnable, QSize
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QGroupBox, QWidget, QListWidget, QListView
from util.detect_face import get_single_bbox_from_image
import math
import numpy as np

ws = 380
prototxt = '/home/henry/FinalProject/face_recognition_system/src/data/model/deploy.prototxt'
detect_model = '/home/henry/FinalProject/face_recognition_system/src/data/model/res10_300x300_ssd_iter_140000.caffemodel'

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

class CaptureImage(QObject):
    # video_signal = pyqtSignal(QImage)
    video_signal = pyqtSignal(np.ndarray)
    video_capture = cv2.VideoCapture(0)
    def __init__(self, parent=None):
        super(CaptureImage, self).__init__(parent)
        self.stop_capture = False
    @pyqtSlot()
    def startVideoCapture(self):
        while self.stop_capture == False:
            try:
                ret, frame = self.video_capture.read()
                color_swapped = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.video_signal.emit(color_swapped)
            except:
                pass

class ImageViewer(QWidget):

    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QImage()
        self.image_cv = None
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
    
    @pyqtSlot(np.ndarray)
    def setImage(self, image):
        self.image_cv = image.copy()
        image = image_resize(image, height=330)
        height, width = image.shape[:2]
        image = QImage(image.data, width, height, image.strides[0], QImage.Format_RGB888)
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

