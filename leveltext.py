import pygame


class Level01(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level1.png")

        self.image = pygame.Surface([362, 84], flags=pygame.SRCALPHA)
        self.image = self.image.covert_alpha()
        self.image.blit(self.image_file, (0,0))

        self.rect = self.image.get_rect()
