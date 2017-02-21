import pygame

import game as g
import spritesheet


class Button(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet, sprite_sheet_data):

        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet(sprite_sheet)

        self.image_inactive = self.sprite_sheet.get_image(sprite_sheet_data[0][0],
                                                          sprite_sheet_data[0][1],
                                                          sprite_sheet_data[0][2],
                                                          sprite_sheet_data[0][3])

        self.image_active = self.sprite_sheet.get_image(sprite_sheet_data[1][0],
                                                        sprite_sheet_data[1][1],
                                                        sprite_sheet_data[1][2],
                                                        sprite_sheet_data[1][3])

        self.image = self.image_inactive

        self.rect = self.image.get_rect()


class Menu:

    def __init__(self, display, clock):

        self.display = display
        self.clock = clock

        self.game = g.Game(display, clock)

        main_menu_buttons = list()
        main_menu_buttons.append(Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 0, 360, 80))))
        main_menu_buttons.append(Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 0, 360, 80))))
        main_menu_buttons.append(Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 0, 360, 80))))

    def run(self):

        self.game.run()
