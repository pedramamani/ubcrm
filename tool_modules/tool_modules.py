from data_tools.data_tools import json_to_csv
from image_tools.image_tools import crop_about_gui
import cv2

with open("assets/data.json", 'r') as in_file:
    json_to_csv(in_file, "data.csv")

image = cv2.imread("assets/image.png")
crop_about_gui(image, (200, 100), "assets/cropped.png")
