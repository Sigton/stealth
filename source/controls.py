import pygame
from pygame.locals import *

# The control for each function

WALK_LEFT = K_a
WALK_RIGHT = K_d
JUMP = K_w
ACTION = K_SPACE
CROUCH = K_LCTRL


def get_last_key():

    key = None

    key_pressed = False
    while not key_pressed:
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        print(keys)
        if 1 in keys:
            key = keys.index(1)
            key_pressed = True

    return key
