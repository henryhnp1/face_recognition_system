import numpy as np
from PIL import Image
from util.face_detection import get_single_bbox_from_image
import cv2
from os import listdir
from os.path import isdir, splitext
import os

# from face_detection import get_single_bbox_from_image

def extract_face(filename, prototxt, detect_model ,confidence=0.5, required_size=(160, 160)):
    box = get_single_bbox_from_image(filename, prototxt, detect_model)
    if box is None:
        return None
    startX, startY, endX, endY = box
    image = Image.open(filename)
    image = image.convert('RGB')
    pilxels = np.asarray(image)
    face = pilxels[startY:endY, startX:endX]
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = np.asarray(image)
    return face_array

def get_extract_face_array_from_image(image_file, bbox, required_size=(160, 160)):
    startX, startY, endX, endY = bbox
    image = cv2.cvtColor(image_file, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(image)
    pixels = np.asarray(image)
    face = pixels[startY:endY, startX:endX]
    image = image.resize(required_size)
    face_array = np.asarray(image)
    return face_array

def crop_face(filename, prototxt, detect_model, destination, current_num, confidence=0.5):
    box = get_single_bbox_from_image(filename, prototxt, detect_model)
    print(box)
    if box is None:
        return None
    startX, startY, endX, endY = box
    image = cv2.imread(filename)
    crop_image = image[startY:endY, startX:endX]
    dest = destination+current_num+'.jpg'
    cv2.imwrite(dest, crop_image)
    print('Crop face to ' + dest)

def crop_face_data(folder, prototxt, detect_model, conficence=0.5):
    for subdir in listdir(folder):
        child = folder + subdir + '/'
        dest = '/home/henry/FinalProject/face_recognition_system/core/data/dataset/processed/' + subdir +'/'
        if not os.path.exists(dest):
            os.makedirs(dest)
        for item in listdir(child):
            if not isdir(item):
                if item.endswith('.jpg') or item.endswith('.jpeg'):
                    file_name = item.split('.')[0]
                    item = os.path.join(child, item)
                    print(item)
                    crop_face(item, prototxt, detect_model, dest, file_name)

# def test():
#     folder = '/home/henry/FinalProject/face_recognition_system/core/data/'
#     image_dir = '/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/'
#     prototxt = '/home/henry/FinalProject/face_recognition_system/core/data/model/deploy.prototxt'
#     detect_model = '/home/henry/FinalProject/face_recognition_system/core/data/model/res10_300x300_ssd_iter_140000.caffemodel'
#     crop_face_data(image_dir, prototxt, detect_model)

# test()