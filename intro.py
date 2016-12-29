import pygame
import constants
from spritesheet import blit_alpha
import covers


def run_intro(display):

    title_font = pygame.font.Font("resources/orionpax.otf", 72)
    title = title_font.render("By Sigton", True, constants.WHITE)
    title_rect = title.get_rect()

    title_x = (constants.SCREEN_WIDTH / 2) - (title_rect.width / 2)
    title_y = (constants.SCREEN_HEIGHT / 2) - (title_rect.height / 2)

    dark_background = covers.DarkScreen()

    pygame.time.wait(500)

    game_exit = False

    # Fade the text in
    for n in range(63):

        gen = (x for x in pygame.event.get() if x.type == pygame.QUIT)
        for x in gen:
            game_exit = True
        if game_exit:
            break
        display.fill(constants.BLACK)
        dark_background.draw(display)

        blit_alpha(display, title, (title_x, title_y), n*4)

        pygame.display.flip()
        pygame.time.wait(25)

    return game_exit if game_exit else pygame.time.wait(1000)
