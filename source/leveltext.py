import pygame
try:
    import constants
except ImportError:
    import source


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


class Level06(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level6.png")

        self.image = pygame.Surface([353, 42], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level07(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level7.png")

        self.image = pygame.Surface([431, 84], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level08(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level8.png")

        self.image = pygame.Surface([396, 84], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level09(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level9.png")

        self.image = pygame.Surface([412, 84], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level10(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level10.png")

        self.image = pygame.Surface([459, 84], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()


class Level11(LevelText):

    def __init__(self):

        LevelText.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/text/level11.png")

        self.image = pygame.Surface([361, 84], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()
