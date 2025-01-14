import sys
import yaml
from detectMotion import detectMotion
import os

video_path = "./videos/"
image_path = "./images/"
coordinates_path = "./coordinates/"

# get the video name with extension from the command line argument
video_name_with_extension = sys.argv[1]

# separate the video name and extension
video_name, video_extension = os.path.splitext(video_name_with_extension)

# Create the paths for the video and coordinates file
video_file = os.path.join(video_path, video_name_with_extension)
coordinates_file = os.path.join(coordinates_path, f"{video_name}.yml")


# Load coordinates from YAML file
try:
  with open(coordinates_file, "r") as data:
      points = yaml.safe_load(data)
except FileNotFoundError:
   print("The video needs to be preprocessed first!")
   print("Use the command: py preprocess.py <video-file>")
   sys.exit(0)

# Initialize motion detector and run motion detection
detector = detectMotion(video_file, points)
detector.detect()
