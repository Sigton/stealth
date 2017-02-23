import pygame

import spritesheet


class HUD(pygame.sprite.Sprite):

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/hud_bar.png")
        self.image = sprite_sheet.get_image(0, 0, 480, 48)

        self.rect = self.image.get_rect()
        self.rect.centerx = 480
        self.rect.y = 672

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))
