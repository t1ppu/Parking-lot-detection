import sys
import cv2
import os
from generateCoordinates import generateCoordinates
import time

video_path = "./videos/"
image_path = "./images/"
coordinates_path = "./coordinates/"

# get the video name with extension from the command line argument
video_name_with_extension = sys.argv[1]

# separate the video name and extension
video_name, video_extension = os.path.splitext(video_name_with_extension)

video_file = os.path.join(video_path, video_name_with_extension)


# Capture the first frame from the video
capture = cv2.VideoCapture(video_file)
ret, first_frame = capture.read()
if not ret:
        print(f"Error: Could not read the first frame from the video {video_file}")
        sys.exit(1)

# Save the first frame as an image
image_file = image_path + video_name + ".png"
cv2.imwrite(image_file, first_frame)

# generate YML file for coordinates
data_file = os.path.join(coordinates_path, f"{video_name}.yml")
with open(data_file, "w+") as f:
    print("--- Click on the four corners of a parking space to mark it. Press 'q' to exit ---")
    time.sleep(2)
    generator = generateCoordinates(image_file, f)
    generator.generate()

# success message
print("Preprocessing completed successfully!")