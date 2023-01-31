'''
    Physical parameters are expressed in their real-world values and will
    only will be scaled by a factor when being drawn to the window.
    All units are SI unless specified otherwise (angles are in radians).
'''

# general constants
PI = 3.1415
DEGREE_TO_RAD = PI / 180

# window parameters
TITLE_WINDOW = "Adaptive Swirl"
LENGTH_WINDOW = 500
WIDTH_WINDOW = HEIGHT_WINDOW = LENGTH_WINDOW

LENGTH_FIELD = 4 # side length of the field
FACTOR_SCALE = LENGTH_WINDOW / LENGTH_FIELD

# robot graphics and parameters
COLOR_FILL_TORRET = 'black'
COLOR_FILL_BASE_TORRET = 'red'

WIDTH_CHASSIS = 0.4
LENGTH_CHASSIS = 0.5

WIDTH_TORRET = 0.05
LENGTH_TORRET = 0.2
RADIUS_BASE_TORRET = 0.05
X_TORRET_RELATIVE = 0.3
Y_TORRET_RELATIVE = WIDTH_CHASSIS / 2

# adaptive swirl motion parameters
ANGLE_CENTER_SWIRL_RELATIVE = 45 * DEGREE_TO_RAD
ANGLE_RANGE_SWIRL = 80 * DEGREE_TO_RAD

BOOL_LINES_SWIRL = False
LENGTH_LINE_LIMIT_SWIRL = 1
LENGTH_VECT_CHASSIS = 0.5
COLOR_LINES_SWIRL = 'blue'

# exception parameters and ranges
RANGE_ANGLE_CHASSIS_RELATIVE = (-90 * DEGREE_TO_RAD, 90 * DEGREE_TO_RAD)
RANGE_Y_SIMPLE_ROBOT = RANGE_X_SIMPLE_ROBOT = (WIDTH_CHASSIS / 2, LENGTH_FIELD - WIDTH_CHASSIS / 2)
RANGE_Y = (0, HEIGHT_WINDOW / FACTOR_SCALE)
RANGE_X = (0, LENGTH_WINDOW / FACTOR_SCALE)

MODE_EXCEPTION_STRICT = 'S' # all robot exceptions will be checked to the detriment of performance
MODE_EXCEPTION_LENIENT = 'L' # compute-intensive robot exception will not be checked to boost performance
MODE_EXCEPTION_OFF = 'O' # no robot exceptions will be checked/raised
MODE_EXCEPTION = MODE_EXCEPTION_STRICT

# avoid exceptions by restricting parameters to stay within allowed ranges (init value exceptions are not avoided)
BOOL_EXCEPTION_AVOID = True

# translation and rotation rates
SPEED_TRANSLATION_ROBOT = 2
SPEED_ROTATION_ROBOT = 200 * DEGREE_TO_RAD
SPEED_ROTATION_TORRET = 180 * DEGREE_TO_RAD

# animation parameters
RATE_FRAME = 30
DELTA_POSITION_ROBOT = SPEED_TRANSLATION_ROBOT / RATE_FRAME
DELTA_ANGLE_ROBOT = SPEED_ROTATION_ROBOT / RATE_FRAME
DELTA_ANGLE_TORRET = SPEED_ROTATION_TORRET / RATE_FRAME
