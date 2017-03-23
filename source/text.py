import pygame
import constants

if not pygame.font.get_init():
    pygame.font.init()


class LevelText(pygame.sprite.Sprite):

    player = None

    def __init__(self, text, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font("resources/alienleague.ttf", 22)

        self.image = self.font.render(text, True, constants.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y


class LoadingLabel(pygame.sprite.Sprite):

    def __init__(self, text, x, y):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font("resources/alienleague.ttf", 36)

        self.image = self.font.render(text, True, constants.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_text(self, text, x, y):

        self.image = self.font.render(text, True, constants.WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class Text(pygame.sprite.Sprite):

    # Generic text class

    def __init__(self, text, size, x, y):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the font
        self.font = pygame.font.Font("resources/alienleague.ttf", size)

        # Draw the text
        self.image = self.font.render(text, True, constants.WHITE)

        # Then move it
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
