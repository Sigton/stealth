import pygame

import spritesheet
import funcs

class Torch(pygame.sprite.Sprite):

    direction = "R"

    guard = None

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/light.png")
        self.image_r = self.sprite_sheet.get_image(0, 0, 160, 94)
        self.image_l = self.sprite_sheet.get_image(0, 94, 160, 94)

        self.image = self.image_r

        self.rect = self.image.get_rect()

        self.hitmask = funcs.create_mask(self.image)

    def update(self):

        # Move to guards position
        self.direction = self.guard.direction

        if self.direction == "R":
            self.image = self.image_r
            self.rect.x = self.guard.rect.x + self.guard.rect.width / 2

            self.hitmask = funcs.create_mask(self.image)
        else:
            self.image = self.image_l
            self.rect.x = (self.guard.rect.x + self.guard.rect.width / 2) - self.rect.width

            self.hitmask = funcs.create_mask(self.image)

        self.rect.y = self.guard.rect.y - self.guard.rect.height / 2
