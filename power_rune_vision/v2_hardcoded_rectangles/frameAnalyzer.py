from math import sin, cos, tan
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from time import time
import cv2
from constants import *

# start timing program execution
timeStart = time()

# calculate and return a normalized sum of grayscale pixel values
# over defined mask at given angle
# most of the code in this function is to specify the area covered by mask at given angle
def calcLumVal(frame, angle):
    theta = angle * DEG_TO_RAD
    def boundLeft(x):
        bound = round(RAD_RUNE - (x+0.5-RAD_RUNE)/tan(theta) - WIDTH_HALF_MASK/sin(theta))
        if 180 <= angle < 360:
            bound -= 1
        return bound
    def boundRight(x):
        bound = round(RAD_RUNE - (x+0.5-RAD_RUNE)/tan(theta) + WIDTH_HALF_MASK/sin(theta))
        if 0 <= angle < 180:
            bound -= 1
        return bound
    def boundTop(x):
        bound = round(RAD_RUNE + (x+0.5-RAD_RUNE)*tan(theta) - RAD_MAX_MASK/cos(theta))
        if 90 <= angle < 270:
            bound -= 1
        return bound
    def boundBottom(x):
        bound = round(RAD_RUNE + (x-RAD_RUNE)*tan(theta) - RAD_MIN_MASK/cos(theta))
        if 0 <= angle < 90 or 270 <= angle < 360:
            bound -= 1
        return bound

    def xMin():
        if 0 <= angle < 90:
            value = round(RAD_RUNE + RAD_MIN_MASK*sin(theta) - WIDTH_HALF_MASK*cos(theta))
        elif 90 <= angle < 180:
            value = round(RAD_RUNE + RAD_MIN_MASK*sin(theta) + WIDTH_HALF_MASK*cos(theta))
        elif 180 <= angle < 270:
            value = round(RAD_RUNE + RAD_MAX_MASK*sin(theta) + WIDTH_HALF_MASK*cos(theta))
        elif 270 <= angle < 360:
            value = round(RAD_RUNE + RAD_MAX_MASK*sin(theta) - WIDTH_HALF_MASK*cos(theta))
        return value
    def xMax():
        if 0 <= angle < 90:
            value = round(RAD_RUNE + RAD_MAX_MASK*sin(theta) + WIDTH_HALF_MASK*cos(theta))
        elif 90 <= angle < 180:
            value = round(RAD_RUNE + RAD_MAX_MASK*sin(theta) - WIDTH_HALF_MASK*cos(theta))
        elif 180 <= angle < 270:
            value = round(RAD_RUNE + RAD_MIN_MASK*sin(theta) - WIDTH_HALF_MASK*cos(theta))
        elif 270 <= angle < 360:
            value = round(RAD_RUNE + RAD_MIN_MASK*sin(theta) + WIDTH_HALF_MASK*cos(theta))
        return value - 1
    def yMin(x):
        if angle == 0:
            return boundTop(x)
        elif 0 < angle < 90:
            return max(boundLeft(x), boundTop(x))
        elif angle == 90:
            return boundLeft(x)
        elif 90 < angle < 180:
            return max(boundBottom(x), boundLeft(x))
        elif angle == 180:
            return boundBottom(x)
        elif 180 < angle < 270:
            return max(boundRight(x), boundBottom(x))
        elif angle == 270:
            return boundRight(x)
        elif 270 < angle < 360:
            return max(boundTop(x), boundRight(x))
    def yMax(x):
        if angle == 0:
            return boundBottom(x)
        elif 0 < angle < 90:
            return min(boundBottom(x), boundRight(x))
        elif angle == 90:
            return boundRight(x)
        elif 90 < angle < 180:
            return min(boundRight(x), boundTop(x))
        elif angle == 180:
            return boundTop(x)
        elif 180 < angle < 270:
            return min(boundTop(x), boundLeft(x))
        elif angle == 270:
            return boundLeft(x)
        elif 270 < angle < 360:
            return min(boundLeft(x), boundBottom(x))

    lumSum = 0
    cntPixels = 0
    for x in range(xMin(), xMax()+1):
        for y in range(yMin(x), yMax(x)+1):
            cntPixels += 1
            if BOOL_RUN_CALIB:
                frameCalib[y][x] = 0
            if frame[y][x] >= LUM_THRESH_MASK:
                lumSum += frame[y][x]
    return lumSum/cntPixels

# find panels and their states and properties from luminosity values
def findPanels(lumVals):
    # checks if there is a peak in neighbourhood of new angle
    def isPeakInNbhd(newAngle, angles):
        isPeak = False
        for angle in angles:
            if 0 <= (newAngle - angle) % 360 <= ANGLE_NBHD or -ANGLE_NBHD <= newAngle - angle - 360 < 0:
                isPeak = True
                break
        return isPeak

    # find peaks in luminosity values corresponsing to panels that are activating/activated
    # correct for peaks at boundaries
    lumValsPeak = lumVals + lumVals[0:2]
    peaks, properties = find_peaks(lumValsPeak, height=(LUM_THRESH_NOISE, None), distance=CNT_INC_DIST_THRESH)
    anglePanels, lumPanels, statePanels = [], [], []
    for peak in peaks:
        anglePanels += [(int(peak) * ANGLE_INC) % 360]
        lumPanels += [lumVals[int(peak) % CNT_INC_FULL]]
        statePanels += [STATE_ACTIVATED]

    # find the panel that is activating
    indexMin = min(range(len(lumPanels)), key=lumPanels.__getitem__)
    statePanels[indexMin] = STATE_ACTIVATING

    # compute angle of panels that are off
    # it is required that there is at least one activating/activated panel
    cntPanels = len(anglePanels)
    while cntPanels < 5:
        angleOff = anglePanels[0]
        angleOffAdjust = 0
        while isPeakInNbhd(angleOff, anglePanels):
            angleOff = (angleOff + ANGLE_SPACING) % 360
        for angle in anglePanels[0:]:
            angleOffAdjust += angle - angleOff

        angleOffAdjust = angleOffAdjust % ANGLE_SPACING
        if ANGLE_SPACING - ANGLE_NBHD * cntPanels < angleOffAdjust < ANGLE_SPACING:
            angleOffAdjust -= ANGLE_SPACING
        angleOffAdjust = angleOffAdjust / cntPanels
        angleOff += round(angleOffAdjust / ANGLE_INC) * ANGLE_INC
        angleOff = angleOff % 360

        anglePanels += [angleOff]
        lumPanels += [lumVals[int(angleOff / ANGLE_INC)]]
        statePanels += [STATE_INACTIVE]
        cntPanels += 1

    return anglePanels, lumPanels, statePanels

# obtain square frame and resize to match defined dimensions
frame = cv2.imread(PATH_FRAME + NAME_FRAME, cv2.IMREAD_GRAYSCALE)
frame = cv2.resize(frame, (2*RAD_RUNE, 2*RAD_RUNE))
if BOOL_RUN_CALIB:
    frameCalib = frame.copy()

# obtain luminosity values for all angles
lumVals = []
angleVals = range(0, 360, ANGLE_INC)
for angle in angleVals:
    lumVals += [calcLumVal(frame, angle)]
    if BOOL_RUN_CALIB:
        cv2.imshow(TITLE_WINDOW_CALIB, frameCalib)
        cv2.waitKey(DELAY_CALIB_MS)

# obtain angle, luminosity value and state of all five panels
(anglePanels, lumPanels, statePanels) = findPanels(lumVals)

# stop timing program execution
timeFinish = time()
print('Total Run Time =', timeFinish - timeStart)

# plot the findings
if BOOL_SHOW_PLOT:
    plt.plot(angleVals, lumVals)
    for angle, lum, state in zip(anglePanels, lumPanels, statePanels):
        if state == STATE_ACTIVATED:
            pointsActivated, = plt.plot(angle, lum, MARKER_ACTIVATED,
                mfc=CLR_MARKER_STATE, mec=CLR_MARKER_STATE, label=LABEL_ACTIVATED)
        elif state == STATE_ACTIVATING:
            pointsActivating, = plt.plot(angle, lum, MARKER_ACTIVATING,
                mfc=CLR_MARKER_STATE, mec=CLR_MARKER_STATE, label=LABEL_ACTIVATING)
        elif state == STATE_INACTIVE:
            pointsInactive, = plt.plot(angle, lum, MARKER_INACTIVE,
                mfc=CLR_MARKER_STATE, mec=CLR_MARKER_STATE, label=LABEL_INACTIVE)
    plt.plot(angleVals, [LUM_THRESH_NOISE] * CNT_INC_FULL, CLR_THRESH)
    plt.xlabel(LABEL_X)
    plt.ylabel(LABEL_Y)
    plt.legend(handles=[pointsActivated, pointsActivating, pointsInactive])
    plt.show()

if BOOL_RUN_CALIB:
    cv2.destroyAllWindows()
