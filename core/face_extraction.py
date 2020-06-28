import numpy as np
from PIL import Image
from face_detection import get_single_bbox_from_image
import cv2

def extract_face(filename, prototxt, detect_model ,confidence=0.5, required_size=(160, 160)):
    box = get_single_bbox_from_image(filename, prototxt, detect_model)
    if box is None:
        return None
    startX, startY, endX, endY = get_single_bbox_from_image(filename, prototxt, detect_model)
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