import pygame
import constants


def run_intro(display):

    title_font = pygame.font.Font("resources/orionpax.otf", 72)
    title = title_font.render("Sigton", True, constants.WHITE)
    title_rect = title.get_rect()

    title_x = (constants.SCREEN_WIDTH / 2) - (title_rect.width / 2)
    title_y = (constants.SCREEN_HEIGHT / 2) - (title_rect.height / 2)
    display.blit(title, (title_x, title_y))

    pygame.display.flip()
    pygame.time.wait(4000)
