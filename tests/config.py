# Camera Settings
CAMERA_INDEX = 0  # Use 0 for default webcam

# HSV Color Range for detecting blue
# These values may need fine-tuning based on lighting conditions
# LOWER_HSV = (100, 150, 50)
# UPPER_HSV = (140, 255, 255)

# HSV Color Range for detecting yellow
LOWER_HSV = (20, 100, 100)
UPPER_HSV = (40, 255, 255)

# Tracker Settings (if you use tracking algorithms later)
TRACKER_TYPE = 'CSRT'

# Window Settings
SHOW_MASK = True
WINDOW_NAME = "Blue Object Tracker"