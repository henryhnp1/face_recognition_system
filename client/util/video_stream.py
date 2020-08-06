import cv2
import sys
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGroupBox
import math

src_cam = 0
ws = 380
prototxt = '/home/henry/FinalProject/face_recognition_system/core/data/model/deploy.prototxt'
detect_model = '/home/henry/FinalProject/face_recognition_system/core/data/model/res10_300x300_ssd_iter_140000.caffemodel'
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        video_stream = VideoStream(src=src_cam).start()
        time.sleep(1.0)
        count = args.cur_im
        while True:
            frame = video_stream.read()
            frame = imutils.resize(frame, width=ws)
            net = cv2.dnn.readNetFromCaffe(prototxt, detect_model)
            h, w = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                (300, 300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence < args.confidence:
                    continue
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = box.astype('int')
                box = (math.floor(startX), math.floor(startY), round(endX), round(endY))
                thickness_border = 2
                thickness_rectangle = 40
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), thickness_border)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            # cv2.imshow("frame", frame)
            # key = cv2.waitKey(1) & 0xFF
            # if key == ord('q'):
            #     break
            # if key == ord('c'):
            #     temp = frame
            #     count += 1
            #     cv2.imwrite(args.stf + str(count)+'.jpg', frame)

# class MyGroupBox(QGroupBox):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     @pyqtSlot(QImage)
#     def setImage(self, image):
#         self.label.setPixmap(QPixmap.fromImage(image))

#     def initUI(self):
#         # create a label
#         self.label = QLabel(self)
#         self.label.move(280, 120)
#         self.label.resize(640, 480)
#         th = Thread(self)
#         th.changePixmap.connect(self.setImage)
#         th.start()