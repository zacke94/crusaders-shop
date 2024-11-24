import threading
import time
import cv2
from datetime import datetime
import os
from .logger import logger_instance
from .pi_utils import *


def _file_name(id):
    return f"recordings/{id}/{datetime.now().strftime('%b_%d_%Y_%H_%M_%S')}.avi"

def _record(id):
    try:
        os.makedirs(f"recordings/{id}", exist_ok=True)

        if is_pi_environment == False:
            return
        # Open a connection to the external camera (0 is usually the default camera, use 1 for external camera)
        logger_instance.info("Camera starting")
        cap = cv2.VideoCapture(0)

        # Check if the camera opened successfully
        if not cap.isOpened():
            raise Exception("Error: Could not open the camera.")

        # Define the codec and create a VideoWriter object to save the video
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like 'MJPG' or 'X264'
        out = cv2.VideoWriter(_file_name(id), fourcc, 20.0, (640, 480))

        start_time = time.time()

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if not ret:
                raise Exception("Error: Failed to capture image.")

            # Write the frame to the video file
            out.write(frame)

            # Break the loop after 10 seconds or if 'q' is pressed
            if time.time() - start_time > 10:
                break

        # Release everything when done
        cap.release()
        out.release()
        logger_instance.info("Camera finished")
    except Exception as e:
        logger_instance.error(f"Recording for user {id} failed with: {e}")



def record(id):
    thread = threading.Thread(target=_record, args=(id,))
    thread.start()
    thread.join()

    logger_instance.info(f"Recording for user {id} was successful")