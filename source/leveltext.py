import pygame
import constants


class LevelText(pygame.sprite.Sprite):

    player = None

    def __init__(self, text, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font("resources/alienleague.ttf", 18)

        self.image = self.font.render(text, True, constants.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
