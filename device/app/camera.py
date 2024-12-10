import threading
import time
import cv2
from datetime import datetime
import os
from .logger import logger_instance
from .pi_utils import *


def _file_name(customer_path, order_id):
    return f"{customer_path}/{order_id}_{datetime.now().strftime('%b_%d_%Y_%H_%M_%S')}.avi"

def _record(customer_id, order_id):
    try:
        customer_path = f"recordings/{customer_id}"
        os.makedirs(customer_path, exist_ok=True)

        if is_pi_environment == False:
            return
        # Open a connection to the external camera (0 is usually the default camera, use 1 for external camera)
        logger_instance.info(f"Recording started for order {order_id} with user {customer_id}")
        cap = cv2.VideoCapture(0)

        # Check if the camera opened successfully
        if not cap.isOpened():
            raise Exception("Error: Could not open the camera.")

        # Define the codec and create a VideoWriter object to save the video
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like 'MJPG' or 'X264'
        out = cv2.VideoWriter(_file_name(customer_path, order_id), fourcc, 20.0, (640, 480))

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
        logger_instance.info("Recording ended")
    except Exception as e:
        logger_instance.error(f"Recording for order {order_id} with user {customer_id} failed with: {e}")

def record(customer_id, order_id):
    thread = threading.Thread(target=_record, args=(customer_id, order_id))
    thread.start()
    logger_instance.info(f"Recording for order {order_id} with user {customer_id} was successful")