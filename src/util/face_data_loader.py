from os import listdir
from os.path import isdir

from util.face_extraction import extract_face
import numpy as np
import os
from numpy import savez_compressed
from tensorflow.keras.models import load_model
from sklearn.linear_model import SGDClassifier
# from face_extraction import extract_face
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer, FunctionTransformer
import pickle

def load_faces(directory, prototxt, detect_model):
    faces = []
    for filename in listdir(directory):
        path = directory + filename
        print("loading: " + path)
        face = extract_face(path, prototxt, detect_model)
        if face is None:
            continue
        faces.append(face)
    return faces

def load_dataset(directory, prototxt, detect_model):
    faces_data, labels_data = [], []
    dd = 1
    print(directory)
    for subdir in listdir(directory):
        path_folder = directory + subdir + '/'
        if not isdir(path_folder):
            next
        data_compress = path_folder + subdir +'_faces_data.npz'
        if os.path.exists(data_compress):
            faces, labels = load_face_data_from_file(data_compress)
            print('>load from file face data.npz')
        else:
            faces = load_faces(path_folder, prototxt, detect_model)
            labels = [subdir for _ in range(len(faces))]
            savez_compressed(data_compress, faces, labels)
            print(">save " + data_compress)
        print('>loaded %d examples for class: %s' %(len(faces), subdir))
        print('>loaded %d data class' %(dd))
        faces_data.extend(faces)
        labels_data.extend(labels)
        dd += 1
    return np.asarray(faces_data), np.asarray(labels_data)

def embedding_face_data(face_data_compress, face_embedded_compress, model_embedding):
    data_loaded = np.load(face_data_compress, allow_pickle=True)
    faces_data, labels_data = data_loaded['arr_0'], data_loaded['arr_1']
    newFaces = []
    print(len(faces_data), len(labels_data))
    for i, face_pixels in enumerate(faces_data):
        if face_pixels is not None:
            embedding = get_embedding(model_embedding, face_pixels)
            newFaces.append(embedding)
        else:
            labels_data = np.delete(labels_data, i)
    savez_compressed(face_embedded_compress, newFaces, labels_data)
    print("save " + face_embedded_compress)

def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = np.expand_dims(face_pixels, axis=0)
    yhat = model.predict(samples)
    return yhat[0]

def load_face_data_from_file(file_face_compress):
    data_loaded = np.load(file_face_compress, allow_pickle=True)
    faces_data, labels_data = data_loaded['arr_0'], data_loaded['arr_1']
    return faces_data, labels_data

def load_face_embedded_from_file(file_face_embedded_compress):
    data_loaded = np.load(file_face_embedded_compress, allow_pickle=True)
    face_embedded, labels = data_loaded['arr_0'], data_loaded['arr_1']
    return face_embedded, labels

def run_load_data(face_dir, prototxt, detect_model):
    faces, labels = load_dataset(face_dir, prototxt, detect_model)

def run_embedding(face_dir, model, file_embedded_all):
    run_embedding_face_data(face_dir, model)
    run_get_all_embedding(face_dir, file_embedded_all)

def run_embedding_face_data(face_dir, model):
    for subdir in listdir(face_dir):
        path_folder = face_dir + subdir + '/'
        face_data_compress = path_folder + subdir +'_faces_data.npz'
        face_embedding_compress = path_folder + subdir +'_faces_embedded.npz'
        print(face_data_compress, face_embedding_compress)
        if os.path.exists(face_data_compress):
            if os.path.exists(face_embedding_compress):
                continue
            embedding_face_data(face_data_compress, face_embedding_compress, model)

def run_get_all_embedding(face_dir, file_embedded_all):
    faces_embedded, labels = [], []
    for subdir in listdir(face_dir):
        path_folder = face_dir + subdir + '/'
        if not isdir(path_folder):
            continue
        if os.path.exists(path_folder + subdir + '_faces_embedded.npz'):
            embedded_compresed = path_folder + subdir + '_faces_embedded.npz'
            data_loaded = np.load(embedded_compresed, allow_pickle=True)
            embedded, labeled = data_loaded['arr_0'], data_loaded['arr_1']
            faces_embedded.extend(embedded)
            labels.extend(labeled)
    X_train, X_test, y_train, y_test= train_test_split(faces_embedded, labels, test_size=0.2, stratify=labels)
    savez_compressed(file_embedded_all, X_train, y_train, X_test, y_test)

def train_model(face_dir, model_embedding, detect_model, prototxt, file_embedded_all, model_classification_path):
    run_load_data(face_dir, prototxt, detect_model)
    run_embedding(face_dir, model_embedding, file_embedded_all)
    data = np.load(file_embedded_all)
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    print('Dataset: train=%d, test=%d' % (trainX.shape[0], testX.shape[0]))
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    testX = in_encoder.transform(testX)

    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
    testy = out_encoder.transform(testy)

    # model_classify = SGDClassifier(loss='hinge', penalty='l2', max_iter=1000)
    model_classify = SVC(kernel='rbf' , class_weight='balanced' , C=1000 , gamma=0.0082, probability=True)
    model_classify.fit(trainX, trainy)
    
    pickle.dump(model_classify, open(model_classification_path, 'wb'))
    yhat_train = model_classify.predict(trainX)
    yhat_test = model_classify.predict(testX)

    score_train = accuracy_score(trainy, yhat_train)
    score_test = accuracy_score(testy, yhat_test)
    print('Accuracy: train=%.3f, test=%.3f' % (score_train*100, score_test*100))

def test():
    face_dir = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/processed/'
    model_embedding_path = '/home/henry/FinalProject/face_recognition_system/src/data/model/facenet_keras.h5'
    model_embedding = load_model(model_embedding_path)
    detect_model = '/home/henry/FinalProject/face_recognition_system/src/data/model/res10_300x300_ssd_iter_140000.caffemodel'
    prototxt = '/home/henry/FinalProject/face_recognition_system/src/data/model/deploy.prototxt'
    file_embedded_all = '/home/henry/FinalProject/face_recognition_system/src/data/face_embedding.npz'
    model_classification_path = '/home/henry/FinalProject/face_recognition_system/src/data/predict_model.sav'
    train_model(face_dir, model_embedding, detect_model, prototxt, file_embedded_all, model_classification_path)

def load_single_face_data(directory, prototxt, detect_model):
    directory_name = directory.split('/')[-1]
    data_compress = directory + '/' + directory_name + '_faces_data.npz'
    if os.path.exists(data_compress):
        faces, labels = load_face_data_from_file(data_compress)
        print('>load from file face data.npz')
    else:
        faces = load_faces(directory+'/', prototxt, detect_model)
        labels = [directory_name for _ in range(len(faces))]
        savez_compressed(data_compress, faces, labels)
        print(">save " + data_compress)
    return np.asarray(faces), np.asarray(labels)

def load_single_embedding(directory, prototxt, detect_model, model_embedding):
    directory_name = directory.split('/')[-1]
    embedded_comprass = directory + '/' + directory_name + '_faces_embedded.npz'
    if os.path.exists(embedded_comprass):
        return embedded_comprass
    face_data, label_data = load_single_face_data(directory, prototxt, detect_model)
    newFaces = []
    for i, face_pixels in enumerate(face_data):
        if face_pixels is not None:
            embedding = get_embedding(model_embedding, face_pixels)
            newFaces.append(embedding)
        else:
            label_data = np.delete(label_data, i)
    savez_compressed(embedded_comprass, newFaces, label_data)
    print("save " + embedded_comprass)
    return embedded_comprass

def test_partial_learning():
    face_dir = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/processed/'
    directory = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/processed/Alyssa_Milano'
    model_embedding_path = '/home/henry/FinalProject/face_recognition_system/src/data/model/facenet_keras.h5'
    model_embedding = load_model(model_embedding_path)
    detect_model = '/home/henry/FinalProject/face_recognition_system/src/data/model/res10_300x300_ssd_iter_140000.caffemodel'
    prototxt = '/home/henry/FinalProject/face_recognition_system/src/data/model/deploy.prototxt'
    model_classification_path = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/predict_model001.sav'
    new_model_classification_path = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/predict_model002.sav'
    file_embedded_all = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/face_embedding.npz'
    new_name = load_single_embedding(directory, prototxt, detect_model, model_embedding)
    data = np.load(new_name)
    new_trainX, new_trainY = data['arr_0'], data['arr_1']
    run_get_all_embedding(face_dir, file_embedded_all)
    data = np.load(file_embedded_all)
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']

    model_classify = pickle.load((open(model_classification_path, 'rb')))
    model_classify.partial_fit(new_trainX, new_trainY)

    pickle.dump(model, open(new_model_classification_path, 'wb'))
    yhat_train = model_classify.predict(trainX)
    yhat_test = model_classify.predict(testX)

    score_train = accuracy_score(trainy, yhat_train)
    score_test = accuracy_score(testy, yhat_test)
    print('Accuracy: train=%.3f, test=%.3f' % (score_train*100, score_test*100))

# test_partial_learning()
# test()