import pygame
import spritesheet


class HealthBar(pygame.sprite.Sprite):

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

        self.image = self.images[10]

        self.rect = self.image.get_rect()


class ProgressBar(pygame.sprite.Sprite):

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

        self.image = self.images[10]

        self.rect = self.image.get_rect()

        self.progress = 0
