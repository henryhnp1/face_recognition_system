import numpy as np
import cv2
from imutils.video import VideoStream
import imutils
import time
import math
from PIL import Image
from os import listdir
from numpy import savez_compressed
from os.path import isdir
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer, FunctionTransformer
from sklearn.svm import SVC
from keras.models import load_model
from random import choice
import argparse
import sys

from face_data_loader import load_faces, load_dataset, get_embedding
from face_extraction import extract_face, get_extract_face_array_from_image
from face_detection import get_single_bbox_from_image


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', type=str, choices=['CAP', 'TRAIN', 'CLASSIFY'])
    parser.add_argument('--data_dir', type=str)  # folder of all image
    parser.add_argument('--model', type=str)  # facenet pretrained model
    parser.add_argument('--data', type=str)  # folder of faces data
    parser.add_argument('--embedding', type=str)
    parser.add_argument('--detect_model', type=str)
    parser.add_argument('--prototxt')
    parser.add_argument('--confidence', type=float, default=0.5)  
    parser.add_argument('--src_cam', type=int, default=0)  #use src cam
    parser.add_argument('--stf', type=str)  # save to folder
    parser.add_argument('--ws', type=int, default=1080)  # width screen
    parser.add_argument('--cur_im', type=int, default=0)
    
    return parser.parse_args(argv)

def get_image_from_video(args):
    video_stream = VideoStream(src=args.src_cam).start()
    time.sleep(2.0)
    count = args.cur_im
    while True:
        frame = video_stream.read()
        frame = imutils.resize(frame, width=args.ws)
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('c'):
            temp = frame
            count += 1
            cv2.imwrite(args.stf + str(count)+'.jpg', frame)
    cv2.destroyAllWindows()
    video_stream.stop()

def run_load_data(args):
    faces, labels = load_dataset(args.data_dir, args.prototxt, args.detect_model)
    X_train, X_test, y_train, y_test= train_test_split(faces, labels, test_size=0.2, stratify=labels)
    savez_compressed(args.data, X_train, y_train, X_test, y_test)

def run_embedding(args):
    data = np.load(args.data)
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    print('Loaded: ', trainX.shape, trainy.shape, testX.shape, testy.shape)
    model = load_model(args.model)
    print('Loaded Model')
    newTrainX = []
    for face_pixels in trainX:
        embedding = get_embedding(model, face_pixels)
        newTrainX.append(embedding)
    newTrainX = np.asarray(newTrainX)
    print(newTrainX.shape)
    newTestX = list()
    for face_pixels in testX:
        embedding = get_embedding(model, face_pixels)
        newTestX.append(embedding)
    newTestX = np.asarray(newTestX)
    print(newTestX.shape)
    savez_compressed(args.embedding, newTrainX, trainy, newTestX, testy)
        
def train_model(args):
    run_load_data(args)
    run_embedding(args)
    data = np.load(args.embedding)
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    print('Dataset: train=%d, test=%d' % (trainX.shape[0], testX.shape[0]))
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    testX = in_encoder.transform(testX)

    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
    testy = out_encoder.transform(testy)

    model = SVC(kernel='linear', probability=True)
    model.fit(trainX, trainy)

    yhat_train = model.predict(trainX)
    yhat_test = model.predict(testX)

    score_train = accuracy_score(trainy, yhat_train)
    score_test = accuracy_score(testy, yhat_test)
    print('Accuracy: train=%.3f, test=%.3f' % (score_train*100, score_test*100))

def run_classify(args):
    video_stream = VideoStream(src=args.src_cam).start()
    time.sleep(2.0)
    count = 0
    #========= load model ==========
    model = load_model(args.model)
    face_embedded_data = np.load(args.embedding)
    trainX, trainy = face_embedded_data['arr_0'], face_embedded_data['arr_1']
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)

    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)

    model_predict = SVC(kernel='linear', probability=True)
    model_predict.fit(trainX, trainy)

    while True:
        frame = video_stream.read()
        frame = imutils.resize(frame, width=args.ws)
        net = cv2.dnn.readNetFromCaffe(args.prototxt, args.detect_model)
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
            if startX > w: startX = 0
            if startY > h: startY = 0
            if endX > w: endX = w
            if endY > h: endY = h
            box = (math.floor(startX), math.floor(startY), round(endX), round(endY))
            thickness_border = 2
            thickness_rectangle = 40
            #======= recognition ===============================
            face_array = get_extract_face_array_from_image(frame, box)
            embedding = get_embedding(model, face_array)

            samples = np.expand_dims(embedding, axis=0)
            y_hatclass = model_predict.predict(samples)

            y_hatprob = model_predict.predict_proba(samples)
            class_index = y_hatclass[0]
            index = y_hatprob.argmax()
            predic = y_hatprob[0, index] * 100
            text_print = None
            fonscale = 0.7
            if predic >= 80:
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
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('r'):
            pass
            # name = recognizer()
    cv2.destroyAllWindows()
    video_stream.stop()

def run(args):
    if args.mode == 'CAP':
        get_image_from_video(args)
        '''
            python core/face_recognition.py --mode CAP
        '''
    elif args.mode == 'TRAIN':
        train_model(args)
        '''
            python core/face_recognition.py --mode TRAIN --data_dir core/data/dataset/raw/ 
            --model core/data/model/facenet_keras.h5 --embedding core/data/dataset/face_embedding_001.npz 
            --data core/data/dataset/dataset_face_001.npz  --prototxt core/data/model/deploy.prototxt 
            --detect_model core/data/model/res10_300x300_ssd_iter_140000.caffemodel 
        '''
    else:
        run_classify(args)
        '''
            python core/face_recognition.py --mode CLASSIFY --prototxt core/data/model/deploy.prototxt 
            --detect_model core/data/model/res10_300x300_ssd_iter_140000.caffemodel --confidence 0.8 
            --model core/data/model/facenet_keras.h5 --embedding core/data/dataset/face_embedding_001.npz 
        '''

run(parse_arguments(sys.argv[1:]))
