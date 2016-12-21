import pygame
import spritesheet


class Blackout(pygame.sprite.Sprite):

    player = None

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/blackout.png")
        self.image = self.sprite_sheet.get_image(0, 0, 2000, 1500)

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

        self.image = spritesheet.SpriteSheet("resources/loading_screen.png").get_image(0, 0, 960, 720)

        self.rect = self.image.get_rect()

    def draw(self, display):

        display.blit(self.image, (0, 0))
