import cv2
from picamera2 import Picamera2
import numpy as np
import time




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
