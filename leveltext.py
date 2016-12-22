import pygame
import constants


class LevelText(pygame.sprite.Sprite):

    player = None

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

    def update(self):

        if self.player.rect.x < constants.SCREEN_WIDTH / 2:
            self.rect.x = constants.SCREEN_WIDTH - self.rect.width - 10
            if self.player.rect.y < constants.SCREEN_HEIGHT / 2:
                self.rect.y = constants.SCREEN_HEIGHT - self.rect.height - 10
            else:
                self.rect.y = 10
        else:
            self.rect.x = 10
            if self.player.rect.y < constants.SCREEN_HEIGHT / 2:
                self.rect.y = constants.SCREEN_HEIGHT - self.rect.height - 10
            else:
                self.rect.y = 10

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class Level01(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level1.png")

        self.image = pygame.Surface([362, 84], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level02(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level2.png")

        self.image = pygame.Surface([318, 126], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level03(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level3.png")

        self.image = pygame.Surface([327, 126], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level04(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level4.png")

        self.image = pygame.Surface([381, 84], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level05(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level5.png")

        self.image = pygame.Surface([351, 126], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()
