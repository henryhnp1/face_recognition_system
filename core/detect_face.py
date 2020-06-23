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
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from keras.models import load_model
from random import choice


prototxt = 'core/data/model/deploy.prototxt'
detect_model = 'core/data/model/res10_300x300_ssd_iter_140000.caffemodel'
data_dir = 'core/data/dataset/raw/'
data = 'core/data/dataset/dataset_face_001.npz'
embedded = 'core/data/dataset/face_embedding_001.npz'

def get_single_bbox_from_image(image_path, prototxt, detect_model, confidence_param=0.5):
    net = cv2.dnn.readNetFromCaffe(prototxt, detect_model)
    image = cv2.imread(image_path)  # to do: image link
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_param:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            startX, startY, endX, endY = box.astype('int')
            if startX > w: startX = 0
            if startY > h: startY = 0
            if endX > w: endX = w
            if endY > h: endY = h
            box = (math.floor(startX), math.floor(startY), round(endX), round(endY))
    return box

def extract_face(filename, prototxt, detect_model ,confidence=0.5, required_size=(160, 160)):
    startX, startY, endX, endY = get_single_bbox_from_image(filename, prototxt, detect_model)
    print(startX, startY, endX, endY)
    image = Image.open(filename)
    image = image.convert('RGB')
    pilxels = np.asarray(image)
    face = pilxels[startY:endY, startX:endX]
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = np.asarray(image)
    return face_array

def load_faces(directory, prototxt, detect_model):
    faces = []
    for filename in listdir(directory):
        path = directory + filename
        print("loading: " + path)
        face = extract_face(path, prototxt, detect_model)
        faces.append(face)
    return faces

def load_dataset(directory, prototxt, detect_model):
    faces_data, labels_data = [], []
    for subdir in listdir(directory):
        path = directory + subdir + '/'
        if not isdir(path):
            next
        faces = load_faces(path, prototxt, detect_model)
        labels = [subdir for _ in range(len(faces))]
        print('>loaded %d examples for class: %s' %(len(faces), subdir))
        faces_data.extend(faces)
        labels_data.extend(labels)
    return np.asarray(faces_data), np.asarray(labels_data)

def run_load_data():
    faces, labels = load_dataset(data_dir, prototxt, detect_model)
    print(faces.shape, labels.shape)
    X_train, X_test, y_train, y_test= train_test_split(faces, labels, test_size=0.2, stratify=labels)
    savez_compressed(data, X_train, y_train, X_test, y_test)

def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = np.expand_dims(face_pixels, axis=0)
    yhat = model.predict(samples)
    return yhat[0]
    
def run_get_embedding():
    data = np.load('../data/dataset/face_001.npz')
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    print('Loaded: ', trainX.shape, trainy.shape, testX.shape, testy.shape)
    model = load_model('../data/model/facenet_keras.h5')
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
    savez_compressed('../data/dataset/face_001_embeddings.npz', newTrainX, trainy, newTestX, testy)


def train_model():
    run_get_embedding()
    data = np.load('../data/dataset/face_001_embeddings.npz')
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

    
def test_train():
    data_load = np.load(data)
    testX_faces = data_load['arr_2']
    # load face embeddings
    data_load = np.load(embedded)
    trainX, trainy, testX, testy = data_load['arr_0'], data_load['arr_1'], data_load['arr_2'], data_load['arr_3']
    # normalize input vectors
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    print("after transform: ", trainX)
    testX = in_encoder.transform(testX)
    # # label encode targets
    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
    testy = out_encoder.transform(testy)
    # fit model
    model = SVC(kernel='linear', probability=True)
    model.fit(trainX, trainy)
    selection = choice([i for i in range(testX.shape[0])])
    random_face_pixels = testX_faces[selection]
    random_face_emb = testX[selection]
    random_face_class = testy[selection]
    random_face_name = out_encoder.inverse_transform([random_face_class])
    # prediction for the face
    samples = np.expand_dims(random_face_emb, axis=0)
    yhat_class = model.predict(samples)
    yhat_prob = model.predict_proba(samples)
    # get name
    class_index = yhat_class[0]
    class_probability = yhat_prob[0,class_index] * 100
    predict_names = out_encoder.inverse_transform(yhat_class)
    print('Predicted: %s (%.3f)' % (predict_names[0], class_probability))
    print('Expected: %s' % random_face_name[0])
    # plot for fun
    plt.imshow(random_face_pixels)
    title = '%s (%.3f)' % (predict_names[0], class_probability)
    plt.title(title)
    plt.show()




def test_get_list_face():
    folder = '../data/dataset/raw/chipu/'
    i = 1
    for filename in listdir(folder):
        path = folder + filename
        face = extract_face(path)
        print(i, face.shape)
        plt.subplot(3, 10, i)
        plt.axis('off')
        plt.imshow(face)
        i+=1
    plt.show()

# # get_face_from_video()
def test():
    filename = '../data/dataset/raw/khanh/024.jpg'
    image = cv2.imread(filename)
    startX, startY, endX, endY = get_box_from_image(filename, 'test.jpg')
    face = image[startY:endY, startX:endX]
    print(startX, startY, endX, endY)

    

#test()
#run_load_data()
#train_model()
test_train()
    