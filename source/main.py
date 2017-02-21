import pygame
from pygame.locals import *

import game
import constants


def main():

    # Main Program

    # Initiate pygame
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()

    # Set the display size
    game_display = pygame.display.set_mode(constants.SIZE)

    # Hide the mouse
    pygame.mouse.set_visible(False)

    # Set the window caption and icon
    pygame.display.set_caption("Stealth")

    icon_img = pygame.image.load("resources/icon.ico")

    icon = pygame.Surface([32, 32], flags=SRCALPHA)
    icon = icon.convert_alpha()
    icon.blit(icon_img, (0, 0))
    pygame.display.set_icon(icon)

    # Used to manage update frequency
    clock = pygame.time.Clock()

    # Run the game
    game.game(game_display, clock)  # Nice and easy way to avoid scoping issues

    pygame.mouse.set_visible(True)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
