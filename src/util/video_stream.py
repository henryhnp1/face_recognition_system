import cv2
from imutils.video import VideoStream
import sys
from PyQt5.QtCore import QThread, Qt, pyqtSignal, QObject, pyqtSlot, QRunnable, QSize
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QGroupBox, QWidget, QListWidget, QListView
from util.detect_face import get_single_bbox_from_image
import math
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from util.face_data_loader import load_faces, load_dataset, get_embedding, embedding_face_data
from util.face_extraction import extract_face, get_extract_face_array_from_image
from util.face_detection import get_single_bbox_from_image 
from util import common
from tensorflow.keras.models import load_model
import os 

ws = 380
prototxt = '/home/henry/FinalProject/face_recognition_system/src/data/model/deploy.prototxt'
detect_model = '/home/henry/FinalProject/face_recognition_system/src/data/model/res10_300x300_ssd_iter_140000.caffemodel'
model_path = '/home/henry/FinalProject/face_recognition_system/src/data/model/facenet_keras.h5'
track_folder = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/track/'
# face_embedded_data = np.load(args.embedding)
# trainX, trainy = face_embedded_data['arr_0'], face_embedded_data['arr_1']
# # model_predict_trained = pickle.load(open(args.trained_predict_model, 'rb'))
# in_encoder = Normalizer(norm='l2')
# trainX = in_encoder.transform(trainX)

# out_encoder = LabelEncoder()
# out_encoder.fit(trainy)

# # model_predict_trained = SVC(kernel='linear', probability=True)
# model_predict_trained = SVC(kernel='rbf' , class_weight='balanced' , C=1000 , gamma=0.0082, probability=True)
# model_predict_trained.fit(trainX, trainy)

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

# class CaptureImage(QObject):
#     # video_signal = pyqtSignal(QImage)
#     video_signal = pyqtSignal(np.ndarray)
#     # video_capture = cv2.VideoCapture(1)
#     def __init__(self, parent=None):
#         super(CaptureImage, self).__init__(parent)
#         self.stop_capture = False
#         self.video_capture = cv2.VideoCapture(0)
#     @pyqtSlot()
#     def startVideoCapture(self):
#         while self.stop_capture == False:
#             try:
#                 ret, frame = self.video_capture.read()
#                 color_swapped = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 self.video_signal.emit(color_swapped)
#             except:
#                 pass

class CaptureTrack(QObject):
    video_signal = pyqtSignal(np.ndarray)
    video_capture = cv2.VideoCapture(0)

    def __init__(self, metadata, parent=None):
        super(CaptureTrack, self).__init__(parent)
        self.stop_capture = False
        self.metadata = metadata

    @pyqtSlot()
    def startVideoTrack(self):
        net = cv2.dnn.readNetFromCaffe(prototxt, detect_model)
        model = load_model(model_path)
        self.metadata['result_predict'] = dict()
        temple = []
        while self.stop_capture == False:
            try:
                ret, frame = self.video_capture.read()
                h, w = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                    (300, 300), (104.0, 177.0, 123.0))
                net.setInput(blob)
                detections = net.forward()
                for i in range(0, detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence < self.metadata['confidence']:
                        continue
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    startX, startY, endX, endY = box.astype('int')
                    if startX > w: startX = 0
                    if startY > h: startY = 0
                    if endX > w: endX = w
                    if endY > h: endY = h
                    box = (math.floor(startX), math.floor(startY), round(endX), round(endY))
                    face = common.crop_face(frame, box).copy()
                    face = image_resize(face, 220, 220)
                    thickness_border = 2
                    thickness_rectangle = 40
                    #======= recognition ===============================
                    face_array = get_extract_face_array_from_image(frame, box)
                    embedding = get_embedding(model, face_array)
                    # # test
                    # embedding = in_encoder.format(embedding)

                    samples = np.expand_dims(embedding, axis=0)
                    y_hatclass = self.metadata['predict_model'].predict(samples)
                    y_hatprob = self.metadata['predict_model'].predict_proba(samples)
                    class_index = y_hatclass[0]
                    class_index = self.metadata['out_encoder'].inverse_transform(y_hatclass)[0]
                    index = y_hatprob.argmax()
                    predic = y_hatprob[0, index] * 100
                    text_print = None
                    fonscale = 0.7
                    if predic >= 87:
                        text_print = '%s  %.3f' % (class_index, predic)
                    else:
                        text_print = 'U N K N O W'
                        fonscale = 1
                    startX_text = startX
                    text_size = (cv2.getTextSize(text_print, cv2.FONT_HERSHEY_TRIPLEX, fonscale, 1)[0])[0]
                    if endX < startX + text_size:
                        temp = (startX + text_size - endX)
                        semi_temp = int(temp/2)
                        endX = endX + semi_temp
                        startX = startX - semi_temp if startX - semi_temp > 0 else 0
                        startX_text = startX
                    else:
                        temp = (endX - startX - text_size)
                        startX_text = startX + int(temp/2)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), thickness_border)
                    cv2.rectangle(frame, (startX - thickness_border , endY), (endX + thickness_border, endY+ thickness_rectangle), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, text_print, (startX_text + thickness_border, endY + int(thickness_rectangle*3/4)), cv2.FONT_HERSHEY_TRIPLEX, fonscale, (255, 255, 255))
                    
                    if self.metadata['recognition'] == 1:
                        if text_print == 'U N K N O W':
                            class_index = 'U N K N O W'
                        temple.append(class_index)
                        if len(temple) < 51:
                            if class_index not in self.metadata['result_predict']:
                                self.metadata['result_predict'][class_index] = list()
                                self.metadata['result_predict'][class_index].append(face)
                            else:
                                self.metadata['result_predict'][class_index].append(face)
                        else:
                            result = common.get_key_have_most_values(self.metadata['result_predict'])
                            person_id = common.get_single_value_from_query("select id from person where name_en = '{}' limit 1;".format(result), self.metadata['database'])
                            door_id = self.metadata['door']
                            permission_id = common.get_single_value_from_query("select permission from person_door_permission where person = {} limit 1;".format(person_id),  self.metadata['database'])
                            role_door = common.get_single_value_from_query("select r.name from door as d join role_door as r on d.role = r.id where d.id = {} limit 1;".format(door_id), self.metadata['database'])
                            if permission_id == None:
                                if role_door == None:
                                    permission_id = 2
                                elif role_door == 'RESTRICT': permission_id = 2
                                else: permission_id = 1

                            permission_name = common.get_single_value_from_table('permission', 'name', 'where id = {}'.format(permission_id), self.metadata['database'])
                            time_now = common.get_sql_date_from_now()
                            image_path = track_folder + time_now+'.jpg'
                            cv2.imwrite(track_folder + time_now+'.jpg', self.metadata['result_predict'][class_index][0])
                            temple.clear()
                            self.metadata['result_predict'].clear()
                            if result == 'U N K N O W' or permission_name == 'BAN':
                                query_insert = "insert into warning(name, door, permission, time_in, image) values('{}', {}, {}, '{}', '{}')".format(class_index,  door_id, permission_id, time_now,image_path)
                                common.insert_history_out_in(self.metadata['database'], query_insert)
                            else:
                                query_insert = "insert into history_out_int(person, time, door, permission, url) values({}, '{}', {}, {}, '{}')".format(person_id, time_now, door_id, permission_id, image_path)
                                common.insert_history_out_in(self.metadata['database'], query_insert)
                            print(permission_name, role_door)
                            self.metadata['announce'].setText(permission_name)
                            if permission_name == 'BAN':
                                self.metadata['announce'].setStyleSheet('QLabel{color: red}')
                                duration = 1  # seconds
                                freq = 600
                                os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
                            else:
                                self.metadata['announce'].setStyleSheet('QLabel{color: green}')

                color_swapped = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.video_signal.emit(color_swapped)
            except:
                pass
    
    @pyqtSlot()
    def startVideoCapture(self):
        while self.stop_capture == False:
            try:
                ret, frame = self.video_capture.read()
                color_swapped = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.video_signal.emit(color_swapped)
            except:
                pass

    def set_metadata(self, metadata):
        self.metadata = metadata
        try:
            self.metadata['predict_model'] = pickle.load((open(self.metadata['predict_model_path'], 'rb')))
            self.metadata['embedded_face'] = np.load(self.metadata['embedded_face_path'])
            self.metadata['trainY'] = self.metadata['embedded_face']['arr_1']
            self.metadata['out_encoder'] = LabelEncoder().fit(self.metadata['trainY'])    
        except:
            print("error")

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
        image = image_resize(image, height=421)
        height, width = image.shape[:2]
        image = QImage(image.data, width, height, image.strides[0], QImage.Format_RGB888)
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()



