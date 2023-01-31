
# square frame with side length FRAME_H_DIM with the wheel centered with radius WHEEL_RAD
WHEEL_RAD = 100
FRAME_H_DIM = int(1.1 * WHEEL_RAD)
TARGET_RAD = int(0.87 * WHEEL_RAD)
MASK_H_LEN = int(0.05 * WHEEL_RAD)
MASK_RAD = int(0.6 * WHEEL_RAD)
WHEEL_CNTR = (FRAME_H_DIM, FRAME_H_DIM)


ANGLE_INC = 3 # choose a divisor of 72 (1, 2, 3, 4, 6, ...)
ANGLE_MAX = 360
ANGLE_SEP = 72
ANGLE_ESTIMATE_DIST = 5
ANGLE_NBHD = ANGLE_SEP - 2 * ANGLE_ESTIMATE_DIST
DEG_TO_RAD = 3.1415 / 180
ANGLE_VALS = range(0, ANGLE_MAX, ANGLE_INC)

INC_ANGLE_MAX = int(ANGLE_MAX / ANGLE_INC)
INC_ANGLE_SEP = int(ANGLE_SEP / ANGLE_INC)
INC_ANGLE_NBHD = int(ANGLE_NBHD / ANGLE_INC)

LUM_MAX = 255
LUM_THRESH_BIN = 0.85 * LUM_MAX
DENS_THRESH_LOW = 0.3
DENS_THRESH_HIGH = 0.6

ANGULAR_SPEED = 60 # degrees per second

STATE_ACTIVE = '1'
STATE_ACTIVATING = 'A'
STATE_INACTIVE = '-'

STATUS_PREP = 'p'
STATUS_SHOOT = 'x'
STATUS_DONE = '!'

#############################################################################

# # wheel dimensions (all values are relative to wheel radius)
# RAD_WHEEL = 100
#

#
# ANGLE_SEP = int(ANGLE_MAX / CNT_PANELS)
# ANGLE_NBHD = 0.75 * ANGLE_SEP
# INC_ANGLE_MAX = int(ANGLE_MAX / ANGLE_INC)
# INC_ANGLE_SEP = int(ANGLE_SEP / ANGLE_INC)
# INC_ANGLE_NBHD = int(ANGLE_NBHD / ANGLE_INC)
#
#
#
#
#
# BOOL_SHOW_PLOT = True
# BOOL_RUN_CALIB = False
# DELAY_CALIB_MS = 20
#
# # target panel states


#################################################################
'''

RAD_TARGET = int(0.92 * RAD_WHEEL)

# video constants
RAD_WHEEL_VID = 310
SCALE_FACTOR_VID = RAD_WHEEL / RAD_WHEEL_VID
COORDS_RUNE_CNTR_VID = (int(1020 * SCALE_FACTOR_VID), int(456 * SCALE_FACTOR_VID))
DELAY_VID_MS = 1

TITLE_WINDOW_VID = 'Simulation'
RAD_CIRCLE_AIM = int(0.08 * RAD_WHEEL)
CLR_CIRCLE_AIM = (0, 0, 255)
RAD_CIRCLE_CALIB = int(0.05 * RAD_WHEEL)
CLR_CIRCLE_CALIB = 0

# video read and save parameters

PATH_IN_VID = 'videos/'
NAME_IN_VID = 'Red_LightsOn_Rotating.mov'

SIZE_IN_VID = (1920, 1080)
PATH_OUT_VID = 'videos/sims/'
NAME_OUT_VID = 'demo_rotating_lit_1.mp4'
FORMAT_OUT_VID = 'MP4V'
SIZE_OUT_VID = (int(round(SIZE_IN_VID[0] * SCALE_FACTOR_VID)),
    int(round(SIZE_IN_VID[1] * SCALE_FACTOR_VID)))
FR_RATE_OUT_VID = 20.0
BOOL_WRITE_VID = False

# mask component dimensions (all values are relative to wheel radius)
WIDTH_HALF_MASK = int(0.05 * RAD_WHEEL)
RAD_MIN_MASK = int(0.6 * RAD_WHEEL)
RAD_MAX_MASK = int(0.65 * RAD_WHEEL)




# angle constants (all values in degrees)



ANGLE_SPACING = int(360 / CNT_PANELS)

INC_ANGLE_FULL = int(360 / ANGLE_INC)
# the neighbourhood of an angle searched for its corresponding panel

INC_ANGLE_NBHD = int(ANGLE_NBHD / ANGLE_INC)

# luminosity and peak constants


LUM_THRESH_NOISE = 0.05 * DENS_MAX


# plot options

CLR_THRESH = 'red'
LABEL_X = 'Angle [°]'
LABEL_Y = 'Net Luminosity [0-255]'
MARKER_ACTIVE = 's'
MARKER_ACTIVATING = '^'
MARKER_INACTIVE = 'o'
LABEL_ACTIVE = 'Active'
LABEL_ACTIVATING = 'Activating'
LABEL_INACTIVE = 'Inactive'
CLR_MARKER_STATE = 'black'
'''
