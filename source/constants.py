# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen Dimensions
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Player attributes
PLAYER_SPEED = 1.3
PLAYER_GRAVITY = 0.5
PLAYER_FRICTION = 0.8
PLAYER_JUMP_HEIGHT = 10.5
PLAYER_CLIMB_SPEED = 2

# Guard attributes
GUARD_SPEED = 1.5

HGUARD_SPEED = 2
HGUARD_FOLLOW_DIST = 500
HGUARD_FRICTION = 0.8


# Sets the screen to a new size
def set_screen_size(new_width, new_height):

    global SCREEN_WIDTH, SCREEN_HEIGHT, SIZE

    SCREEN_WIDTH = new_width
    SCREEN_HEIGHT = new_height

    SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    return SIZE
