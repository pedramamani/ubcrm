from constants import *
from numpy import sin, cos

class LimitsExceededException(Exception):
    def __init__(self, parameter, value, range=None):
        if range is None:
            message = parameter + ', ' + str(value) + ', exceeded allowed range.'
        else:
            message = parameter + ', ' + str(value) + ', exceeded allowed range [' + str(range[0]) + ', ' + str(range[1]) + '].'
        super().__init__(message)


def checkRelativeChassisAngle(value, boolRaise):
    if valueOutOfRange(value, RANGE_ANGLE_CHASSIS_RELATIVE):
        if boolRaise:
            raise LimitsExceededException('Relative Chassis Angle', value, RANGE_ANGLE_CHASSIS_RELATIVE)
        else:
            return False
    else:
        return True

def checkRobotXPosition(value, angleChassis, boolRaise):
    if MODE_EXCEPTION == MODE_EXCEPTION_LENIENT and valueOutOfRange(value, RANGE_X_SIMPLE_ROBOT):
        if boolRaise:
            raise LimitsExceededException('Robot X Position', value, RANGE_X_SIMPLE_ROBOT)
        else:
            return False
    elif (MODE_EXCEPTION == MODE_EXCEPTION_STRICT and
    (valueOutOfRange(value + Y_TORRET_RELATIVE * sin(angleChassis) - X_TORRET_RELATIVE * cos(angleChassis), RANGE_X) or
    valueOutOfRange(value + Y_TORRET_RELATIVE * sin(angleChassis) + (LENGTH_CHASSIS - X_TORRET_RELATIVE) * cos(angleChassis), RANGE_X) or
    valueOutOfRange(value - Y_TORRET_RELATIVE * sin(angleChassis) + (LENGTH_CHASSIS - X_TORRET_RELATIVE) * cos(angleChassis), RANGE_X) or
    valueOutOfRange(value - Y_TORRET_RELATIVE * sin(angleChassis) - X_TORRET_RELATIVE * cos(angleChassis), RANGE_X))):
        if boolRaise:
            raise LimitsExceededException('Robot X Position', value)
        else:
            return False
    else:
        return True

def checkRobotYPosition(value, angleChassis, boolRaise):
    if MODE_EXCEPTION == MODE_EXCEPTION_LENIENT and valueOutOfRange(value, RANGE_Y_SIMPLE_ROBOT):
        if boolRaise:
            raise LimitsExceededException('Robot Y Position', value, RANGE_Y_SIMPLE_ROBOT)
        else:
            return False
    elif (MODE_EXCEPTION == MODE_EXCEPTION_STRICT and
    (valueOutOfRange(value - Y_TORRET_RELATIVE * cos(angleChassis) - X_TORRET_RELATIVE * sin(angleChassis), RANGE_Y) or
    valueOutOfRange(value - Y_TORRET_RELATIVE * cos(angleChassis) + (LENGTH_CHASSIS - X_TORRET_RELATIVE) * sin(angleChassis), RANGE_Y) or
    valueOutOfRange(value + Y_TORRET_RELATIVE * cos(angleChassis) + (LENGTH_CHASSIS - X_TORRET_RELATIVE) * sin(angleChassis), RANGE_Y) or
    valueOutOfRange(value + Y_TORRET_RELATIVE * cos(angleChassis) - X_TORRET_RELATIVE * sin(angleChassis), RANGE_Y))):
        if boolRaise:
            raise LimitsExceededException('Robot Y Position', value)
        else:
            return False
    else:
        return True

def valueOutOfRange(value, range):
    return (value < range[0] or value > range[1])
