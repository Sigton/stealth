import pygame

import game


def main():

    # Main Program

    # Initiate pygame
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()

    game.game()

if __name__ == "__main__":
    main()
