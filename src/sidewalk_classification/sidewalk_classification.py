import cv2
import threading
import tensorflow as tf
import numpy as np
import time
from utils.circularBuffer import CircularBuffer

classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk', 'Nothing Detected']
model_path = "./sidewalk_classification/sidewalk_classification_model_resnet.h5"
readings_buffer_size = 10
image_preprocessing_dimens = (100, 100)
detection_threshold = 0.85

class SidewalkClassification:

    def capture_processing(self):
        while True:
            try:
                frame = self.video_capture.read()[1]
                preprocessed_frame = cv2.resize(frame, image_preprocessing_dimens, interpolation=cv2.INTER_LINEAR)
                self.images_queue.add(np.expand_dims(frame, 0))
            except Exception as e:
                print("Capturing Not Working", e)

    def classification_starter(self):
        while self.video_capture.isOpened():
            threading.Thread(target=self.capture_processing).start()
            time.sleep(3)
            while True:
                try:
                    self.perform_inference(self.images_queue.getLast())
                except Exception as e:
                    print("Classification Not Working")


    def perform_inference(self, image):
        feedforward_result = self.model.predict(image).tolist()[0]

        self.readings_buffer.add(None if feedforward_result == None or max(feedforward_result) < detection_threshold else feedforward_result)
        averaged_result = self.readings_buffer.mean()
        self.classifier_queue.add(classes[len(classes) - 1] if averaged_result is None else classes[np.argmax(averaged_result)])

    def get_inference(self):
        return self.classifier_queue.getLast()

    def __init__(self, vid_source):
        self.model = tf.keras.models.load_model(model_path)
        self.readings_buffer = CircularBuffer(readings_buffer_size)
        self.images_queue = CircularBuffer(1)
        self.classifier_queue = CircularBuffer(1)
        self.video_capture = cv2.VideoCapture(vid_source)
        threading.Thread(target=self.classification_starter).start()

