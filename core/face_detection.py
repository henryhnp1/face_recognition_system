import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
import math

def get_single_bbox_from_image(image_path, prototxt, detect_model, confidence_param=0.5, frame=None):
    net = cv2.dnn.readNetFromCaffe(prototxt, detect_model)
    if frame is not None:
        image = frame
    else:
        image = cv2.imread(image_path)  # to do: image link
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    box = None
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

def get_face_from_video(image_folder, confidence_param=0.5, src_cam=0):
    video_stream = VideoStream(src=src_cam).start()
    time.sleep(2.0)
    count = 0
    while True:
        frame = video_stream.read()
        frame = imutils.resize(frame, width=1080)
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence < confidence_param:
                continue
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            startX, startY, endX, endY = box.astype('int')
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('c'):
            temp = frame
            count = count + 1
            cv2.imwrite('../data/image/test/test'+ str(count)+'.jpg', frame)
    cv2.destroyAllWindows()
    video_stream.stop()