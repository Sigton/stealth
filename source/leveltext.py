import pygame
import constants


class LevelText(pygame.sprite.Sprite):

    player = None

    def __init__(self, text, x, y):

        pygame.sprite.Sprite.__init__(self)
