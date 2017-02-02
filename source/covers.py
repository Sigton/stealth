import pygame


class Blackout(pygame.sprite.Sprite):

    player = None

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/blackout.png")

        self.image = pygame.Surface([2000, 1500], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()

    def update(self):

        self.rect.x = (self.player.rect.x + (self.player.rect.width / 2)) - (self.rect.width / 2)
        self.rect.y = (self.player.rect.y + (self.player.rect.height / 2)) - (self.rect.height / 2)

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class LoadingScreen(pygame.sprite.Sprite):

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/loading_screen.png")

        self.image = pygame.Surface([960, 720], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

        self.rect = self.image.get_rect()

    def draw(self, display):

        display.blit(self.image, (0, 0))


class DarkScreen(pygame.sprite.Sprite):

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        self.image_file = pygame.image.load("resources/darkscreen.png")

        self.image = pygame.Surface([960, 720], flags=pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.blit(self.image_file, (0, 0))

    def draw(self, display):

        display.blit(self.image, (0, 0))
