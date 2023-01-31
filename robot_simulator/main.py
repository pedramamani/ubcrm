from graphics import *
from time import sleep
from constants import *
from robot import Robot


# initialize robot state parameters
xRobot = LENGTH_CHASSIS + 0.2
yRobot = LENGTH_CHASSIS + 0.2
angleTorret = 30 * DEGREE_TO_RAD
angleChassisRelative = -90 * DEGREE_TO_RAD

window = GraphWin(TITLE_WINDOW, WIDTH_WINDOW, HEIGHT_WINDOW, autoflush=False)
window.setCoords(0, 0, WIDTH_WINDOW, HEIGHT_WINDOW)
robot = Robot(xRobot, yRobot, angleTorret, angleChassisRelative, window)
robot.adaptiveSwirlCtrl()

window.close()
