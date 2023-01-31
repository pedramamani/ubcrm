from wheel_vision import WheelVision
from constants import *
import cv2

feed = cv2.VideoCapture('../videos/Red_LightsOff_Rotating.mov')

#frameDims = (577, 577)
feedDims = (1920, 1080)
vision = WheelVision(feed, feedDims, 'BGR', wheelRad=320, wheelCntr=(1005, 490))
vision.run(modeCalib=False, showPlot=True, showDisp=True)
