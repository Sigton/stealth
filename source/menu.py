import pygame

import game as g
import spritesheet


class Button(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet, sprite_sheet_data):

        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet(sprite_sheet)

        self.image = self.sprite_sheet.get_image(sprite_sheet_data[0],
                                                 sprite_sheet_data[1],
                                                 sprite_sheet_data[2],
                                                 sprite_sheet_data[3])

        self.rect = self.image.get_rect()


class Menu:

    def __init__(self, display, clock):

        self.display = display
        self.clock = clock

        self.game = g.Game(display, clock)

    def run(self):

        self.game.run()
