import numpy as np

# power rune dimensions (all values are relative to rune radius)
RAD_RUNE = 80
RAD_TARGET = int(0.92 * RAD_RUNE)

# video constants
RAD_RUNE_VID = 310
SCALE_FACTOR_VID = RAD_RUNE / RAD_RUNE_VID
COORDS_RUNE_CNTR_VID = (int(990 * SCALE_FACTOR_VID),
                        int(490 * SCALE_FACTOR_VID))
DELAY_VID_MS = 1

TITLE_WINDOW_VID = 'Simulation'
RAD_CIRCLE_AIM = int(0.06 * RAD_RUNE)
CLR_CIRCLE_AIM = (0, 0, 255)
RAD_CIRCLE_CALIB = int(0.05 * RAD_RUNE)
CLR_CIRCLE_CALIB = 0

# video read and save parameters
PATH_FRAME = '../images/'
NAME_FRAME = 'frame_lit.png'
PATH_IN_VID = '../videos/'
NAME_IN_VID = 'Red_LightsOff_Rotating.mov'
SIZE_IN_VID = (1920, 1080)
PATH_OUT_VID = '../videos/sims/'
NAME_OUT_VID = 'demo_rotating_lit_1.mp4'
FORMAT_OUT_VID = 'MP4V'
SIZE_OUT_VID = (int(round(SIZE_IN_VID[0] * SCALE_FACTOR_VID)),
                int(round(SIZE_IN_VID[1] * SCALE_FACTOR_VID)))
FR_RATE_OUT_VID = 20.0
BOOL_WRITE_VID = True

# mask component dimensions (all values are relative to wheel radius)
WIDTH_HALF_MASK = int(0.04 * RAD_RUNE)
RAD_MIN_MASK = int(0.5 * RAD_RUNE)
RAD_MAX_MASK = int(0.70 * RAD_RUNE)
BOOL_RUN_CALIB = False
DELAY_CALIB_MS = 1
TITLE_WINDOW_CALIB = 'Frame Neg-Masked'

# angle constants (all values in degrees)
DEG_TO_RAD = np.pi / 180
ANGLE_INC = 2  # choose a divisor of 72 (i.e. 1,2,3,4,6,...)
CNT_PANELS = 5
ANGLE_SPACING = int(360 / CNT_PANELS)
CNT_INC_SPACING = int(ANGLE_SPACING / ANGLE_INC)
CNT_INC_FULL = int(360 / ANGLE_INC)
# the neighbourhood of an angle searched for its corresponding panel
ANGLE_NBHD = max(3, 2 * ANGLE_INC)
CNT_INC_NBHD = int(ANGLE_NBHD / ANGLE_INC)

# luminosity and peak constants
LUM_MAX = 255
LUM_THRESH_MASK = 0.85 * LUM_MAX
LUM_THRESH_NOISE = 0.35 * LUM_MAX
CNT_INC_DIST_THRESH = 0.8 * CNT_INC_SPACING

# plot options
BOOL_SHOW_PLOT = False
CLR_THRESH = 'red'
LABEL_X = 'Angle [°]'
LABEL_Y = 'Net Luminosity [0-255]'
MARKER_ACTIVATED = 's'
MARKER_ACTIVATING = '^'
MARKER_INACTIVE = 'o'
LABEL_ACTIVATED = 'Activated'
LABEL_ACTIVATING = 'Activating'
LABEL_INACTIVE = 'Inactive'
CLR_MARKER_STATE = 'black'

# target panel states
STATE_ACTIVATED = '1'
STATE_ACTIVATING = 'A'
STATE_INACTIVE = '-'
