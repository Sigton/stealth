# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (127, 0, 0)

# Screen Dimensions
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

# Player attributes
# These define how the player feels in movement
PLAYER_SPEED = 1.3
PLAYER_GRAVITY = 0.5
PLAYER_FRICTION = 0.8
PLAYER_JUMP_HEIGHT = 10.5
PLAYER_CLIMB_SPEED = 2

# Guard attributes
GUARD_SPEED = 1

HGUARD_SPEED = 3
HGUARD_FOLLOW_DIST = 400
HGUARD_FRICTION = 0.8


# Sets all of the variables to
# new values depending on the given screen size
def set_screen_size(new_width, new_height):

    # We are using the variables from the global scope
    global SCREEN_WIDTH, SCREEN_HEIGHT, SIZE, SCREEN_CENTER

    # Assign the new values
    SCREEN_WIDTH = new_width
    SCREEN_HEIGHT = new_height

    SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    # And return the size of the new screen
    return SIZE
