''' RoboMaster Power Rune Vision

This code enables recognition of the 'Activating' target panel on the power rune in the 2019 RoboMaster challenge 'Standard Racing & Smart Firing' to be shot. Both a one-time recognition (image) and a continuous recognition (video) option are available.

Running this code requires the following packages to be installed:
    - numpy: NumPy, fundamental scientific computing package
    - scipy: SciPy, scientific computing package
    - cv2: OpenCV, computer vision and machine learning package
    - matplotlib: 2D plotting package

The file "constants.py" containing default values and constants should be placed in the same directory as this file.
'''

from math import sin, cos, tan
import time
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import cv2
import numpy as np
from constants import *


class WheelVision():
    def __init__(self, source, sourceDims, colorSpace, wheelRad=None, wheelCntr=None):
        self.src = source
        self.srcDims = sourceDims
        self.clrSrc = colorSpace
        self.frame = None

        # TODO: FIX THESE AFTER IMPLEMENTING SELF-DIMENSION RECOGNITION ALGORITHM
        if wheelRad is None:
            self.wheelRad = round((sourceDims[1]/2) / FRAME_H_DIM * WHEEL_RAD)
        else:
            self.wheelRad = wheelRad
        if wheelCntr is None:
            self.wheelCntr = (round(sourceDims[0]/2), round(sourceDims[1]/2))
        else:
            self.wheelCntr = wheelCntr

        (x0, y0) = self.wheelCntr
        scaleFactor = WHEEL_RAD / self.wheelRad
        self.cropTL = (max(0, round(x0 - FRAME_H_DIM/scaleFactor)), max(0, round(y0 - FRAME_H_DIM/scaleFactor)))
        self.cropBR = (min(sourceDims[0] - 1, round(x0 + FRAME_H_DIM/scaleFactor)), min(sourceDims[1] - 1, round(y0 + FRAME_H_DIM/scaleFactor)))

        self.panelCntActive = None
        self.panelAngles = None
        self.panelDenss = None
        self.panelStates = None
        self.panelActivatingAngle = None
        self.wheelStatus = STATUS_PREP
        self.wheelRotDir = -1 # -1 indicates CW and +1 indicates CCW rotation of wheel

        # TODO: REMOVE THESE DEBUG OPTIONS IN THE FINAL VERSION OF THE CODE
        self.showDisp = None
        self.showPlot = None
        self.showTime = None
        self.timeStart = None
        self.timeStop = None
        self.cntFrames = 0


    # ---------- HANDLING DIFFERENT MODES OF EXECUTION ---------- #
    def run(self, modeCalib=False, showDisp=True, showPlot=True, showTime=True):

        self.timeStart = time.time()
        self.showDisp = showDisp
        self.showPlot = showPlot
        self.showTime = showTime

        if modeCalib:
            modeFunc = self.calib
        else:
            modeFunc = self.bare

        while self.updateFrame():
            self.cntFrames += 1
            modeFunc()

        self.timeStop = time.time()
        if self.showTime:
            self.printTime()

    def calib(self):
        self.convertColor('B&W', 'BGR')
        for angle in ANGLE_VALS:
            self.paintMask(angle)

        cv2.circle(self.frame, WHEEL_CNTR, 3, (0,0,255), -1)
        cv2.circle(self.frame, WHEEL_CNTR, TARGET_RAD, (0,0,255), 2)
        cv2.circle(self.frame, WHEEL_CNTR, WHEEL_RAD, (0,255,0), 2)

        cv2.imshow('Calibration', self.frame)
        cv2.waitKey(50)

    def bare(self):

        densVals = []
        for angle in ANGLE_VALS:
            #densVals += [self.calcDens(angle)]
            if self.wheelStatus == STATUS_SHOOT and len(self.panelAngles) == 5:
                if self.isInNbhd(angle, self.panelAngles, ANGLE_ESTIMATE_DIST):
                    densVals += [self.calcDens(angle)]
                else:
                    densVals += [0]
            else:
                densVals += [self.calcDens(angle)]

        self.findTarget(densVals)


        if self.showDisp:
            self.convertColor('B&W', 'BGR')
            if self.wheelStatus == STATUS_SHOOT:
                angleTarget = self.panelActivatingAngle * DEG_TO_RAD
                coordsTarget = (round(WHEEL_CNTR[0] + TARGET_RAD * sin(angleTarget)),
                                round(WHEEL_CNTR[1] - TARGET_RAD * cos(angleTarget)))
                cv2.circle(self.frame, coordsTarget, 5, (0,0,255), -1)
            cv2.imshow('Bare', self.frame)
            cv2.waitKey(10)



    # ---------- OBTAINING AND PROCESSING OF A FRAME ---------- #
    def updateFrame(self):
        self.frame = self.readNextFrame()
        if self.frame is not None:
            self.cropAndResize(self.cropTL, self.cropBR, (2*FRAME_H_DIM, 2*FRAME_H_DIM))
            self.convertColor(self.clrSrc, 'B&W')
            return True
        else:
            return False

    def readNextFrame(self):
        ret, frame = self.src.read()
        if ret:
            return frame
        else:
            return None

    def cropAndResize(self, coordsTL, coordsBR, newDims):
        self.frame = self.frame[coordsTL[1] : coordsBR[1], coordsTL[0] : coordsBR[0]]
        self.frame = cv2.resize(self.frame, newDims)

    def convertColor(self, clrFrame, clrNew):

        if clrFrame != clrNew:
            if clrFrame == 'B&W':
                self.convertColor('GRAY', clrNew)
            elif clrNew == 'B&W':
                self.convertColor(clrFrame, 'GRAY')
                _, self.frame = cv2.threshold(self.frame, LUM_THRESH_BIN, LUM_MAX, cv2.THRESH_BINARY)
            else:
                conversion = eval('cv2.COLOR_' + clrFrame + '2' + clrNew)
                self.frame = cv2.cvtColor(self.frame, conversion)


    # ---------- FOR DEBUGGING AND OPTIMIZATION PURPOSES ---------- #
    def paintMask(self, angle):
        angle *= DEG_TO_RAD
        x0 = WHEEL_CNTR[0] + MASK_RAD * sin(angle)
        y0 = WHEEL_CNTR[1] - MASK_RAD * cos(angle)
        for y in range(round(y0 - MASK_H_LEN), round(y0 + MASK_H_LEN)):
            for x in range(round(x0 - MASK_H_LEN), round(x0 + MASK_H_LEN)):
                self.frame[y][x] = [255,0,0]

    def printTime(self):
        totalTime = self.timeStop - self.timeStart
        print('Frame Processing Rate: {:.3} fps'.format(self.cntFrames / totalTime))
        print('Total Execution Time: {:.3} s'.format(totalTime))

    def plot(self, densVals):
            plt.plot(ANGLE_VALS, densVals)
            plt.plot(ANGLE_VALS, [DENS_THRESH_LOW] * INC_ANGLE_MAX, 'red')
            plt.plot(ANGLE_VALS, [DENS_THRESH_HIGH] * INC_ANGLE_MAX, 'red')

            for angle, dens, state in zip(self.panelAngles, self.panelDenss, self.panelStates):
                if state == STATE_ACTIVE:
                    pointsActive, = plt.plot(angle, dens, 's', mfc='black', mec='black', label='Active')
                elif state == STATE_ACTIVATING:
                    pointsActivating, = plt.plot(angle, dens, '^', mfc='black', mec='black', label='Activating')
                elif state == STATE_INACTIVE:
                    pointsInactive, = plt.plot(angle, dens, 'o', mfc='black', mec='black', label='Inactive')

            handles = []
            if STATE_ACTIVE in self.panelStates:
                handles += [pointsActive]
            if STATE_ACTIVATING in self.panelStates:
                handles += [pointsActivating]
            if STATE_INACTIVE in self.panelStates:
                handles += [pointsInactive]

            plt.xlabel('Angle [°]')
            plt.ylabel('Sample dens [0-1]')
            plt.legend(handles=handles)
            plt.show()


    # ---------- CORE ALGORITHM EXECUTION ---------- #
    def calcDens(self, angle):
        angle *= DEG_TO_RAD
        x0 = WHEEL_CNTR[0] + MASK_RAD * sin(angle)
        y0 = WHEEL_CNTR[1] - MASK_RAD * cos(angle)
        cntWhites = 0
        cntPixels = 0
        for y in range(round(y0 - MASK_H_LEN), round(y0 + MASK_H_LEN)):
            for x in range(round(x0 - MASK_H_LEN), round(x0 + MASK_H_LEN)):
                cntPixels += 1
                if self.frame[y][x]:
                    cntWhites += 1
        return cntWhites / cntPixels

    def findTarget(self, densVals):

        densValsPeak = densVals + densVals[0 : INC_ANGLE_SEP]
        peaks, properties = find_peaks(densValsPeak, height=(DENS_THRESH_LOW, None), distance=INC_ANGLE_NBHD)
        self.processPeaks(peaks, densVals)

        if (0 <= self.panelCntActive <= 3) and (STATE_ACTIVATING in self.panelStates):
            self.estimateInactives(densVals)

        if (0 <= self.panelCntActive <= 4) and (STATE_ACTIVATING in self.panelStates):
            self.wheelStatus = STATUS_SHOOT
        elif self.panelCntActive == 0:
            self.wheelStatus = STATUS_PREP
        elif self.panelCntActive == 5:
            self.wheelStatus = STATUS_DONE
        elif len(self.panelAngles) > 5:
            print('Debug! More than 5 panels detected:', self.panelAngles)
            if self.showPlot:
                self.plot(densVals)



    # ---------- BUILDING BLOCKS OF CORE ALGORITHM ---------- #
    def isInNbhd(self, newAngle, angles, distThresh):
        for angle in angles:
            dist = (newAngle - angle) % ANGLE_MAX
            if  (dist <= distThresh) or (ANGLE_MAX - dist <= distThresh):
                return True
        return False

    def processPeaks(self, peaks, densVals):
        self.panelAngles, self.panelDenss, self.panelStates = [], [], []
        self.panelCntActive = 0
        self.panelActivatingAngle = None

        if len(peaks) > 0:
            for peak in peaks:
                # TODO: CHECK IF THESE CONDITIONS FOR PERIODIC BOUNDARIES MAKE SENSE
                if (peak + INC_ANGLE_MAX in peaks) or (peak > INC_ANGLE_SEP - 2) and (peak <= INC_ANGLE_MAX):
                    self.panelAngles += [(int(peak) * ANGLE_INC) % ANGLE_MAX]
                    self.panelDenss += [densVals[int(peak) % INC_ANGLE_MAX]]
                    self.panelStates += [STATE_ACTIVE]
                    self.panelCntActive += 1

            indexMin = min(range(self.panelCntActive), key=self.panelDenss.__getitem__)
            if (self.panelCntActive < 5) or (self.panelDenss[indexMin] <= DENS_THRESH_HIGH):
                self.panelStates[indexMin] = STATE_ACTIVATING
                self.panelActivatingAngle = self.panelAngles[indexMin]
                self.panelCntActive -= 1

    def estimateInactives(self, densVals):
        cntPanels = len(self.panelAngles)

        while cntPanels < 5:
            angleOff = self.panelAngles[cntPanels - 1]
            angleOffAdjust = 0

            cntLoops = 0
            while self.isInNbhd(angleOff, self.panelAngles, ANGLE_NBHD):
                angleOff = (angleOff + ANGLE_SEP) % ANGLE_MAX
                cntLoops += 1
                if cntLoops >= 5:
                    print(angleOff, self.panelAngles)
                    return

            for angle in self.panelAngles[0 : cntPanels - 1]:
                angleOffAdjust += angle - angleOff
            angleOffAdjust = angleOffAdjust % ANGLE_SEP

            if ANGLE_SEP - ANGLE_ESTIMATE_DIST * cntPanels < angleOffAdjust < ANGLE_SEP:
                angleOffAdjust -= ANGLE_SEP
            angleOffAdjust = angleOffAdjust / cntPanels
            angleOff += round(angleOffAdjust / ANGLE_INC) * ANGLE_INC
            angleOff = angleOff % ANGLE_MAX

            self.panelAngles += [angleOff]
            self.panelDenss += [densVals[int(angleOff / ANGLE_INC)]]
            self.panelStates += [STATE_INACTIVE]
            cntPanels += 1
