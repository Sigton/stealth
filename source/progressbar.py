import pygame
import spritesheet
import entities


class ProgressBar(pygame.sprite.Sprite):

    parent = None
    level = None

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/healthbar.png")

        self.images = []

        image = self.sprite_sheet.get_image(0, 0, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(0, 16, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(0, 32, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(0, 48, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(0, 64, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(0, 80, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(32, 0, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(32, 16, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(32, 32, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(32, 48, 32, 16)
        self.images.append(image)

        image = self.sprite_sheet.get_image(32, 64, 32, 16)
        self.images.append(image)

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.start_x = None
        self.start_y = None

        self.timer = 30

    def update(self):

        self.rect.x = self.parent.rect.x + (self.parent.rect.width/2 - self.rect.width/2)
        self.rect.y = self.parent.rect.y - 20

        if self.start_x is None and self.start_y is None:
            self.start_x = self.rect.x
            self.start_y = self.rect.y

        self.image = self.images[self.parent.progress]

        if self.parent.progress >= 10 and self.timer:
            self.timer -= 1

        if not self.timer and self.parent.progress >= 10 and not isinstance(self.parent, entities.RechargingKeypad):
            self.level.entities.remove(self)
