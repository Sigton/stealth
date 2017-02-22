import pygame
from pygame.locals import *

import menu as m
import constants


def main():

    # Main Program

    # Initiate pygame
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()

    # Set the display size
    game_display = pygame.display.set_mode(constants.SIZE)

    # Set the window caption and icon
    pygame.display.set_caption("Stealth")

    icon_img = pygame.image.load("resources/icon.ico")

    icon = pygame.Surface([32, 32], flags=SRCALPHA)
    icon = icon.convert_alpha()
    icon.blit(icon_img, (0, 0))
    pygame.display.set_icon(icon)

    # Used to manage update frequency
    clock = pygame.time.Clock()

    # Start the menu
    menu = m.Menu(game_display, clock)

    menu.run()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
