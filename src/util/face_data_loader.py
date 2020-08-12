from os import listdir
from os.path import isdir
from util.face_extraction import extract_face
import numpy as np
import os
from numpy import savez_compressed
from keras.models import load_model

def load_faces(directory, prototxt, detect_model):
    faces = []
    for filename in listdir(directory):
        path = directory + filename
        print("loading: " + path)
        face = extract_face(path, prototxt, detect_model)
        if face is None:
            os.remove(path)
            next
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
    model = load_model(model_embedding)
    newFaces = []
    print(len(faces_data), len(labels_data))
    for i, face_pixels in enumerate(faces_data):
        if face_pixels is not None:
            embedding = get_embedding(model, face_pixels)
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