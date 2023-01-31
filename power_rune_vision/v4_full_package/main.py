from wheel_vision import WheelVision
import cv2

feed = cv2.VideoCapture('../videos/Red_LightsOn_Rotating.mov')
vision = WheelVision(feed, (1920, 1080), 'BGR', (1010, 470), 800)
vision.run(modeCalib=True, showPlot=False, showDisp=True, contRecntr=True)
