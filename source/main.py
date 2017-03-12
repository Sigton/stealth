import pygame
from pygame.locals import *

import menu as m
import constants
import sys


class Main:

    def __init__(self):
        # Main Program

        # Initiate pygame
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # Set the display size
        self.game_display = pygame.display.set_mode(constants.SIZE)

        # Set the window caption and icon
        pygame.display.set_caption("Stealth")

        icon_img = pygame.image.load("resources/icon.ico")

        icon = pygame.Surface([32, 32], flags=SRCALPHA)
        icon = icon.convert_alpha()
        icon.blit(icon_img, (0, 0))
        pygame.display.set_icon(icon)

        # Used to manage update frequency
        self.clock = pygame.time.Clock()

    def run(self):

        # Start the menu
        menu = m.Menu(self.game_display, self.clock)
        menu.run()

        # Quit the game
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    # Begin everything
    game = Main()
    game.run()
