from os import listdir
from os.path import isdir
from face_extraction import extract_face
import numpy as np

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

def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = np.expand_dims(face_pixels, axis=0)
    yhat = model.predict(samples)
    return yhat[0]