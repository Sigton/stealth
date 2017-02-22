import pygame
from pygame.locals import *

import game as g
import spritesheet
import constants


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


class Text(pygame.sprite.Sprite):

    def __init__(self, text, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font("resources/alienleague.ttf", 48)

        self.image = self.font.render(text, True, constants.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Menu:

    def __init__(self, display, clock):

        self.display = display
        self.clock = clock

        self.game = g.Game(display, clock)

        self.background = pygame.image.load("resources/menubackground.png").convert()

        self.main_menu_buttons = list()
        self.main_menu_buttons.append(Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 0, 360, 80))))
        self.main_menu_buttons.append(Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 0, 360, 80))))
        self.main_menu_buttons.append(Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 0, 360, 80))))

        self.title = Text("STEALTH", 300, 100)

    def run(self):

        game_exit = False

        while not game_exit:

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

            self.display.fill(constants.BLACK)
            self.display.blit(self.background, (0, 0))

            self.display.blit(self.title.image, (self.title.rect.x, self.title.rect.y))

            pygame.display.update()
            self.clock.tick(60)
