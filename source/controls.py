import pygame
from pygame.locals import *

# The control for each function

WALK_LEFT = K_a
WALK_RIGHT = K_d
JUMP = K_w
ACTION = K_SPACE
CROUCH = K_LCTRL


def get_last_key():

    key_pressed = False
    while not key_pressed:

        for event in pygame.event.get():
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    return None

                else:
                    return event.key
