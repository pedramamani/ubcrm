from scipy.signal import find_peaks
import cv2
from math import sin, cos, tan
from constants import *
import matplotlib.pyplot as plt


# copied from frameAnalyzer - modified
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
                roiCalib[y][x] = 0
            if frame[y][x] >= LUM_THRESH_MASK:
                lumSum += frame[y][x]
    return lumSum/cntPixels


# copied from frameAnalyzer - modified
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
    lumValsPeak = lumVals + lumVals[0:CNT_INC_SPACING]
    peaks, properties = find_peaks(lumValsPeak, height=(LUM_THRESH_NOISE, None), distance=CNT_INC_DIST_THRESH)

    if len(peaks) == 0:
        return None, None, [STATE_INACTIVE] * CNT_PANELS

    anglePanels, lumPanels, statePanels = [], [], []
    for peak in peaks:
        if (peak <= CNT_INC_FULL and
            not (peak in range(CNT_INC_SPACING-2) and not (peak+CNT_INC_FULL) in peaks)):
            anglePanels += [(int(peak) * ANGLE_INC) % 360]
            lumPanels += [lumVals[int(peak) % CNT_INC_FULL]]
            statePanels += [STATE_ACTIVATED]

    # find the panel that is activating
    indexMin = min(range(len(lumPanels)), key=lumPanels.__getitem__)
    statePanels[indexMin] = STATE_ACTIVATING

    # compute angle of panels that are off
    # it is required that there is at least one activating/activated panel
    cntPanels = len(anglePanels)

    if cntPanels > CNT_PANELS:
        if BOOL_SHOW_PLOT:
            plotPlates(lumVals, anglePanels, lumPanels, statePanels)

    while cntPanels < CNT_PANELS:
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


# plot the luminosity values and plate info for debugging
def plotPlates(lumVals, anglePanels, lumPanels, statePanels):
    angleVals = range(0, 360, ANGLE_INC)
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

    handles = []
    if STATE_ACTIVATED in statePanels:
        handles += [pointsActivated]
    if STATE_ACTIVATING in statePanels:
        handles += [pointsActivating]
    if STATE_INACTIVE in statePanels:
        handles += [pointsInactive]

    plt.plot(angleVals, [LUM_THRESH_NOISE] * CNT_INC_FULL, CLR_THRESH)
    plt.xlabel(LABEL_X)
    plt.ylabel(LABEL_Y)
    plt.legend(handles=handles)
    plt.show()


# set up feed from given video file
feed = cv2.VideoCapture(PATH_IN_VID + NAME_IN_VID)
# set up output video file write
if BOOL_WRITE_VID:
    fourcc = cv2.VideoWriter_fourcc(*FORMAT_OUT_VID)
    videoOut = cv2.VideoWriter(PATH_OUT_VID + NAME_OUT_VID, fourcc, FR_RATE_OUT_VID, SIZE_OUT_VID)

while feed.isOpened():
    ret, frame = feed.read()
    if not ret:
        break
    frame = cv2.resize(frame, (0,0), fx=SCALE_FACTOR_VID, fy=SCALE_FACTOR_VID)
    # cropping region of interest that contains the rune/wheel only from video
    roi = frame[COORDS_RUNE_CNTR_VID[1] - RAD_RUNE : COORDS_RUNE_CNTR_VID[1] + RAD_RUNE,
        COORDS_RUNE_CNTR_VID[0] - RAD_RUNE : COORDS_RUNE_CNTR_VID[0] + RAD_RUNE]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    if BOOL_RUN_CALIB:
        roiCalib = roi.copy()

    # obtain luminosity values for all angles
    lumVals = []
    angleVals = range(0, 360, ANGLE_INC)
    for angle in angleVals:
        lumVals += [calcLumVal(roi, angle)]
        if BOOL_RUN_CALIB:
            cv2.circle(roiCalib, (RAD_RUNE, RAD_RUNE), RAD_CIRCLE_CALIB, CLR_CIRCLE_CALIB, -1)
            cv2.imshow(TITLE_WINDOW_CALIB, roiCalib)
            cv2.waitKey(DELAY_CALIB_MS)

    # obtain angle, luminosity value and state of all five panels
    anglePanels, _, statePanels = findPanels(lumVals)

    # indicate the activating cell with a marker
    if anglePanels != None:
        for i in range(CNT_PANELS):
            if statePanels[i] == STATE_ACTIVATING:
                angleAim = anglePanels[i]
        coordsAim = (int(COORDS_RUNE_CNTR_VID[0] + RAD_TARGET * sin(angleAim * DEG_TO_RAD)),
            int(COORDS_RUNE_CNTR_VID[1] - RAD_TARGET * cos(angleAim * DEG_TO_RAD)))
        #cv2.circle(frame, coordsAim, RAD_CIRCLE_AIM, CLR_CIRCLE_AIM, -1)
        cv2.line(frame, (coordsAim[0], 0), (coordsAim[0], SIZE_IN_VID[1]), CLR_CIRCLE_AIM, 1)
        cv2.line(frame, (0, coordsAim[1]), (SIZE_IN_VID[0], coordsAim[1]), CLR_CIRCLE_AIM, 1)

    # display simulation of algorithm running on video
    if not BOOL_RUN_CALIB:
        cv2.imshow(TITLE_WINDOW_VID, frame)
        if BOOL_WRITE_VID:
            videoOut.write(frame)
        cv2.waitKey(DELAY_VID_MS)

feed.release()
cv2.destroyAllWindows()
