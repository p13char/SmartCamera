import cv2
from picamera2 import Picamera2
import numpy as np
import time

# loading the files for mobilenet model
classNames = []
classFile = "coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"
# values got from research paper and hit trial  Ref-link:   https://www.ijert.org/research/real-time-object-detection-and-recognition-using-mobilenet-ssd-with-opencv-IJERTV11IS010070.pdf
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)

net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
class VideoCamera(object):
    def __init__(self):
        self.picam2 = Picamera2()
        
        self.picam2.configure(self.picam2.create_preview_configuration(main={"size": (1920, 1080)}))
        
        self.picam2.start()
        time.sleep(2.0)  

    def __del__(self):
        self.picam2.stop()

    def get_frame(self):
        frame = self.picam2.capture_array()
        if frame.shape[2] ==4:
        
            frame = cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)
        return frame

def getObjects(self, thres, nms, draw=True):
        ''' Funtion to get the objects in the image frame '''
        flag = False
        img = self.get_frame()
        
        classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
        objects = classNames
        objectInfo = []
        
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                className = classNames[classId - 1]
                if className in objects:
                    flag = True
                    objectInfo.append([box, className])
                    if draw:
                        cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                        cv2.putText(img, classNames[classId-1].upper(), (box[0] + 10, box[1] + 30),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        return img, flag
