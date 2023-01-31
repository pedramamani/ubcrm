from constants import *
from graphics import *
from numpy import sin, cos
from exceptions import *
from keyboard import is_pressed
from time import sleep

class Robot:
    '''
        Represent the state of a Robot with a torret in a 2D plane.
    '''

    def __init__(self, xInit, yInit, angleTorretInit, angleChassisRelativeInit, window):
        if not MODE_EXCEPTION == MODE_EXCEPTION_OFF:
            checkRobotXPosition(xInit, angleTorretInit + angleChassisRelativeInit, True)
            checkRobotYPosition(yInit, angleTorretInit + angleChassisRelativeInit, True)
            checkRelativeChassisAngle(angleChassisRelativeInit, True)

        self.x = xInit
        self.y = yInit
        self.angleTorret = angleTorretInit % (2 * PI)
        self.angleChassisRelative = angleChassisRelativeInit
        self.window = window
        self.draw()


    def draw(self):
        for item in self.window.items[:]:
            item.undraw()

        angleChassis = self.angleTorret + self.angleChassisRelative
        chassis = Polygon([
        Point((self.x + Y_TORRET_RELATIVE * sin(angleChassis) - X_TORRET_RELATIVE * cos(angleChassis)) * FACTOR_SCALE,
        (self.y - Y_TORRET_RELATIVE * cos(angleChassis) - X_TORRET_RELATIVE * sin(angleChassis)) * FACTOR_SCALE),
        Point((self.x + Y_TORRET_RELATIVE * sin(angleChassis) + (LENGTH_CHASSIS - X_TORRET_RELATIVE) * cos(angleChassis)) * FACTOR_SCALE,
        (self.y - Y_TORRET_RELATIVE * cos(angleChassis) + (LENGTH_CHASSIS - X_TORRET_RELATIVE) * sin(angleChassis)) * FACTOR_SCALE),
        Point((self.x - Y_TORRET_RELATIVE * sin(angleChassis) + (LENGTH_CHASSIS - X_TORRET_RELATIVE) * cos(angleChassis)) * FACTOR_SCALE,
        (self.y + Y_TORRET_RELATIVE * cos(angleChassis) + (LENGTH_CHASSIS - X_TORRET_RELATIVE) * sin(angleChassis)) * FACTOR_SCALE),
        Point((self.x - Y_TORRET_RELATIVE * sin(angleChassis) - X_TORRET_RELATIVE * cos(angleChassis)) * FACTOR_SCALE,
        (self.y + Y_TORRET_RELATIVE * cos(angleChassis) - X_TORRET_RELATIVE * sin(angleChassis)) * FACTOR_SCALE)])

        torret = Polygon([
        Point((self.x + WIDTH_TORRET/2 * sin(self.angleTorret)) * FACTOR_SCALE,
        (self.y - WIDTH_TORRET/2 * cos(self.angleTorret)) * FACTOR_SCALE),
        Point((self.x + WIDTH_TORRET/2 * sin(self.angleTorret) + LENGTH_TORRET * cos(self.angleTorret)) * FACTOR_SCALE,
        (self.y - WIDTH_TORRET/2 * cos(self.angleTorret) + LENGTH_TORRET * sin(self.angleTorret)) * FACTOR_SCALE),
        Point((self.x - WIDTH_TORRET/2 * sin(self.angleTorret) + LENGTH_TORRET * cos(self.angleTorret)) * FACTOR_SCALE,
        (self.y + WIDTH_TORRET/2 * cos(self.angleTorret) + LENGTH_TORRET * sin(self.angleTorret)) * FACTOR_SCALE),
        Point((self.x - WIDTH_TORRET/2 * sin(self.angleTorret)) * FACTOR_SCALE,
        (self.y + WIDTH_TORRET/2 * cos(self.angleTorret)) * FACTOR_SCALE)])
        torret.setFill(COLOR_FILL_TORRET)

        baseTorret = Circle(Point(self.x * FACTOR_SCALE, self.y * FACTOR_SCALE), RADIUS_BASE_TORRET * FACTOR_SCALE)
        baseTorret.setFill(COLOR_FILL_BASE_TORRET)

        if BOOL_LINES_SWIRL:
            angleSwirlMax = self.angleTorret + ANGLE_CENTER_SWIRL_RELATIVE + ANGLE_RANGE_SWIRL / 2
            angleSwirlMin = self.angleTorret + ANGLE_CENTER_SWIRL_RELATIVE - ANGLE_RANGE_SWIRL / 2
            lineLimitSwirlMax = Line(Point(self.x * FACTOR_SCALE, self.y * FACTOR_SCALE),
                Point((self.x + LENGTH_LINE_LIMIT_SWIRL * cos(angleSwirlMax)) * FACTOR_SCALE, (self.y + LENGTH_LINE_LIMIT_SWIRL * sin(angleSwirlMax)) * FACTOR_SCALE))
            lineLimitSwirlMax.setOutline(COLOR_LINES_SWIRL)
            lineLimitSwirlMin = Line(Point(self.x * FACTOR_SCALE, self.y * FACTOR_SCALE),
                Point((self.x + LENGTH_LINE_LIMIT_SWIRL * cos(angleSwirlMin)) * FACTOR_SCALE, (self.y + LENGTH_LINE_LIMIT_SWIRL * sin(angleSwirlMin)) * FACTOR_SCALE))
            lineLimitSwirlMin.setOutline(COLOR_LINES_SWIRL)

            vectChassis = Line(Point(self.x * FACTOR_SCALE, self.y * FACTOR_SCALE),
                Point((self.x + LENGTH_VECT_CHASSIS * cos(angleChassis)) * FACTOR_SCALE, (self.y + LENGTH_VECT_CHASSIS * sin(angleChassis)) * FACTOR_SCALE))
            vectChassis.setArrow('last')
            vectChassis.setOutline(COLOR_LINES_SWIRL)

            lineLimitSwirlMax.draw(self.window)
            lineLimitSwirlMin.draw(self.window)
            vectChassis.draw(self.window)

        chassis.draw(self.window)
        torret.draw(self.window)
        baseTorret.draw(self.window)
        self.window.update()


    def translate(self, deltaXRobot, deltaYRobot):
        if ((checkRobotXPosition(self.x + deltaXRobot, self.angleTorret + self.angleChassisRelative, (not BOOL_EXCEPTION_AVOID and MODE_EXCEPTION != MODE_EXCEPTION_OFF)) and
        checkRobotYPosition(self.y + deltaYRobot, self.angleTorret + self.angleChassisRelative, (not BOOL_EXCEPTION_AVOID and MODE_EXCEPTION != MODE_EXCEPTION_OFF))) or
        MODE_EXCEPTION == MODE_EXCEPTION_OFF):
            self.x += deltaXRobot
            self.y += deltaYRobot
            self.draw()

    def rotate(self, DELTA_ANGLE_ROBOT):
        if ((checkRobotXPosition(self.x, self.angleTorret + DELTA_ANGLE_ROBOT + self.angleChassisRelative, (not BOOL_EXCEPTION_AVOID and MODE_EXCEPTION != MODE_EXCEPTION_OFF)) and
        checkRobotYPosition(self.y, self.angleTorret + DELTA_ANGLE_ROBOT + self.angleChassisRelative, (not BOOL_EXCEPTION_AVOID and MODE_EXCEPTION != MODE_EXCEPTION_OFF))) or
        MODE_EXCEPTION == MODE_EXCEPTION_OFF):
            self.angleTorret += DELTA_ANGLE_ROBOT
            self.draw()

    def rotateTorret(self, DELTA_ANGLE_TORRET):
        if (checkRelativeChassisAngle(self.angleChassisRelative - DELTA_ANGLE_TORRET, (not BOOL_EXCEPTION_AVOID and MODE_EXCEPTION != MODE_EXCEPTION_OFF)) or
        MODE_EXCEPTION == MODE_EXCEPTION_OFF):
            self.angleChassisRelative -= DELTA_ANGLE_TORRET
            self.angleTorret += DELTA_ANGLE_TORRET
            self.draw()

    def rotateChassis(self, deltaAngleChassis):
        if ((checkRelativeChassisAngle(self.angleChassisRelative + deltaAngleChassis, (not BOOL_EXCEPTION_AVOID and MODE_EXCEPTION != MODE_EXCEPTION_OFF)) and
        checkRobotXPosition(self.x, self.angleTorret + deltaAngleChassis + self.angleChassisRelative, (not BOOL_EXCEPTION_AVOID and MODE_EXCEPTION != MODE_EXCEPTION_OFF)) and
        checkRobotYPosition(self.y, self.angleTorret + deltaAngleChassis + self.angleChassisRelative, (not BOOL_EXCEPTION_AVOID and MODE_EXCEPTION != MODE_EXCEPTION_OFF))) or
        MODE_EXCEPTION == MODE_EXCEPTION_OFF):
            self.angleChassisRelative += deltaAngleChassis
            self.draw()


    def uncoupledChassisBasedCtrl(self):
        while not is_pressed('esc'):
            sleep(1 / RATE_FRAME)
            self.__keyboardChassisRotationCtrl()
            self.__keyboardChassisTranslationCtrl()
            self.__keyboardTorretCtrl()

    def uncoupledGimbalBasedCtrl(self):
        while not is_pressed('esc'):
            sleep(1 / RATE_FRAME)
            self.__keyboardChassisRotationCtrl()
            self.__keyboardGimbalBasedChassisTranslationCtrl()
            self.__keyboardTorretCtrl()

    def adaptiveSwirlCtrl(self):
        boolRotationChassisCW = True

        while not is_pressed('esc'):
            sleep(1 / RATE_FRAME)
            boolUnderAngleChassis = (self.angleChassisRelative <= ANGLE_CENTER_SWIRL_RELATIVE - ANGLE_RANGE_SWIRL / 2)
            boolOverAngleChassis = (self.angleChassisRelative >= ANGLE_CENTER_SWIRL_RELATIVE + ANGLE_RANGE_SWIRL / 2)

            if (boolRotationChassisCW and boolOverAngleChassis):
                boolRotationChassisCW = False
            elif (not boolRotationChassisCW and boolUnderAngleChassis):
                boolRotationChassisCW = True

            if boolRotationChassisCW:
                self.rotateChassis(DELTA_ANGLE_ROBOT)
            else:
                self.rotateChassis(-DELTA_ANGLE_ROBOT)

            self.__keyboardGimbalBasedChassisTranslationCtrl()
            self.__keyboardTorretCtrl()


    def __keyboardChassisTranslationCtrl(self):
        if is_pressed('d'):
            self.translate(DELTA_POSITION_ROBOT, 0)
        elif is_pressed('a'):
            self.translate(-DELTA_POSITION_ROBOT, 0)
        if is_pressed('w'):
            self.translate(0, DELTA_POSITION_ROBOT)
        elif is_pressed('s'):
            self.translate(0, -DELTA_POSITION_ROBOT)

    def __keyboardGimbalBasedChassisTranslationCtrl(self):
        if is_pressed('d'):
            self.translate(DELTA_POSITION_ROBOT * sin(self.angleTorret), -DELTA_POSITION_ROBOT * cos(self.angleTorret))
        elif is_pressed('a'):
            self.translate(-DELTA_POSITION_ROBOT * sin(self.angleTorret), DELTA_POSITION_ROBOT * cos(self.angleTorret))
        if is_pressed('w'):
            self.translate(DELTA_POSITION_ROBOT * cos(self.angleTorret), DELTA_POSITION_ROBOT * sin(self.angleTorret))
        elif is_pressed('s'):
            self.translate(-DELTA_POSITION_ROBOT * cos(self.angleTorret), -DELTA_POSITION_ROBOT * sin(self.angleTorret))

    def __keyboardChassisRotationCtrl(self):
        if is_pressed('q'):
            self.rotateChassis(DELTA_ANGLE_ROBOT)
        elif is_pressed('e'):
            self.rotateChassis(-DELTA_ANGLE_ROBOT)

    def __keyboardTorretCtrl(self):
        if is_pressed('q'):
            self.rotateTorret(DELTA_ANGLE_TORRET)
        elif is_pressed('e'):
            self.rotateTorret(-DELTA_ANGLE_TORRET)
