from pygame.locals import *

# The control for each function

WALK_LEFT = K_a
WALK_RIGHT = K_d
JUMP = K_w
ACTION = K_SPACE
CROUCH = K_LCTRL


def get_key(e):
    return e.char
