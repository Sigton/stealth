import pygame
import constants


class Blackout(pygame.sprite.Sprite):

    # The player that this
    # sprite needs to follow
    player = None

    def __init__(self):

        # Constructor

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        self.image = pygame.image.load("resources/blackout.png").convert_alpha()

        # Set the images rectangle
        self.rect = self.image.get_rect()

    def update(self):

        # Center its image over the center of the player
        self.rect.x = (self.player.rect.x + (self.player.rect.width / 2)) - (self.rect.width / 2)
        self.rect.y = (self.player.rect.y + (self.player.rect.height / 2)) - (self.rect.height / 2)

    def draw(self, display):

        # Blit to the display at its current position
        display.blit(self.image, (self.rect.x, self.rect.y))


class LoadingScreen(pygame.sprite.Sprite):

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        self.image_file_large = pygame.image.load("resources/loading_screen.png")
        self.image_file_small = pygame.image.load("resources/loading_screen_small.png")

        self.image_large = pygame.Surface([960, 720], flags=pygame.SRCALPHA)
        self.image_large = self.image_large.convert_alpha()
        self.image_large.blit(self.image_file_large, (0, 0))

        self.image_small = pygame.Surface([720, 540], flags=pygame.SRCALPHA)
        self.image_small = self.image_small.convert_alpha()
        self.image_small.blit(self.image_file_small, (0, 0))

        self.image = self.image_large

        self.rect = self.image.get_rect()
        self.rect.center = constants.SCREEN_CENTER

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

        self.rect = self.image.get_rect()
        self.rect.center = constants.SCREEN_CENTER

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class GameOverScreen(pygame.sprite.Sprite):

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        self.image_large = pygame.image.load("resources/gameover.png").convert_alpha()
        self.image_small = pygame.image.load("resources/gameover_small.png").convert_alpha()

        self.image = self.image_large

        self.rect = self.image.get_rect()
        self.rect.center = constants.SCREEN_CENTER

    def draw(self, display):

        display.blit(self.image, (0, 0))


class GameOverScreen2(GameOverScreen):

    def __init__(self):

        GameOverScreen.__init__(self)

        self.image_large = pygame.image.load("resources/gameover2.png").convert_alpha()
        self.image_small = pygame.image.load("resources/gameover2_small.png").convert_alpha()

        self.image = self.image_large
