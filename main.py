import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from configs import CAMERA_INDEX, COLOR_RANGES, DEFAULT_COLOR, SHOW_MASK, WINDOW_NAME, MIN_CONTOUR_AREA
from tracking.detector import detect_colored_object
from tracking.utils import draw_bounding_box, show_frames

def main():
    # Initialize camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[ERROR] Cannot open camera. Check CAMERA_INDEX.")
        sys.exit(1)

    # Initialize state
    selected_color = DEFAULT_COLOR
    mask = None
    print("[INFO] Starting video stream. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read frame.")
            break

        frame = cv2.flip(frame, 1)  # Flip for mirror view

        # Handle color selection
        key = cv2.waitKey(1) & 0xFF
        color_keys = {
            ord('p'): 'pink',
            ord('b'): 'blue',
            ord('y'): 'yellow',
            ord('g'): 'green',
            ord('w'): 'white',
            ord('o'): 'orange'
        }
        if key in color_keys:
            new_color = color_keys[key]
            if new_color in COLOR_RANGES:
                selected_color = new_color
                print(f"[INFO] Selected color: {selected_color}")
            else:
                print(f"[WARNING] Color '{new_color}' not supported.")

        # Detect object
        if selected_color == 'red':
            combined_mask = None
            box = None
            for lower_hsv, upper_hsv in zip(COLOR_RANGES['red']['LOWER_HSV'], COLOR_RANGES['red']['UPPER_HSV']):
                current_box, current_mask = detect_colored_object(frame, np.array(lower_hsv), np.array(upper_hsv))
                if current_box:
                    box = current_box
                    mask = current_mask
                    break
                if combined_mask is None:
                    combined_mask = current_mask
                else:
                    combined_mask = cv2.bitwise_or(combined_mask, current_mask)
            mask = combined_mask
        else:
            lower_hsv = np.array(COLOR_RANGES[selected_color]['LOWER_HSV'][0])
            upper_hsv = np.array(COLOR_RANGES[selected_color]['UPPER_HSV'][0])
            box, mask = detect_colored_object(frame, lower_hsv, upper_hsv)

        if box:
            draw_bounding_box(frame, box, label=f"{selected_color.capitalize()} Object")

        # Display selected color and instructions on frame
        cv2.putText(frame, f"Color: {selected_color.capitalize()}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Select: p (pink), b (blue), y (yellow), g (green), w (white), o (orange)",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        # Show frames
        if SHOW_MASK and mask is not None:
            show_frames(frame, mask)
        else:
            show_frames(frame)

        # Exit on 'q'
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()