# main.py
import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tracking.detector import detect_colored_object

# Define HSV range for the object (example: red ball)
lower_hsv = np.array([20, 100, 100])
upper_hsv = np.array([40, 255, 255])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    box, mask = detect_colored_object(frame, lower_hsv, upper_hsv)
    if box:
        x, y, w, h = box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Mask", mask)
    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
