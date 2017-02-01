import pygame
import spritesheet
import math


class Arm(pygame.sprite.Sprite):

    sprite_sheet = None

    guard = None

    def __init__(self):

        # Constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the image
        self.sprite_sheet = spritesheet.SpriteSheet("resources/arms.png")

        self.arm_right = self.sprite_sheet.get_image(0, 0, 28, 12)
        self.arm_left = self.sprite_sheet.get_image(0, 12, 28, 12)

        self.image = self.arm_right

        # Set a reference to the images rectangle
        self.rect = self.image.get_rect()

    def update(self):

        self.rect.x = self.guard.rect.x + self.guard.rect.width / 4
        self.rect.y = self.guard.rect.y + self.guard.rect.height / 4